from abc import abstractmethod
from airflow import DAG
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from shared.src.pipeline.models.dag_docker_task_config_model import DagDockerTaskModel
from shared.src.pipeline.interfaces.i_dag import IDag


class DagBase(IDag):
    def create_docker_task(self, docker_configs: DagDockerTaskModel):
        config_dict = docker_configs.model_dump(exclude_none=True)
        
        config_dict["environment"] = {
            "AWS_S3_BUCKET": Variable.get("AWS_S3_BUCKET"),
            "AWS_ACCESS_KEY_ID": Variable.get("AWS_ACCESS_KEY_ID"),
            "AWS_SECRET_ACCESS_KEY": Variable.get("AWS_SECRET_ACCESS_KEY"),
            "MLFLOW_TRACKING_URI": "http://mlflow:5000",
            "MLFLOW_ARTIFACT_UPLOAD_DOWNLOAD_TIMEOUT": "300",
            "MLFLOW_ARTIFACT_URI": "mlflow-artifacts:/",  # ✅ Client-side override
        }
        
        # Join the shared network so containers can resolve 'mlflow' hostname
        config_dict["network_mode"] = "shared-network"
        
        return DockerOperator(**config_dict)