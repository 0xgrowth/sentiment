# --- BUGS ABOUND

import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from core.config import get_settings

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

APP_NAME = "AI Market Tracker"
APP_VERSION = "1.0.0"
ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# -----------------------------------------------------------------------------
# Logging Setup
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger("ai-market-tracker")

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
# Lifespan Events (Startup / Shutdown)
# -----------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(" Starting AI Market Tracker...")
    # Initialize DB connections, model loading, schedulers here
    yield
    logger.info(" Shutting down AI Market Tracker...")


# -----------------------------------------------------------------------------
# FastAPI App Initialization
# -----------------------------------------------------------------------------

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    debug=DEBUG,
    lifespan=lifespan,
)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------------------------
# Health Check
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
# Create Tables
# -----------------------------------------------------------------------------


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# -----------------------------------------------------------------------------
# Market Data Endpoint
# -----------------------------------------------------------------------------

@app.get("/market/{symbol}", response_model=MarketData)
async def get_market_data(symbol: str):
    """
    Fetch real-time market data.
    Replace with actual exchange API integration.
    """
    logger.info(f"Fetching market data for {symbol}")

    # Placeholder mock response
    return MarketData(
        symbol=symbol.upper(),
        price=150.25,
        timestamp=datetime.utcnow(),
    )


# -----------------------------------------------------------------------------
# AI Prediction Endpoint
# -----------------------------------------------------------------------------

def mock_ai_model(prices: List[float]) -> float:
    """
    Placeholder AI prediction logic.
    Replace with ML model inference.
    """
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
# Background Task Example
# -----------------------------------------------------------------------------

def log_prediction(symbol: str):
    logger.info(f"Prediction generated for {symbol}")


@app.post("/predict-with-log", response_model=PredictionResponse)
async def predict_with_background(
    request: PredictionRequest,
    background_tasks: BackgroundTasks,
):
    predicted = mock_ai_model(request.historical_prices)

    background_tasks.add_task(log_prediction, request.symbol)

    return PredictionResponse(
        symbol=request.symbol.upper(),
        predicted_price=round(predicted, 2),
        confidence=0.87,
    )


# -----------------------------------------------------------------------------
# Run Server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=DEBUG,
    )

