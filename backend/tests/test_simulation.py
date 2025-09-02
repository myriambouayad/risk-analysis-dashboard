import numpy as np
from simulation import simulate_gbm, var_es

def test_gbm_shapes():
    out = simulate_gbm(100, 0.1, 0.2, horizon_days=10, trials=500)
    assert len(out["terminal"]) == 500
    assert len(out["paths_sample"]) <= 100

def test_var_monotone():
    x = np.random.normal(0,1,10000)
    m95 = var_es(x, 0.95)["VaR"]
    m99 = var_es(x, 0.99)["VaR"]
    assert m99 >= m95
