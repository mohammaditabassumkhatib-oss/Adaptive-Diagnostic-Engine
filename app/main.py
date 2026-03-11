from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routes import router
from app.db.seed import seed_questions

@asynccontextmanager
async def lifespan(app: FastAPI):
    await seed_questions()       # Seeds DB on startup if empty
    yield

app = FastAPI(
    title="Adaptive Diagnostic Engine",
    description="1D IRT-based adaptive testing system",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)