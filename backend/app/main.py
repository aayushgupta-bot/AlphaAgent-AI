from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import stock, predict, chat

app = FastAPI(title="AlphaAgent AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stock.router, prefix="/api/stock", tags=["Stock"])
app.include_router(predict.router, prefix="/api/predict", tags=["Predict"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
