
import pygame
from typing import List
from src.sdk.entities.entity import Entity
from src.sdk.components.transform import Transform

class MainGameLoopHandle:
    def __init__(self, entity: Entity) -> None:
        self.entity = entity

        self.transform = self.entity.get_component(Transform)
      

    def update(self, events: List[pygame.event.Event]) -> None:

        self.transform.x =+ 5  

