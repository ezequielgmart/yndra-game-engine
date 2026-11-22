import pygame

from typing import Any, Dict

class Render2DSystem:
    """
    Sistema encargado de manejar la renderización de las entidades en 2D.

    Atributos:
        screen: Superficie de la pantalla donde se dibujan las entidades.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Inicializa el sistema de renderizado.

        Args:
            screen: Superficie de Pygame para la renderización.
        """
        self.screen = screen

    def render(self, component_arrays: Dict[str, Any]) -> None:
        """
        Dibuja en pantalla todas las entidades que tengan componentes
        "render" y "transform".

        Args:
            component_arrays (dict): Arreglos de componentes agrupados por tipo.
        """
        render_components = component_arrays.get("render")
        transform_components = component_arrays.get("transform")

        if render_components and transform_components:
            for entity_id, render_component in render_components.items():
                transform_component = transform_components.get(entity_id)

                if transform_component:
                    for sprite in render_component.sprites:
                        self.screen.blit(sprite, (transform_component.x, transform_component.y))
