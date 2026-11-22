class Transform:
    """
    Componente que define la posición 2D de una entidad.

    Atributos:
        x (int): Coordenada X.
        y (int): Coordenada Y.
        rotation (float): Rotación de la entidad en grados.
        scale (float): Factor de escala de la entidad.
    """
    def __init__(self, x:int, y:int, rotation:float, scale:float) -> None:
        """
        Args:
            x (int): Coordenada X inicial.
            y (int): Coordenada Y inicial.
            rotation (float): Rotación inicial en grados.
            scale (float): Factor de escala inicial.
        """
        self.x:int = x
        self.y:int = y
        self.rotation:float = rotation
        self.scale:float = scale