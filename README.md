# Risk Analysis Dashboard

Upload data → run Monte Carlo simulations (GBM, bootstrap returns, startup cost distributions, correlated credit defaults). Outputs VaR/ES, loss/PNL distributions, and charts. Built with React + FastAPI.

## Quickstart

### Backend
```bash
cd backend
python -m venv .venv
# activate: source .venv/bin/activate (Mac/Linux)  OR  .venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Web: http://localhost:5173  |  API: http://localhost:8000

## API Example
POST /simulate
- GBM:
```json
{ "model":"gbm","trials":20000,"horizon_days":252,"confidence":0.95,"prices":[100,101.2,99.5,102.1] }
```
