from typing import Dict, Optional
from pydantic import BaseModel


class TabularDataPreparationConfigModel(BaseModel):
    saved_training_file_name: str
    saved_validation_file_name: str
    saved_test_file_name: str
    split_ratios: Optional[Dict[str, float]] = {
        "validation_and_test": 0.2,
        "test": 0.5
    }