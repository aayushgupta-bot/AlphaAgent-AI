from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class FeaturesResponse(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol")
    status: str = Field("success", description="Status of the feature generation")
    latest_features: Dict[str, Any] = Field(..., description="The most recent feature vector")
    sample_rows: List[Dict[str, Any]] = Field(..., description="Last N rows of the features dataframe")
    rows_count: int = Field(..., description="Total number of valid rows after dropping NaNs")
