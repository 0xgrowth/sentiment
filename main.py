import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db, engine, Base
from app.models import User  # <-- make sure this exists

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

APP_NAME = "AI Market Tracker"
APP_VERSION = "1.0.0"
ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger("ai-market-tracker")

# -----------------------------------------------------------------------------
# Lifespan
# -----------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Market Tracker...")
    await init_db()
    yield
    logger.info("Shutting down AI Market Tracker...")

# -----------------------------------------------------------------------------
# App Initialization
# -----------------------------------------------------------------------------

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG,
    lifespan=lifespan,
)

# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Database Init
# -----------------------------------------------------------------------------

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# -----------------------------------------------------------------------------
# Pydantic Models
# -----------------------------------------------------------------------------

class MarketData(BaseModel):
    symbol: str
    price: float
    timestamp: datetime


class PredictionRequest(BaseModel):
    symbol: str
    historical_prices: List[float]


class PredictionResponse(BaseModel):
    symbol: str
    predicted_price: float
    confidence: float


# -----------------------------------------------------------------------------
# Health
# -----------------------------------------------------------------------------

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "environment": ENV,
        "timestamp": datetime.utcnow(),
    }

# -----------------------------------------------------------------------------
# Users
# -----------------------------------------------------------------------------

@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

# -----------------------------------------------------------------------------
# Market Data
# -----------------------------------------------------------------------------

@app.get("/market/{symbol}", response_model=MarketData)
async def get_market_data(symbol: str):
    logger.info(f"Fetching market data for {symbol}")

    return MarketData(
        symbol=symbol.upper(),
        price=150.25,
        timestamp=datetime.utcnow(),
    )

# -----------------------------------------------------------------------------
# AI Prediction
# -----------------------------------------------------------------------------

def mock_ai_model(prices: List[float]) -> float:
    if not prices:
        raise ValueError("Prices list cannot be empty")
    return sum(prices) / len(prices) * 1.02


@app.post("/predict", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    if not request.historical_prices:
        raise HTTPException(status_code=400, detail="Historical prices required")

    predicted = mock_ai_model(request.historical_prices)

    return PredictionResponse(
        symbol=request.symbol.upper(),
        predicted_price=round(predicted, 2),
        confidence=0.87,
    )

# -----------------------------------------------------------------------------
# Background Task
# -----------------------------------------------------------------------------

def log_prediction(symbol: str):
    logger.info(f"Prediction generated for {symbol}")


@app.post("/predict-with-log", response_model=PredictionResponse)
async def predict_with_background(
    request: PredictionRequest,
    background_tasks: BackgroundTasks,
):
    if not request.historical_prices:
        raise HTTPException(status_code=400, detail="Historical prices required")

    predicted = mock_ai_model(request.historical_prices)

    background_tasks.add_task(log_prediction, request.symbol)

    return PredictionResponse(
        symbol=request.symbol.upper(),
        predicted_price=round(predicted, 2),
        confidence=0.87,
    )