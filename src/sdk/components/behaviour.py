from typing import Any, Dict


class Behaviour:
    """
    Componente que gestiona los comportamientos dinámicos de la entidad.

    Atributos:
        data (dict): Diccionario con datos sobre los scripts y comportamientos asociados.
        instances (dict): Cached script instances, keyed by module name, so their
            state persists across frames instead of being recreated every frame.
    """

    def __init__(self, **kwargs: Any) -> None:
        """
        Args:
            kwargs: Datos dinámicos sobre los scripts y configuraciones del comportamiento.
        """
        self.data: Dict[str, Any] = kwargs
        self.instances: Dict[str, Any] = {}