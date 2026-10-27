from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401  (importing registers the tables on Base)
from app.config import CORS_ORIGINS
from app.database import Base, engine
from app.routers import auth, expenses, groups


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Fine for a small project; a bigger one would use migrations (Alembic) instead.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="SplitKaro API",
    description="Split shared expenses with your flatmates, hostel friends or trip group.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(groups.router)
app.include_router(expenses.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
