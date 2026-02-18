from typing import Dict, Optional
from pydantic import BaseModel

class DagDockerTaskModel(BaseModel):
    task_id: str
    image: str
    api_version: Optional[str] = "auto"
    auto_remove: Optional[str] = "force"
    command: str
    docker_url: Optional[str] = "tcp://airflow-docker-proxy:2375"
    network_mode: str = "bridge"
    mount_tmp_dir: Optional[bool] = False
    environment: Optional[Dict[str, str]] = None
    