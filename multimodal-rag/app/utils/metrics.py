"""Prometheus metrics for monitoring"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST


# Request metrics
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

# Document processing metrics
documents_processed_total = Counter(
    "documents_processed_total",
    "Total documents processed",
    ["document_type", "status"]
)

document_processing_duration_seconds = Histogram(
    "document_processing_duration_seconds",
    "Document processing duration in seconds",
    ["document_type"]
)

# Embedding metrics
embeddings_generated_total = Counter(
    "embeddings_generated_total",
    "Total embeddings generated",
    ["embedding_type"]
)

embedding_generation_duration_seconds = Histogram(
    "embedding_generation_duration_seconds",
    "Embedding generation duration in seconds",
    ["embedding_type"]
)

# Vector store metrics
vector_store_operations_total = Counter(
    "vector_store_operations_total",
    "Total vector store operations",
    ["operation", "status"]
)

vector_store_size = Gauge(
    "vector_store_size",
    "Number of vectors in store",
    ["collection"]
)

# Query metrics
queries_total = Counter(
    "queries_total",
    "Total queries processed",
    ["query_type"]
)

query_duration_seconds = Histogram(
    "query_duration_seconds",
    "Query processing duration in seconds",
    ["query_type"]
)

retrieval_results_count = Histogram(
    "retrieval_results_count",
    "Number of results retrieved per query"
)

# Agent metrics
agent_iterations_total = Counter(
    "agent_iterations_total",
    "Total agent iterations",
    ["agent_type"]
)

agent_execution_duration_seconds = Histogram(
    "agent_execution_duration_seconds",
    "Agent execution duration in seconds",
    ["agent_type"]
)

# Error metrics
errors_total = Counter(
    "errors_total",
    "Total errors",
    ["error_type"]
)


def get_metrics():
    """Get current metrics in Prometheus format"""
    return generate_latest()
