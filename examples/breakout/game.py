import os
import sys

import pygame

# Make the repository root importable so `src` resolves regardless of cwd.
_REPO_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

# Work from this example's directory so relative asset/scene paths resolve.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from src.engine import Engine  # noqa: E402  (import after sys.path setup)


def main() -> None:
    """Entry point for the breakout example."""
    pygame.init()

    width: int = 800
    height: int = 600
    screen: pygame.Surface = pygame.display.set_mode((width, height))

    engine: Engine = Engine(screen, "scenes/level1.json")
    engine.run()

    pygame.quit()


if __name__ == "__main__":
    main()