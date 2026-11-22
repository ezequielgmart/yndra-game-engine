import  pygame 

"""

Componente del motor para generar los datos principales que se necesita para que 
el juego funcione. 

algunos metodos que se puede utilizar a lo largo del motor

"""







 



# Components
class Position:
    """
    Componente que define la posición 2D de una entidad.

    Atributos:
        x (int): Coordenada X.
        y (int): Coordenada Y.
        rotation (float): Rotación de la entidad en grados.
        scale (float): Factor de escala de la entidad.
    """
    def __init__(self, x, y, rotation, scale):
        """
        Args:
            x (int): Coordenada X inicial.
            y (int): Coordenada Y inicial.
            rotation (float): Rotación inicial en grados.
            scale (float): Factor de escala inicial.
        """
        self.x = x
        self.y = y
        self.rotation = rotation
        self.scale = scale






