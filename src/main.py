from time import time

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, CONTENT_TYPE_LATEST, REGISTRY, generate_latest

from src.routers import auth, categories, posts, topics

app = FastAPI(title="Forum DevOps")

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests processed by the application",
    ["method", "path", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
)


@app.middleware("http")
async def prometheus_metrics_middleware(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    elapsed = time() - start_time

    REQUEST_LATENCY.labels(method=request.method, path=request.url.path).observe(elapsed)
    REQUEST_COUNT.labels(
        method=request.method,
        path=request.url.path,
        status=str(response.status_code),
    ).inc()

    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(topics.router)
app.include_router(posts.router)
