from src.pipeline.dag_base import DagBase
from src.pipeline.models.dag_config_model import DagConfigModel
from airflow import DAG
from src.pipeline.models.dag_stream_build_model import DagStreamBuildModel


class StreamDagBase(DagBase):
    def __init__(self, configs: DagConfigModel):
        self.configs = configs
        
    def build(self, build_configs: DagStreamBuildModel):
        with DAG(
            **self.configs.model_dump()
        ) as dag:
            stream_to_online_task = self.create_docker_task(
                **build_configs.stream_to_online_task.model_dump()
            )
            
            stream_to_offline_task = self.create_docker_task(
                **build_configs.stream_to_offline_task.model_dump()
            )
            
        return dag