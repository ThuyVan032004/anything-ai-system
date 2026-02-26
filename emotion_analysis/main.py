from fastapi import FastAPI
import uvicorn

from emotion_analysis.app.routes.ea_prediction import ea_prediction_router

from fastapi import APIRouter
import mlflow
from contextlib import asynccontextmanager
from fastapi import FastAPI

from emotion_analysis.common.constants import AppConstants

# Load model 1 lần duy nhất khi startup
model_pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_pipeline
    mlflow.set_tracking_uri(AppConstants.MLFLOW_TRACKING_URI)
    model_pipeline = mlflow.sklearn.load_model(model_uri="models:/emotion-analysis-xgboost/2")
    print(f"[INFO] Model loaded successfully: {model_pipeline}")
    yield
    # cleanup nếu cần

app = FastAPI(
    title="Emotion Analysis API",
    description="An API for analyzing emotions in text.",
    version="1.0.0",
    lifespan=lifespan
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.include_router(ea_prediction_router)

if __name__ == "__main__":
    uvicorn.run("emotion_analysis.main:app", host="localhost", port=8765, reload=False, workers=1)
