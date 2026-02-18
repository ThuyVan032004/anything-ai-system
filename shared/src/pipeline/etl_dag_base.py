from airflow import DAG
from abc import ABC
from shared.src.pipeline.dag_base import DagBase
from shared.src.pipeline.models.dag_config_model import DagConfigModel
from shared.src.pipeline.models.dag_etl_build_model import DagETLBuildModel


class ETLDagBase(DagBase, ABC):
    def __init__(self, configs: DagConfigModel):
        self.configs = configs
        
    def build(self, build_configs: DagETLBuildModel):
        with DAG(
            **self.configs.model_dump(exclude_none=True)
        ) as dag:
            # ingest_task = self.create_docker_task(
            #     **build_configs.ing est_task.model_dump()
            # )
            
            clean_task = self.create_docker_task(
                build_configs.clean_task
            )
            
            explore_and_validate_task = self.create_docker_task(
                build_configs.explore_and_validate_task
            )
            
            # ingest_task >> 
            clean_task >> explore_and_validate_task
        
        return dag
        
        
    
    