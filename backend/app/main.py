from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import stock, predict, chat

# Initialize FastAPI application with basic metadata (title & version)
app = FastAPI(title="AlphaAgent AI", version="1.0.0")

# Enable CORS middleware to allow frontend (e.g., Next.js) to communicate with backend APIs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers for modular endpoints: stock data, predictions, and chat functionality
app.include_router(stock.router, prefix="/api/stock", tags=["Stock"])
app.include_router(predict.router, prefix="/api/predict", tags=["Predict"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
def read_root():
    return {"message": "AlphaAgent AI Backend is running. Access /docs for the API."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
