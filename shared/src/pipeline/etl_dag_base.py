from airflow import DAG
from src.pipeline.dag_base import DagBase
from src.pipeline.models.dag_config_model import DagConfigModel
from src.pipeline.models.dag_etl_build_model import DagETLBuildModel


class ETLDagBase(DagBase):
    def __init__(self, configs: DagConfigModel):
        self.configs = configs
        
    def build(self, build_configs: DagETLBuildModel):
        with DAG(
            **self.configs.model_dump()
        ) as dag:
            ingest_task = self.create_docker_task(
                **build_configs.ingest_task.model_dump()
            )
            
            clean_task = self.create_docker_task(
                **build_configs.clean_task.model_dump()
            )
            
            explore_and_validate_task = self.create_docker_task(
                **build_configs.explore_and_validate_task.model_dump()
            )
            
            ingest_task >> clean_task >> explore_and_validate_task
        
        return dag
        
        
    
    