# PyECS Engine Core

---

## Overview

`PyECS Engine Core` is a lightweight and flexible foundational component for game development, built upon the Entity-Component-System (ECS) architectural pattern. It provides the essential structure for managing game entities, their attributes (components), and the logic that operates on them (systems), making it ideal for creating modular and scalable game projects.

This core component simplifies game logic by decoupling data from behavior, promoting reusability and maintainability. It includes core functionalities for loading level data from JSON files, managing entities with their associated components, and executing game loop and rendering systems.

---

## Features

* **Entity-Component-System (ECS) Architecture**: A robust foundation for building games, emphasizing composition over inheritance.
* **JSON-based Level Loading**: Easily define your game worlds, entities, and their components using declarative JSON files.
* **Dynamic Component Management**: Add and retrieve components from entities at runtime, allowing for flexible object definitions.
* **Pluggable Systems**: Implement custom game logic and rendering systems that operate on specific component types.
* **Dynamic Script Execution**: Load and execute Python scripts (behaviors) associated with entities, enabling custom logic for game objects.
* **Pygame Integration**: Includes a 2D rendering system compatible with Pygame surfaces for visual output.

---

## Getting Started

### Prerequisites

To run this engine core, you need:

* Python 3.x
* Pygame library

You can install Pygame using pip:

```bash
pip install pygame