from pydantic import BaseModel
from shared.src.pipeline.models.dag_docker_task_config_model import DagDockerTaskModel


class DagETLBuildModel(BaseModel):
    # ingest_task: DagDockerTaskModel
    clean_task: DagDockerTaskModel
    explore_and_validate_task: DagDockerTaskModel