from typing import Optional
from pydantic import BaseModel

class DagDockerTaskConfigModel(BaseModel):
    task_id: str
    image: str
    api_version: Optional[str] = "auto"
    auto_remove: Optional[bool] = True
    command: str
    docker_url: str
    network_mode: str = "bridge"