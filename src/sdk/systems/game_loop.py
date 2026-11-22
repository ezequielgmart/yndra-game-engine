from ..entities.entity import Entity
from ..utils.os_utils import OsHandler
from ..utils.config import COMPONENT_REGISTRY

from typing import Any, Dict, List

import pygame

class GameLoopSystem:
    """
    Sistema principal para manejar el bucle del juego, incluyendo la gestión de niveles y entidades.

    Atributos:
        level_data (dict): Datos del nivel actual cargado.
        entities (dict): Entidades activas en el juego identificadas por ID.
        component_arrays (dict): Diccionario que almacena arreglos de componentes agrupados por tipo.
    """

    def __init__(self):
        """
        Inicializa el sistema de bucle de juego.
        """
        self.level_data: Dict[str, Any] = {}
        self.entities: Dict[str, Any] = {}
        self.component_arrays: Dict[str, Any] = {}
        self.os_handler: OsHandler = OsHandler()

    def load_level(self, level:str) -> None:
        """
        Carga los datos del nivel desde un archivo JSON.

        Args:
            level (str): Ruta al archivo JSON del nivel.
        """
        self.level_data.clear()
        self.entities.clear()
        self.component_arrays.clear()

        self.level_data = self.os_handler.read_json_file(level)

        self.init_level_entities()

        return None

    def init_level_entities(self) -> None:

        layers: Dict[str, Dict[str, Any]] = self.level_data.get('layers', {})

        for layer_data in layers.values():
            entities = layer_data.get('entities', [])
            for entity_data in entities:
                self.process_entity_data(entity_data)


    def process_entity_data(self, entity_data: Dict[str, Any]) -> None:
        """
        Procesa los datos de una entidad, crea instancias y registra sus componentes.

        El tipo de componente que viene en el JSON se busca en COMPONENT_REGISTRY.
        La clave usada en component_arrays se normaliza siempre a minúsculas para
        que coincida de forma intencional con las claves que usan los sistemas
        (por ejemplo, "transform", "render", "behaviour").

        Args:
            entity_data (dict): Datos de la entidad como su ID y componentes.
        """
        entity_id = entity_data['entity_id']
        entity = Entity(entity_id)
        self.entities[entity_id] = entity  # Almacenar la entidad por ID

        for component_data in entity_data['components']:
            component_type = component_data['type'].lower()  # Clave normalizada y consistente
            component_values = component_data['data']

            # Resolver la clase del componente a través del registro explícito
            component_class = COMPONENT_REGISTRY.get(component_type)
            if component_class:
                component = component_class(**component_values)
                entity.add_component(component)

                # Almacenar el componente en el array correspondiente
                if component_type not in self.component_arrays:
                    self.component_arrays[component_type] = {}
                self.component_arrays[component_type][entity_id] = component
            else:
                print(f"Warning: Component type '{component_type}' is not registered in COMPONENT_REGISTRY.")

    def onUpdate(self, events: List[pygame.event.Event]) -> None:
        """
        Runs the update() method of every entity behaviour script.

        Script instances are created only once and cached on the Behaviour
        component, so their internal state (timers, velocity, etc.) persists
        across frames instead of being reset every frame.

        Args:
            events: pygame events already polled once per frame by the engine.
                They are forwarded to every script so the event queue is not
                consumed multiple times.
        """
        behaviours = self.component_arrays.get("behaviour")
        if not behaviours:
            return

        for entity_id, behaviour in behaviours.items():
            entity = self.entities.get(entity_id)
            if not entity:
                continue

            scripts = behaviour.data.get("scripts", [])

            for script_data in scripts:
                script_path = script_data["path"]
                script_module_name = script_data["module"]

                try:
                    self.os_handler.check_script_is_on_pythonpath(script_path)

                    # Create the instance only once and cache it on the Behaviour
                    script_instance = behaviour.instances.get(script_module_name)
                    if script_instance is None:
                        module = __import__(script_module_name)
                        script_class = getattr(module, script_module_name)
                        script_instance = script_class(entity)
                        behaviour.instances[script_module_name] = script_instance

                    # Always update the same instance so its state persists
                    script_instance.update(events)

                except ImportError:
                    print(f"on update function -> Warning: Script module '{script_module_name}' not found.")
                except AttributeError:
                    print(f"on update function -> Warning: Script class '{script_module_name}' not found in module '{script_module_name}'.")