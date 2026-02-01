from abc import abstractmethod
from airflow import DAG
from shared.src.pipeline.interfaces.i_dag import IDag
from shared.src.pipeline.models.dag_config_model import DagConfigModel


class DagBase(IDag):
    def __init__(self, configs: DagConfigModel):
        self.configs = configs
    
    def build(self):
        config_dict = self.configs.model_dump()
        
        with DAG(**config_dict) as dag:
            self.define_tasks(dag)
        return dag
            
    
    @abstractmethod
    def define_tasks(self, dag: DAG):
        pass