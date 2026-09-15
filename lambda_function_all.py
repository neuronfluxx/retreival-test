import io
import os
import urllib.parse

import boto3
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from pypdf import PdfReader

s3 = boto3.client("s3")
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(os.environ.get("PINECONE_INDEX_NAME", "integrated-dense-py"))

AZURE_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
AZURE_API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
AZURE_DEPLOYMENT = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
AZURE_API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
EMBED_DIM = 3072

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)


def embed(texts):
    url = f"{AZURE_ENDPOINT.rstrip('/')}/openai/deployments/{AZURE_DEPLOYMENT}/embeddings?api-version={AZURE_API_VERSION}"
    headers = {"Content-Type": "application/json", "api-key": AZURE_API_KEY}
    resp = requests.post(url, headers=headers, json={"input": texts}, timeout=30)
    resp.raise_for_status()
    return [d["embedding"] for d in resp.json()["data"]]


def handle_upsert(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    reader = PdfReader(io.BytesIO(obj["Body"].read()))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    chunks = splitter.split_text(text)
    if not chunks:
        print(f"No extractable text in {key}")
        return

    embeddings = embed(chunks)
    vectors = [
        {"id": f"{key}#{i}", "values": emb, "metadata": {"source": key, "text": chunk}}
        for i, (chunk, emb) in enumerate(zip(chunks, embeddings))
    ]
    index.upsert(vectors=vectors)
    print(f"Upserted {len(vectors)} chunks for {key}")


def handle_delete(bucket, key):
    # Serverless Pinecone indexes don't support delete-by-metadata-filter,
    # so find matching ids via a filtered query first, then delete by id.
    results = index.query(
        vector=[0.0] * EMBED_DIM,
        top_k=10000,
        filter={"source": key},
        include_values=False,
        include_metadata=False,
    )
    ids = [match["id"] for match in results["matches"]]
    if ids:
        index.delete(ids=ids)
    print(f"Deleted {len(ids)} vectors for {key}")


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        event_name = record["eventName"]

        if event_name.startswith("ObjectCreated"):
            handle_upsert(bucket, key)
        elif event_name.startswith("ObjectRemoved"):
            handle_delete(bucket, key)

    return {"statusCode": 200}
