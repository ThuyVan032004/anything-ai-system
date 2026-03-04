# monitor.py
from dotenv import load_dotenv
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn
from emotion_analysis.app.routes.ea_monitor import ea_monitor_router, build_reference_features  # ← thêm import
from contextlib import asynccontextmanager
import mlflow
import os

from emotion_analysis.common.constants import AppConstants

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model pipeline để lấy vectorizer — cùng model với serving
    mlflow.set_tracking_uri(AppConstants.MLFLOW_TRACKING_URI)
    model_pipeline = mlflow.sklearn.load_model(model_uri="models:/emotion-analysis-xgboost/2")
    vectorizer = model_pipeline.named_steps["vectorizer"]

    # Build & cache reference features từ raw training data
    await build_reference_features(vectorizer)
    print("[INFO] Reference features built and cached.")
    yield

app = FastAPI(
    title="Emotion Analysis Monitoring Service",
    description="A service for monitoring data drift and model performance for Emotion Analysis",
    version="1.0.0",
    lifespan=lifespan,  # ← thêm
)

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

Instrumentator().instrument(app).expose(app)

app.include_router(ea_monitor_router)

# if __name__ == "__main__":
    # uvicorn.run("emotion_analysis.monitor:app", host="localhost", port=8769, reload=False, workers=1)