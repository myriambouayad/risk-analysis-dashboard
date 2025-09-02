from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

ModelType = Literal["gbm", "bootstrap", "startup_costs", "credit_risk"]

class SimulationRequest(BaseModel):
    model: ModelType
    trials: int = Field(ge=100, le=1_000_000, default=20_000)
    horizon_days: int = 252
    confidence: float = Field(gt=0, lt=1, default=0.95)

    # Data payloads (one of the following depending on model)
    # Stock/returns
    prices: Optional[List[float]] = None  # ordered historical prices
    mu: Optional[float] = None            # annualized drift (if provided)
    sigma: Optional[float] = None         # annualized vol (if provided)
    start_price: Optional[float] = None

    # Startup costs (per line item: distribution params)
    costs: Optional[List[Dict]] = None    # [{"name":"rent","dist":"normal","mu":1000,"sigma":200}, ...]
    periods: Optional[int] = None         # months

    # Credit risk (portfolio of loans)
    loans: Optional[List[Dict]] = None    # [{"ead":100000,"pd":0.02,"lgd":0.45}, ...]
    correlation: Optional[float] = None   # asset correlation in [0,1]
