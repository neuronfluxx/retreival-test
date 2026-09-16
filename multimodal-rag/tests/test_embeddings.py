"""Test embeddings generation"""

import pytest
from app.core.embeddings import get_embedding_generator


def test_text_embedding():
    """Test text embedding generation"""
    generator = get_embedding_generator()

    text = "This is a test document about machine learning."
    embedding = generator.generate_text_embedding(text)

    assert embedding is not None
    assert len(embedding) > 0
    assert isinstance(embedding, list)


def test_batch_text_embeddings():
    """Test batch text embedding generation"""
    generator = get_embedding_generator()

    texts = [
        "First document about AI",
        "Second document about machine learning",
        "Third document about deep learning"
    ]

    embeddings = generator.generate_text_embeddings_batch(texts)

    assert len(embeddings) == len(texts)
    assert all(isinstance(emb, list) for emb in embeddings)


def test_similarity_computation():
    """Test similarity computation"""
    generator = get_embedding_generator()

    text1 = "Machine learning is a subset of AI"
    text2 = "Artificial intelligence includes machine learning"
    text3 = "The weather is sunny today"

    emb1 = generator.generate_text_embedding(text1)
    emb2 = generator.generate_text_embedding(text2)
    emb3 = generator.generate_text_embedding(text3)

    sim_12 = generator.compute_similarity(emb1, emb2)
    sim_13 = generator.compute_similarity(emb1, emb3)

    # Similar texts should have higher similarity
    assert sim_12 > sim_13
