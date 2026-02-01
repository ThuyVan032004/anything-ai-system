from pydantic import BaseModel


class TagModel(BaseModel):
    key: str
    value: str