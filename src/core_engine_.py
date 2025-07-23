import json, pygame, os

import sys 
"""

Componente del motor para generar los datos principales que se necesita para que 
el juego funcione. 

algunos metodos que se puede utilizar a lo largo del motor

"""

def read_json_file(json_file):

    with open(json_file, "r") as f:
        data = json.load(f)

    return data


class Entity:
    """
    Representa una entidad en el sistema ECS (Entity Component System).

    Atributos:
        id (int): Identificador único de la entidad.
        components (dict): Diccionario que asocia tipos de componentes con instancias de componentes.
    """

    def __init__(self, id):
        """
        Inicializa una entidad con un identificador único.

        Args:
            id (int): Identificador de la entidad.
        """
        self.id = id
        self.components = {}

    def add_component(self, components):
        """
        Añade un componente a la entidad.

        Args:
            components: Instancia de un componente que se añadirá.
        """
        self.components[type(components)] = components

    def get_component(self, component_type):
        """
        Obtiene un componente de un tipo específico.

        Args:
            component_type (type): Tipo del componente que se desea obtener.

        Returns:
            El componente si existe, de lo contrario, None.
        """
        return self.components.get(component_type)


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
        self.level_data = {}
        self.entities = {}  # Usaremos un diccionario para almacenar las entidades por ID
        self.component_arrays = {}  # Diccionario para almacenar los arrays de componentes

    def load_level(self, level):
        """
        Carga los datos del nivel desde un archivo JSON.

        Args:
            level (str): Ruta al archivo JSON del nivel.
        """
        self.level_data.clear()
        self.entities.clear()
        self.component_arrays.clear()

        with open(level, "r") as file:
            datos = json.load(file)
            self.level_data = datos

        self.init_level_entities()

    def init_level_entities(self):
        """
        Inicializa las entidades definidas en el nivel, organizadas por capas (layers).
        """
        if 'layers' in self.level_data:  # Si el nivel tiene capas
            for layer_name, layer_data in self.level_data['layers'].items():
                if 'entities' in layer_data:
                    for entity_data in layer_data['entities']:
                        self.process_entity_data(entity_data)

    def process_entity_data(self, entity_data):
        """
        Procesa los datos de una entidad, crea instancias y registra sus componentes.

        Args:
            entity_data (dict): Datos de la entidad como su ID y componentes.
        """
        entity_id = entity_data['entity_id']
        entity = Entity(entity_id)
        self.entities[entity_id] = entity  # Almacenar la entidad por ID

        for component_data in entity_data['components']:
            component_type = component_data['type'].lower()  # Convertir a minúscula para evitar problemas
            component_values = component_data['data']

            # Crear el componente dinámicamente
            component_class = globals().get(component_type.capitalize())  # Capitalize to match class names
            if component_class:
                component = component_class(**component_values)
                entity.add_component(component)

                # Almacenar el componente en el array correspondiente
                if component_type not in self.component_arrays:
                    self.component_arrays[component_type] = {}
                self.component_arrays[component_type][entity_id] = component
            else:
                print(f"Warning: Component class '{component_type.capitalize()}' not found.")

    def onUpdate(self):
        behaviours = self.component_arrays.get("behaviour")

        if behaviours:
            for entity_id, behaviour in behaviours.items():
                entity = self.entities.get(entity_id)
                if entity:
                    for script_data in behaviour.data["scripts"]:
                        script_path = script_data["path"]
                        script_module_name = script_data["module"]

                        try:
                            # Asegúrate de que el módulo esté en el PYTHONPATH
                            sys.path.append(os.path.dirname(script_path))

                            # Importar el módulo dinámicamente
                            module = __import__(script_module_name)

                            # Obtener la clase del script desde el módulo
                            script_class = getattr(module, script_module_name)
                            script_instance = script_class(entity)

    # Confirmar que se ejecuta el método update()
                            print(f"Executing update for entity ID {entity_id}")
                            script_instance.update(pygame.event.get())

                            # Llamar al método update
                            script_instance.update(pygame.event.get())

                        except ImportError:
                            print(f"on update function -> Warning: Script module '{script_module_name}' not found.")
                        except AttributeError:
                            print(f"on update function -> Warning: Script class '{script_module_name}' not found in module '{script_module_name}'.")


class Render2DSystem:
    """
    Sistema encargado de manejar la renderización de las entidades en 2D.

    Atributos:
        screen: Superficie de la pantalla donde se dibujan las entidades.
    """

    def __init__(self, screen):
        """
        Inicializa el sistema de renderizado.

        Args:
            screen: Superficie de Pygame para la renderización.
        """
        self.screen = screen

    def render(self, entities, component_arrays):
            render_components = component_arrays.get("render")
            position_components = component_arrays.get("position")

            if render_components and position_components:
                for entity_id, render_component in render_components.items():
                    position_component = position_components.get(entity_id)

                    if position_component:
                        for sprite in render_component.sprites:
                            self.screen.blit(sprite, (position_component.x, position_component.y))


# Components
class Position:
    """
    Componente que define la posición 2D de una entidad.

    Atributos:
        x (int): Coordenada X.
        y (int): Coordenada Y.
    """
    def __init__(self, x, y, rotation, scale):
        """
        Args:
            x (int): Coordenada X inicial.
            y (int): Coordenada Y inicial.
        """
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale = scale


class Render:
    """
    Componente que define los elementos gráficos de una entidad.

    Atributos:
        sprites (list): Lista de superficies gráficas asociadas a la entidad.
    """
    def __init__(self, sprites, width, height):
        """
        Args:
            sprites (str): Ruta del archivo de imagen para renderizar.
        """
        self.sprites = [pygame.image.load(sprites).convert_alpha()]
        self.width = width
        self.height = height


class Behaviour:
    """
    Componente que gestiona los comportamientos dinámicos de la entidad.

    Atributos:
        data (dict): Diccionario con datos sobre los scripts y comportamientos asociados.
    """
    def __init__(self, **kwargs):
        """
        Args:
            kwargs: Datos dinámicos sobre los scripts y configuraciones del comportamiento.
        """
        self.data = kwargs