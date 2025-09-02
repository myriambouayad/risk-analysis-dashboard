from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import numpy as np

from schemas import SimulationRequest
from simulation import (
    estimate_mu_sigma_from_prices, simulate_gbm, simulate_bootstrap,
    simulate_startup_costs, simulate_credit_risk, var_es
)

app = FastAPI(title="Risk Analysis Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/simulate")
def simulate(req: SimulationRequest) -> Dict[str, Any]:
    model = req.model

    if model in ("gbm", "bootstrap"):
        if req.prices and (req.mu is None or req.sigma is None):
            mu, sigma = estimate_mu_sigma_from_prices(np.array(req.prices, dtype=float))
        else:
            mu = float(req.mu or 0.08)
            sigma = float(req.sigma or 0.2)
        start_price = float(req.start_price or (req.prices[-1] if req.prices else 100.0))

        if model == "gbm":
            out = simulate_gbm(start_price, mu, sigma, req.horizon_days, req.trials)
        else:
            if not req.prices:
                raise ValueError("bootstrap requires historical prices")
            out = simulate_bootstrap(np.array(req.prices, dtype=float), req.horizon_days, req.trials)

        metrics = var_es(out["pnl"], req.confidence)
        # Ensure JSON-serializable
        serial = {k: (v if isinstance(v, list) else (v.tolist() if hasattr(v, "tolist") else v)) for k, v in out.items()}
        return {"model": model, "metrics": metrics, **serial}

    if model == "startup_costs":
        assert req.costs and req.periods, "costs (list) and periods (int) required"
        out = simulate_startup_costs(req.costs, req.periods, req.trials)
        metrics = var_es(out["terminal"], req.confidence)
        serial = {k: (v if isinstance(v, list) else (v.tolist() if hasattr(v, "tolist") else v)) for k, v in out.items()}
        return {"model": model, "metrics": metrics, **serial}

    if model == "credit_risk":
        assert req.loans, "loans required"
        out = simulate_credit_risk(req.loans, req.correlation or 0.2, req.horizon_days / 252.0, req.trials)
        metrics = var_es(out["portfolio_loss"], req.confidence)
        serial = {k: (v if isinstance(v, list) else (v.tolist() if hasattr(v, "tolist") else v)) for k, v in out.items()}
        return {"model": model, "metrics": metrics, **serial}

    return {"error": "unknown model"}
