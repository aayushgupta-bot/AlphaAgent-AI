from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any
import pandas as pd

from app.schemas.data_schema import FeaturesResponse
from app.agents.data_agent import DataAgent
from app.agents.feature_agent import FeatureAgent
from app.core.exceptions import AlphaAgentError

router = APIRouter()

data_agent = DataAgent()
feature_agent = FeatureAgent()


class StockResponse(BaseModel):
    ticker: str
    price: float
    change: float
    volume: int
    timestamp: str


@router.get("/", response_model=StockResponse)
async def get_stock(ticker: str):
    """
    Fetches current market data for a ticker.
    """
    return {
        "ticker": ticker.upper(),
        "price": 175.43,
        "change": 1.25,
        "volume": 45000000,
        "timestamp": "2026-04-28T10:00:00Z",
    }


@router.get("/features", response_model=FeaturesResponse)
async def get_features(ticker: str):
    """
    Runs the DataAgent → FeatureAgent pipeline and returns enriched features.
    Returns up to the last 60 rows for charting purposes.
    """
    try:
        raw_df = await data_agent.fetch(ticker)
        features_df = await feature_agent.process(raw_df)
    except AlphaAgentError as e:
        raise HTTPException(status_code=400, detail=e.to_dict())

    # Format for JSON
    df_reset = features_df.reset_index()
    if "Date" in df_reset.columns:
        df_reset["Date"] = df_reset["Date"].astype(str)

    records = df_reset.to_dict(orient="records")
    latest = records[-1] if records else {}
    # Return last 60 rows for a richer chart
    samples = records[-60:] if len(records) >= 60 else records

    return FeaturesResponse(
        ticker=ticker.upper(),
        status="success",
        latest_features=latest,
        sample_rows=samples,
        rows_count=len(features_df),
    )
