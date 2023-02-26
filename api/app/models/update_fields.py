from pydantic import BaseModel
import typing as t

class UpdateFieldModel(BaseModel):
    field: str
    value: t.Union[float, str, int]