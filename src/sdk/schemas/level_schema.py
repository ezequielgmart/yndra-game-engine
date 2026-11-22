from pydantic import BaseModel
from typing import Any

class ComponentData(BaseModel):
    type: str
    data: dict[str, Any]

class EntityData(BaseModel):
    entity_id: int
    components: list[ComponentData]

class LayerData(BaseModel):
    entities: list[EntityData]

class LevelData(BaseModel):
    layers: dict[str, LayerData]