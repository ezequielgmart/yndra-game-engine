# Project Vision — A Python-First Game Engine with an RPG Maker-Style Data Editor

> **Goal:** An open-source 2D game engine written in Python, with a modern, RPG Maker-inspired
> **data editor** (hierarchy, inspector, asset browser, static level viewport), whose games can
> be packaged as standalone `.exe` files.

---

## 1. What This Project Is

A game engine and editor for the Python ecosystem:

- **Generic ECS core** written in Python (multi-purpose, not tied to 2D).
- **2D layer** on top of the core (transforms, sprites, camera, simple physics).
- **Runtime** that can be packaged as a distributable `.exe`.
- **Modern, friendly data editor** inspired by RPG Maker: hierarchy, inspector, asset browser,
  and a viewport that paints the level statically and edits JSON files.

The core idea is a **"RPG Maker-style editor but Python-first, built with web tech"**. This is a
real gap in the current ecosystem: engines like Pygame and Arcade have no built-in editor,
engine-like tools such as Ursina are 3D and not ECS-editor-friendly, and Godot is not
Python-first. There is room for a product in this space.

---

## 2. Core Architecture Decision (The One That Defines Everything)

The single most important decision is **how the editor relates to the game runtime**.

We deliberately **do NOT** embed a simulation in the editor, and we do **NOT** stream state at
60 Hz. Instead, we split the project into two clearly separated pieces connected **only by JSON
files and a spawned process**:

- The **editor is a static data editor**. It paints the level statically (tiles, sprites,
  gizmos, grid) and edits **JSON level and prefab files**. It has its hierarchy, inspector,
  asset browser, and level editor — but it does **not** run game logic.
- The **Play** button launches a **separate Python process** (`game.py` or the packaged
  executable) that loads the JSON and runs the **real game with pygame-ce**.
- There is **no embedded simulation**, **no state IPC**, and **no 60 Hz streaming**.
- There is **no hot reload** of user code: the game is **relaunched**.

### Why this model

Two engines that simulate separately (JS in the editor, Python in the game) **diverge over
time**: games eventually "work in the editor but not in the `.exe`". Here the editor **never
simulates** — it only edits data and draws a static preview — so there is no second simulation
to diverge. What Play runs is exactly the real game.

### The JSON contract is the pillar

Since the editor↔runtime contract reduces to **JSON files + `subprocess.Popen`**, **scene
serialization becomes the central pillar of the project**. The project's JSON format is the
**only contract** between editor and runtime, so it must be typed, versioned, and treated as a
core deliverable from day one.

### Rejected approaches

| Approach | Why rejected |
|---|---|
| **Stream frames from Python to the editor** | Adds latency and CPU cost; no longer needed since the editor only paints statically. |
| **Editor simulates in JS (Pixi) only** | Two implementations of the engine → behavior divergence. |
| **Embed a native Python window in Electron** | Fragile and platform-specific; unneeded with the data-editor model. |
| **Embedded simulation / state IPC at 60 Hz** | Removed: the contract is just JSON + process spawn. |

---

## 3. Stack

```
┌──────────────────────────────────────────────────────────────┐
│ RUNTIME (Python, pygame-ce)                                   │
│                                                               │
│  engine-core/       Pure ECS (no 2D, no rendering)            │
│  engine-2d/         Transform, Sprite, Camera, AABB physics   │
│  engine-runtime/    game.py: load JSON, run the real game     │
│  engine/platform/   Platform, InputState, loop, EventBus      │
│  engine/render/     IRenderer + pygame-ce implementation       │
│  engine-package/    Packaging to .exe (PyInstaller/Nuitka)    │
└──────────────────────────────────────────────────────────────┘
                            ▲
                            │ JSON level/prefab files
                            │ + subprocess.Popen (Play)
                            ▼
┌──────────────────────────────────────────────────────────────┐
│ EDITOR (Electron + React + TypeScript + Tailwind)             │
│  - Static data editor (no simulation)                         │
│  - Hierarchy, Inspector, Asset browser                        │
│  - Viewport (PixiJS): paints tiles, sprites, gizmos, grid     │
│  - Play: spawns the runtime process, captures stdout/stderr   │
│  - Projects: typed, versioned JSON levels and prefabs         │
└──────────────────────────────────────────────────────────────┘