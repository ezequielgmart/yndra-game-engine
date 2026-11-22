
from ..components.transform import Transform
from ..components.behaviour import Behaviour
from ..components.render2d import Render2D

from typing import Any, Dict

# Registro explícito de componentes.
# Mapea el "type" que viene en el JSON (normalizado a minúsculas) a su clase.
# Se define aquí, después de las clases, para asegurar que existan en el momento
# de construir el diccionario.
COMPONENT_REGISTRY: Dict[str, Any] = {
    "transform": Transform,
    "render": Render2D,
    "behaviour": Behaviour,
}
