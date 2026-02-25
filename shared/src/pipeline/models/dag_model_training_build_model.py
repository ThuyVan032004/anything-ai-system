from typing import Optional
from pydantic import BaseModel
from shared.src.pipeline.models.dag_docker_task_config_model import DagDockerTaskModel


class DagModelTrainingBuildModel(BaseModel):
    data_extraction_task: Optional[DagDockerTaskModel] = None
    data_validation_task: Optional[DagDockerTaskModel] = None
    data_preparation_task: DagDockerTaskModel
    model_training_task: DagDockerTaskModel
    model_evaluation_task: DagDockerTaskModel
    model_validation_task: DagDockerTaskModel