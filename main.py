from fastapi import FastAPI
from routers.movies import router as movies_router

app = FastAPI(
    title="WatchList API",
    description="REST API untuk mengelola daftar film favorit",
    version="1.0.0",
)

app.include_router(movies_router, prefix="/api/v1")


@app.get("/")
def home():
    return {
        "message": "WatchList API berjalan",
        "docs": "/docs",
    }
