from airflow import DAG
from src.pipeline.dag_base import DagBase
from src.pipeline.models.dag_config_model import DagConfigModel
from src.pipeline.models.dag_docker_task_config_model import DagDockerTaskConfigModel


class MaterializeDagBase(DagBase):
    def __init__(self, configs: DagConfigModel):
        self.configs = configs
        
    def build(self, build_configs: DagDockerTaskConfigModel):
        with DAG(
            **self.configs.model_dump()
        ) as dag:
            materialize_task = self.create_docker_task(
                **build_configs.model_dump()
            )
            
        return dag