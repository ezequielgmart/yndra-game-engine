from typing import Any, Dict, Optional, Type, TypeVar
from typing import Any, Dict

T = TypeVar("T")

class Entity:
    """
    Representa una entidad en el sistema ECS (Entity Component System).

    Atributos:
        id (int): Identificador único de la entidad.
        components (dict): Diccionario que asocia tipos de componentes con instancias de componentes.
    """

    def __init__(self, id:int):
        """
        Inicializa una entidad con un identificador único.

        Args:
            id (int): Identificador de la entidad.
        """
        self.id = id
        self.components: Dict[Type[Any], Any] = {}

    def add_component(self, component: Any) -> None:
        """
        Añade un componente a la entidad.

        Args:
            components: Instancia de un componente que se añadirá.
        """
        self.components[type(component)] = component

    def get_component(self, component_type: Type[T]) -> Optional[T]:
        """
        Obtiene un componente de un tipo específico.

        Args:
            component_type (type): Tipo del componente que se desea obtener.

        Returns:
            El componente si existe, de lo contrario, None.
        """
        return self.components.get(component_type)
