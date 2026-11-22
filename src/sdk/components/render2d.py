
import pygame 

class Render2D:
    """
    Componente que define los elementos gráficos de una entidad.

    Atributos:
        sprites (list): Lista de superficies gráficas asociadas a la entidad.
        width (int): Ancho del sprite.
        height (int): Alto del sprite.
    """
    
    def __init__(self, sprite_path: str, width: int, height: int) -> None:
        """
        Args:
            sprites list[pygame.Surface]: Ruta del archivo de imagen para renderizar.
            width (int): Ancho del sprite.
            height (int): Alto del sprite.
        """
        self.sprites: list[pygame.Surface] = [
            pygame.image.load(sprite_path).convert_alpha()
        ]
        self.width = width
        self.height = height