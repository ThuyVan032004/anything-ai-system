from abc import abstractmethod
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from src.pipeline.models.dag_docker_task_config_model import DagDockerTaskConfigModel
from shared.src.pipeline.interfaces.i_dag import IDag
from shared.src.pipeline.models.dag_config_model import DagConfigModel


class DagBase(IDag):
    def create_docker_task(self, docker_configs: DagDockerTaskConfigModel):
        return DockerOperator(**docker_configs.model_dump())