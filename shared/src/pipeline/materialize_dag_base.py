from abc import ABC
from airflow import DAG
from src.pipeline.dag_base import DagBase
from src.pipeline.models.dag_config_model import DagConfigModel
from src.pipeline.models.dag_materialize_build_model import DagMaterializeBuildModel


class MaterializeDagBase(DagBase, ABC):
    def __init__(self, configs: DagConfigModel):
        self.configs = configs
        
    def build(self, build_configs: DagMaterializeBuildModel):
        with DAG(
            **self.configs.model_dump()
        ) as dag:
            materialize_task = self.create_docker_task(
                **build_configs.model_dump()
            )
            
        return dag