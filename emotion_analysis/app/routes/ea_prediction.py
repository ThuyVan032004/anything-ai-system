from fastapi import APIRouter

from emotion_analysis.data.ea_data_cleaning import EATextDataCleaning
from emotion_analysis.data.helpers.text_data_cleaning_helper import TextDataCleaningHelper


ea_prediction_router = APIRouter(tags=["ea_online_serving"])

class EAOnlineServing:
    @staticmethod
    @ea_prediction_router.post("/predict")
    async def predict(input_text: str):
        from emotion_analysis.main import model_pipeline  # import global model
        
        ea_text_cleaner = EATextDataCleaning()
        cleaned_text = TextDataCleaningHelper.clean_text(text=input_text, cleaner=ea_text_cleaner)
        
        result = model_pipeline.predict([cleaned_text])
        
        return {"result": int(result[0])}