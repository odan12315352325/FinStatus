from pydantic import BaseModel, Field, conlist
from typing import Optional

class PredictRequest(BaseModel):
    inn: str = Field(..., min_length=10, max_length=12)
    company_name: Optional[str] = None
    year: int = Field(..., ge=1990, le=2100)
    quarter: Optional[int] = Field(default=None, ge=1, le=4)

    # строго 35 чисел
    features: conlist(float, min_length=35, max_length=35)