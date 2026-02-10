from pydantic import BaseModel
from shared.src.pipeline.models.dag_docker_task_config_model import DagDockerTaskConfigModel


class DagStreamBuildModel(BaseModel):
    stream_to_online_task: DagDockerTaskConfigModel
    stream_to_offline_task: DagDockerTaskConfigModel