from typing import Any, Dict, Optional

from ..entities.entity import Entity


class Scene: 

    """
        Holds every entity and component loaded from a level file, and provides
        runtime lookup of entities by id.

        Attributes:
            level_data (dict): Raw level data loaded from JSON.
            entities (dict): Active entities keyed by their id.
            component_arrays (dict): Component instances grouped by type and id.
    """
    
    def __init__(self) -> None:
        self.level_data: Dict[str, Any] = {}
        self.entities: Dict[str, Entity] = {} # now this is safely typed, 
        self.component_arrays: Dict[str, Dict[str, Any]] = {}


    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """
        Returns the entity with the given id, or None if it does not exist.

        Args:
            entity_id: Unique identifier of the entity.

        Returns:
            The matching Entity instance, or None.
        """
        return self.entities.get(entity_id)