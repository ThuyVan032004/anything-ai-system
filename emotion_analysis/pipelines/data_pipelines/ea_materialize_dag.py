# from shared.src.pipeline.materialize_dag_base import MaterializeDagBase
# from shared.src.pipeline.models.dag_config_model import DagConfigModel
# from shared.src.pipeline.models.dag_docker_task_config_model import DagDockerTaskModel


# class EAMaterializeDag(MaterializeDagBase):
#     def __init__(self, configs: DagConfigModel):
#         super().__init__(configs)
        
#     def build(self, build_configs: DagDockerTaskModel):
#         return super().build(build_configs)
    


# ea_materialize_dag_configs = DagConfigModel(
#     dag_id="ea_materialize_dag"
# )

# ea_materialize_dag = EAMaterializeDag(ea_materialize_dag_configs)
# built_ea_materialize_dag = ea_materialize_dag.build()