import pygame

from typing import Any, Dict, List

from .sdk.systems.game_loop import GameLoopSystem
from .sdk.systems.render2d_system import Render2DSystem

class Engine: 

    """    
        Orchestrates the main game loop, wiring together the ECS game loop
        system and the 2D rendering system on top of a pygame window.

        Attributes:
            screen (pygame.Surface): Surface where the game is drawn.
            clock (pygame.time.Clock): Clock used to limit the frame rate.
            game_loop (GameLoopSystem): System that loads levels and updates behaviours.
            render_system (Render2DSystem): System that draws renderable entities.
            fps (int): Maximum frames per second.
    
    """

    def __init__(
        self, 
        screen: pygame.Surface,
        level_path: str, 
        clear_color: str = "Black", 
        fps: int = 60

    )-> None: 

        self.screen: pygame.Surface = screen 
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.clear_color: str = clear_color
        self.fps: int = fps

        self.game_loop: GameLoopSystem = GameLoopSystem()
        self.game_loop.load_level(level_path)

        self.render_system: Render2DSystem = Render2DSystem(self.screen)

        self._running: bool = True


    def run(self) -> None: 
        """
        Runs the main loop until the window is closed.

        Each frame: polls events once, handles quit, clears the screen,
        updates behaviours (forwarding the same events), renders, flips
        the display and limits the FPS.
        """

        while self._running: 

            # Poll the event queue exactly once per frame

            events: List[pygame.event.Event] = pygame.event.get()

            for event in events: 

                if event.type == pygame.QUIT: 

                    self._running = False

            # Wipe the previous frame
            self.screen.fill(self.clear_color)

            # update behaviurs with the same events (single source of truth)
            self.game_loop.onUpdate(events)


            # Render entities that have both render and transform components 
            component_arrays: Dict[str, Any] = self.game_loop.component_arrays
            
            self.render_system.render(component_arrays)

            # Put the work on screen
            pygame.display.flip()

            # Limit the frame rate
            self.clock.tick(self.fps)

