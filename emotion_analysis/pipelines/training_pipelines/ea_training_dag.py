from emotion_analysis.pipelines.configs.ea_dag_build_configs import EADagBuildConfigs
from shared.src.pipeline.models.dag_config_model import DagConfigModel
from shared.src.pipeline.model_training_dag_base import ModelTrainingDagBase


class EATrainingDag(ModelTrainingDagBase):
    def __init__(self, configs):
        super().__init__(configs)
        
    def build(self, build_configs):
        return super().build(build_configs)
    
ea_training_dag_configs = DagConfigModel(
    dag_id = "ea_training_dag"
)

ea_training_dag = EATrainingDag(ea_training_dag_configs)
dag = ea_training_dag.build(build_configs=EADagBuildConfigs.EA_TRAINING_DAG_BUILD_CONFIGS)