from typing import Dict

from emotion_analysis.common.constants import AppConstants

    
class EAModelValidationHelper:
    @staticmethod
    def validate_model_with_thresholds(configs: Dict[str, float | int]) -> bool:
        model_accuracy = configs["accuracy"]
        model_precision_weighted = configs["precision_weighted"]
        model_recall_weighted = configs["recall_weighted"]
        model_f1_score_weighted = configs["f1_score_weighted"]
        
        accuracy_threshold = AppConstants.MODEL_VALIDATION_THRESHOLDS["accuracy"]
        precision_weighted_threshold = AppConstants.MODEL_VALIDATION_THRESHOLDS["precision_weighted"]
        recall_weighted_threshold = AppConstants.MODEL_VALIDATION_THRESHOLDS["recall_weighted"]
        f1_score_weighted_threshold = AppConstants.MODEL_VALIDATION_THRESHOLDS["f1_score_weighted"]
        
        is_pass_accuracy = model_accuracy >= accuracy_threshold
        is_pass_precision_weighted = model_precision_weighted >= precision_weighted_threshold
        is_pass_recall_weighted = model_recall_weighted >= recall_weighted_threshold
        is_pass_f1_score_weighted = model_f1_score_weighted >= f1_score_weighted_threshold
        
        is_pass = is_pass_accuracy and is_pass_precision_weighted and is_pass_recall_weighted and is_pass_f1_score_weighted
        
        return {
            "result": is_pass,
            "details": {
                "accuracy": {
                    "model_value": model_accuracy,
                    "threshold": accuracy_threshold,
                    "is_pass": is_pass_accuracy
                },
                "precision_weighted": {
                    "model_value": model_precision_weighted,
                    "threshold": precision_weighted_threshold,
                    "is_pass": is_pass_precision_weighted
                },
                "recall_weighted": {
                    "model_value": model_recall_weighted,
                    "threshold": recall_weighted_threshold,
                    "is_pass": is_pass_recall_weighted
                },
                "f1_score_weighted": {
                    "model_value": model_f1_score_weighted,
                    "threshold": f1_score_weighted_threshold,
                    "is_pass": is_pass_f1_score_weighted
                }
            }
        }
