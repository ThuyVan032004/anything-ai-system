# from shared.src.pipeline.models.dag_config_model import DagConfigModel
# from shared.src.pipeline.models.dag_stream_build_model import DagStreamBuildModel
# from shared.src.pipeline.stream_dag_base import StreamDagBase


# class EAStreamDag(StreamDagBase):
#     def __init__(self, configs: DagConfigModel):
#         super().__init__(configs)
        
#     def build(self, build_configs: DagStreamBuildModel):
#         return super().build(build_configs)
    
# ea_stream_dag_configs = DagConfigModel(
#     dag_id="ea_stream_dag"
# )

# ea_stream_dag = EAStreamDag(ea_stream_dag_configs)
# built_ea_stream_dag = ea_stream_dag.build()