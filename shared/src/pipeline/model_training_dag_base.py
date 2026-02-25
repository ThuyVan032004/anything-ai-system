from abc import ABC

from airflow import DAG
from shared.src.pipeline.models.dag_model_training_build_model import DagModelTrainingBuildModel

from shared.src.pipeline.models.dag_config_model import DagConfigModel
from shared.src.pipeline.dag_base import DagBase


class ModelTrainingDagBase(DagBase, ABC):
    def __init__(self, configs: DagConfigModel):
        self.configs = configs
        
    def build(self, build_configs: DagModelTrainingBuildModel):
        with DAG(
            **self.configs.model_dump(exclude_none=True)
        ) as dag:
            if build_configs.data_extraction_task:
                data_extraction_task = self.create_docker_task(
                    build_configs.data_extraction_task
                )
            
            if build_configs.data_validation_task:
                data_validation_task = self.create_docker_task(
                    build_configs.data_validation_task
                )
            
            data_preparation_task = self.create_docker_task(
                build_configs.data_preparation_task
            )
            
            model_training_task = self.create_docker_task(
                build_configs.model_training_task
            )
            
            model_evaluation_task = self.create_docker_task(
                build_configs.model_evaluation_task
            )
            
            model_validation_task = self.create_docker_task(
                build_configs.model_validation_task
            )
            
            if build_configs.data_extraction_task and build_configs.data_validation_task:
                data_extraction_task >> data_validation_task >> data_preparation_task >> model_training_task >> model_evaluation_task >> model_validation_task
            elif build_configs.data_extraction_task and not build_configs.data_validation_task:
                data_extraction_task >> data_preparation_task >> model_training_task >> model_evaluation_task >> model_validation_task
            elif not build_configs.data_extraction_task and build_configs.data_validation_task:
                data_validation_task >> data_preparation_task >> model_training_task >> model_evaluation_task >> model_validation_task
            else:
                data_preparation_task >> model_training_task >> model_evaluation_task >> model_validation_task
            
        return dag