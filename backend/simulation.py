import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

# ---------- Utility ----------
def annualize(mu_daily: float) -> float:
    return mu_daily * 252

def deannualize_sigma(sigma_annual: float) -> float:
    return sigma_annual / np.sqrt(252)

# ---------- Stock Returns ----------
def estimate_mu_sigma_from_prices(prices: np.ndarray) -> Tuple[float, float]:
    # log returns
    r = np.diff(np.log(prices))
    mu_daily = r.mean()
    sigma_daily = r.std(ddof=1)
    mu_annual = mu_daily * 252
    sigma_annual = sigma_daily * np.sqrt(252)
    return mu_annual, sigma_annual


def simulate_gbm(start_price: float, mu_annual: float, sigma_annual: float, horizon_days: int, trials: int) -> Dict[str, Any]:
    dt = 1/252
    mu = mu_annual
    sigma = sigma_annual
    # daily
    z = np.random.normal(size=(trials, horizon_days))
    increments = (mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z
    paths = start_price * np.exp(np.cumsum(increments, axis=1))
    terminal = paths[:, -1]
    pnl = terminal - start_price
    return {
        "terminal": terminal,
        "paths_sample": paths[:100].tolist(),
        "pnl": pnl,
    }


def simulate_bootstrap(prices: np.ndarray, horizon_days: int, trials: int) -> Dict[str, Any]:
    r = np.diff(np.log(prices))
    n = len(r)
    idx = np.random.randint(0, n, size=(trials, horizon_days))
    boot = r[idx].cumsum(axis=1)
    start = prices[-1]
    paths = start * np.exp(boot)
    terminal = paths[:, -1]
    pnl = terminal - start
    return {
        "terminal": terminal,
        "paths_sample": paths[:100].tolist(),
        "pnl": pnl,
    }

# ---------- Startup Costs ----------
# Supported dists: normal, lognormal, triangular, uniform
def sample_dist(name: str, params: Dict[str, float], size):
    if name == "normal":
        return np.random.normal(params.get("mu", 0), params.get("sigma", 1), size)
    if name == "lognormal":
        mu = params.get("mu", 0)
        sigma = params.get("sigma", 1)
        return np.random.lognormal(mean=mu, sigma=sigma, size=size)
    if name == "triangular":
        left = params.get("left", 0)
        mode = params.get("mode", 1)
        right = params.get("right", 2)
        return np.random.triangular(left, mode, right, size)
    if name == "uniform":
        low = params.get("low", 0)
        high = params.get("high", 1)
        return np.random.uniform(low, high, size)
    raise ValueError(f"Unsupported distribution: {name}")


def simulate_startup_costs(items, periods: int, trials: int) -> Dict[str, Any]:
    # items: list of {name, dist, ...params}
    draws = []
    for it in items:
        dist_name = it.get("dist", "normal")
        params = {k: v for k, v in it.items() if k not in ["name", "dist"]}
        X = sample_dist(dist_name, params, size=(trials, periods))
        draws.append(X)
    # total per period and cumulative
    total_period = np.sum(draws, axis=0)  # (trials, periods)
    cum_total = np.cumsum(total_period, axis=1)
    terminal = cum_total[:, -1]
    return {
        "terminal": terminal,
        "cum_paths_sample": cum_total[:100].tolist(),
    }

# ---------- Credit Risk ----------
# Vasicek one‑factor style Monte Carlo for default correlation.
def simulate_credit_risk(loans, correlation: float, horizon_years: float, trials: int) -> Dict[str, Any]:
    # loans: [{ead, pd, lgd}] with annual PD; horizon_years used to scale PD ~ 1 - (1 - PD)^t
    pd_vec = np.array([1 - (1 - l.get("pd", 0.01))**horizon_years for l in loans])
    lgd_vec = np.array([l.get("lgd", 0.45) for l in loans])
    ead_vec = np.array([l.get("ead", 1000.0) for l in loans])

    n = len(loans)
    rho = np.clip(correlation, 0.0, 0.99)

    # Thresholds from PDs
    from scipy.stats import norm
    thresh = norm.ppf(pd_vec)

    # Common factor Z and idiosyncratic eps
    Z = np.random.normal(size=(trials, 1))
    eps = np.random.normal(size=(trials, n))
    asset = np.sqrt(rho) * Z + np.sqrt(1 - rho) * eps
    default_mat = (asset < thresh).astype(int)

    # Loss = default * LGD * EAD
    loss = (default_mat * lgd_vec * ead_vec).sum(axis=1)
    return {
        "portfolio_loss": loss,
        "default_counts": default_mat.sum(axis=1)
    }

# ---------- Risk Metrics ----------
def var_es(sample: np.ndarray, alpha: float) -> Dict[str, float]:
    sample_sorted = np.sort(sample)
    idx = int(np.floor(alpha * len(sample_sorted)))
    idx = min(max(idx, 0), len(sample_sorted)-1)
    var = sample_sorted[idx]
    es = sample_sorted[:idx+1].mean() if idx >= 0 else sample_sorted.mean()
    return {"VaR": float(var), "ES": float(es)}
