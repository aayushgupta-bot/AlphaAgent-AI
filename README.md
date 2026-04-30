# AlphaAgent AI

A production-grade, multi-agent AI system for stock analysis, forecasting, and explanation. Built with a clean 6-layer architecture where specialized agents orchestrate data ingestion, feature engineering, ML inference, signal generation, and LLM-powered explanations.

![Dashboard](https://img.shields.io/badge/status-live-brightgreen) ![Python](https://img.shields.io/badge/python-3.11+-blue) ![Next.js](https://img.shields.io/badge/next.js-16-black)

---

## Architecture

```
User Request → API Layer → Orchestrator Agent
                                │
                    ┌───────────┼───────────────┐
                    ▼           ▼               ▼
               DataAgent → FeatureAgent → MLAgent
                                              │
                                        SignalAgent
                                              │
                                      ExplanationAgent (LLM)
                                              │
                                         API Response
```

### System Layers

| # | Layer | Description |
|---|-------|-------------|
| 1 | **Data Layer** | OHLCV ingestion via yfinance with missing-value handling |
| 2 | **Feature Layer** | Technical indicators — MA, RSI, MACD, Bollinger, volatility |
| 3 | **Prediction Layer** | XGBoost regression for next-day close price |
| 4 | **Agent Layer** | Orchestrator + specialized agents with validation & error handling |
| 5 | **Signal Layer** | Converts predictions into BUY / SELL / HOLD with strength tiers |
| 6 | **Explanation Layer** | LLM-generated analysis via OpenRouter (grounded, no hallucination) |
| 7 | **API Layer** | FastAPI with typed Pydantic schemas |
| 8 | **Frontend Layer** | Next.js dashboard with Recharts visualization |

### Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js 16, Tailwind CSS v4, Recharts |
| Backend | FastAPI, Python 3.11+ |
| ML | XGBoost, scikit-learn, pandas, numpy |
| LLM | OpenRouter (openai/gpt-oss-20b) |
| Cache | Redis |
| Database | PostgreSQL |
| Queue | Celery |
| Container | Docker Compose |

---

## Project Structure

```
alpha-agent-ai/
├── frontend/                    # Next.js dashboard
│   ├── app/
│   │   ├── page.js              # Main dashboard page
│   │   ├── layout.js            # Root layout
│   │   └── globals.css          # Design system
│   ├── components/
│   │   ├── TickerInput.jsx      # Ticker search input
│   │   ├── StockChart.jsx       # Price history chart
│   │   ├── PredictionCard.jsx   # ML prediction display
│   │   ├── SignalCard.jsx       # BUY/SELL/HOLD signal
│   │   ├── ExplanationPanel.jsx # LLM analysis panel
│   │   └── MetadataBar.jsx      # Pipeline timing bar
│   └── services/
│       └── api.js               # API client
│
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── api/                 # Routes
│   │   │   ├── stock.py         # GET /api/stock, GET /api/stock/features
│   │   │   ├── predict.py       # GET /api/predict
│   │   │   └── chat.py          # POST /api/chat
│   │   ├── agents/              # Multi-agent system
│   │   │   ├── orchestrator.py  # Pipeline controller
│   │   │   ├── data_agent.py    # Data validation & fetching
│   │   │   ├── feature_agent.py # Indicator calculation
│   │   │   ├── ml_agent.py      # XGBoost inference
│   │   │   ├── signal_agent.py  # BUY/SELL/HOLD logic
│   │   │   ├── explanation_agent.py # LLM prompt engineering
│   │   │   └── rag_agent.py     # Context retrieval (placeholder)
│   │   ├── services/            # Business logic
│   │   │   ├── data_service.py  # yfinance OHLCV fetcher
│   │   │   ├── indicator_service.py # Technical indicators
│   │   │   ├── ml_service.py    # Model loading & inference
│   │   │   └── openrouter_service.py # LLM API client
│   │   ├── models/              # Trained ML models
│   │   │   ├── train_model.py   # Training script
│   │   │   ├── xgb.pkl          # Serialized XGBoost model
│   │   │   └── feature_cols.pkl # Feature column manifest
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   └── core/                # Exceptions & shared utilities
│   │       └── exceptions.py    # DataError, FeatureError, PredictionError
│   ├── workers/                 # Celery background tasks
│   ├── config/                  # Settings & environment
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── .env                         # API keys (do not commit)
└── README.md
```

---

## API Endpoints

### `GET /api/predict?ticker=AAPL`

Full multi-agent pipeline — returns prediction, signal, and LLM explanation.

```json
{
  "ticker": "AAPL",
  "status": "success",
  "prediction": {
    "predicted_price": 244.07,
    "direction": "DOWN",
    "confidence": 0.99,
    "range": [239.71, 248.42]
  },
  "signal": {
    "action": "SELL",
    "strength": "STRONG",
    "confidence": 0.99,
    "reason": "Model predicts a downward move to $244.07..."
  },
  "explanation": "The RSI sits at 61.97, indicating...",
  "metadata": {
    "timestamp": "2026-04-28T17:16:36Z",
    "total_pipeline_ms": 10607.74,
    "step_timings_ms": {
      "data_agent": 3084.97,
      "feature_agent": 3.53,
      "ml_agent": 2.08,
      "signal_agent": 0.01,
      "explanation_agent": 7517.04
    }
  }
}
```

### `GET /api/stock/features?ticker=AAPL`

Returns engineered features (MA, RSI, MACD, Bollinger, volatility) for the last 60 trading days.

### `POST /api/chat`

Chat interface for follow-up questions about a ticker (placeholder).

### `GET /health`

Health check endpoint.

---

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 18+
- An [OpenRouter](https://openrouter.ai) API key

### 1. Clone and configure

```bash
git clone https://github.com/your-username/alpha-agent-ai.git
cd alpha-agent-ai

# Create environment file
echo 'OPENROUTER_API_KEY="your_key_here"' > .env
```

### 2. Train the ML model

```bash
cd backend
pip install -r requirements.txt
python3 -m app.models.train_model
```

### 3. Start the backend

```bash
cd backend
env $(cat ../.env | xargs) python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

### 5. Open the dashboard

Navigate to **http://localhost:3000**, enter a ticker (e.g. `AAPL`), and click **Analyze**.

### Docker (alternative)

```bash
docker-compose up --build -d
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000/docs
```

---

## Agent Responsibilities

| Agent | Role |
|-------|------|
| **Orchestrator** | Manages pipeline flow, tracks state, handles failures |
| **DataAgent** | Validates ticker, fetches OHLCV, checks data quality |
| **FeatureAgent** | Computes indicators, drops NaN rows, validates output columns |
| **MLAgent** | Runs XGBoost inference, validates prediction format |
| **SignalAgent** | Converts prediction to BUY/SELL/HOLD with strength tiers |
| **ExplanationAgent** | Constructs grounded prompt, calls LLM, returns analysis |

---
