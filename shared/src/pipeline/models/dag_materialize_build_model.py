from pydantic import BaseModel
from src.pipeline.models.dag_docker_task_config_model import DagDockerTaskModel


class DagMaterializeBuildModel(BaseModel):
    materialize_task: DagDockerTaskModel