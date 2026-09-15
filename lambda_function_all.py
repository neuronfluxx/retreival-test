import io
import os
import urllib.parse

import boto3
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from pypdf import PdfReader

s3 = boto3.client("s3")

# Initialize ChromaDB client
CHROMA_DB_PATH = os.environ.get("CHROMA_DB_PATH", "./chroma_db")
CHROMA_COLLECTION_NAME = os.environ.get("CHROMA_COLLECTION_NAME", "rag-test-collection")
chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)

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
    
    # Prepare for ChromaDB
    ids = []
    documents = []
    metadatas = []
    
    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        ids.append(f"{key}#{i}")
        documents.append(chunk)
        metadatas.append({"source": key})
    
    # Add to ChromaDB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )
    print(f"Added {len(ids)} chunks for {key} to ChromaDB")


def handle_delete(bucket, key):
    # Delete all vectors with matching source in ChromaDB
    try:
        # Get all documents with matching source
        results = collection.get(where={"source": key})
        ids = results["ids"]
        if ids:
            collection.delete(ids=ids)
            print(f"Deleted {len(ids)} vectors for {key}")
        else:
            print(f"No vectors found for {key}")
    except Exception as e:
        print(f"Error deleting from ChromaDB: {e}")


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
