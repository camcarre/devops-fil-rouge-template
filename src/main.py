from fastapi import FastAPI

from src.routers import auth, categories, posts, topics

app = FastAPI(title="Forum DevOps")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(topics.router)
app.include_router(posts.router)
