from pydantic import BaseModel
from shared.src.pipeline.models.dag_docker_task_config_model import DagDockerTaskConfigModel


class DagETLBuildModel(BaseModel):
    ingest_task: DagDockerTaskConfigModel
    clean_task: DagDockerTaskConfigModel
    explore_and_validate_task: DagDockerTaskConfigModel