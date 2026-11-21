# Pyndra

> A Python-first 2D game engine built on an ECS core, with a modern, RPG Maker-inspired data
> editor and standalone `.exe` distribution.
>
> Working title — the name may change in the future.

---

## Table of Contents

- [Why This Project](#why-this-project)
- [What It Aims to Be](#what-it-aims-to-be)
- [Architecture Overview](#architecture-overview)
- [Key Technical Decisions](#key-technical-decisions)
- [Planned Features](#planned-features)
- [Project Status](#project-status)
- [Repository Structure (Planned)](#repository-structure-planned)
- [Documents](#documents)
- [License](#license)
- [Dependencies](#dependencies)

---

## Why This Project

The Python game-development ecosystem has a clear gap:

- **Pygame** and **Arcade** are great libraries, but they have **no built-in editor**.
- Engine-like tools such as **Ursina** are **3D** and not **ECS-editor-friendly**.
- **Godot** and **Unity** are excellent, but they are **not Python-first**.

There is room for a product that combines three things the Python ecosystem lacks together:

1. A **clean, ECS-oriented engine** written from scratch in Python.
2. A **modern, friendly data editor** (hierarchy, inspector, asset browser, static level
   viewport) inspired by RPG Maker.
3. **Standalone distribution**: games packaged as runnable `.exe` files.

The goal is to make it **easy and pleasant to build games in Python** without sacrificing good
engineering (composition over inheritance, data/logic separation) or developer experience.

---

## What It Aims to Be

A complete Python game engine and editor ecosystem:

- **Generic ECS core** written in Python (multi-purpose, not tied to 2D).
- **2D layer** on top of the core (transforms, sprites, camera, simple physics).
- **Raycasting layer** for Doom-style shooters (grid maps on top of the same ECS).
- **Runtime** that can be packaged as a distributable `.exe`.
- **Static data editor** inspired by RPG Maker: hierarchy, inspector, asset browser, and a
  viewport that paints the level statically (tiles, sprites, gizmos, grid) and edits JSON level
  and prefab files. The **Play** button launches a separate game process.

---

## Architecture Overview

The engine is split into a **single authoritative Python runtime** and a **web-tech data editor**
that edits JSON files and paints a static preview.

```
┌──────────────────────────────────────────────────────────────┐
│ RUNTIME (Python, pygame-ce)                                   │
│                                                               │
│  platform/         Platform, InputState, Game Loop, EventBus  │
│  render/           IRenderer + pygame-ce implementation        │
│  engine-core/      Pure ECS (no 2D, no rendering)             │
│  engine-2d/        Transform, Sprite, Camera, AABB physics    │
│  engine-raycast/   Grid maps, raycasting, player controller   │
│  engine-runtime/   game.py: load JSON, run the real game      │
│  engine-package/   Packaging to .exe (PyInstaller/Nuitka)     │
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
```

**Strengths of this design:**
- The **runtime is the single source of truth** for game behavior.
- The **editor never simulates**, only edits data and paints a static preview.
- The **contract is just JSON files + a spawned process** — simple and robust.
- The editor is **web-tech**: modern, fast, polished (key to attracting users).

---

## Key Technical Decisions

| # | Decision | Choice | Rationale |
|---|---|---|---|
| 1 | Editor model | **Static data editor**: paints levels statically, edits JSON | No embedded simulation; editor and runtime never diverge in logic |
| 2 | Rendering backend | **pygame-ce** | Large community, active maintenance, fast development, enough for a 2D tile RPG |
| 3 | Editor↔runtime contract | **JSON files + `subprocess.Popen`** | Simple, robust; JSON is the single contract |
| 4 | Platform support | **Cross-platform**, **Windows-first** | Consistent with the `.exe` distribution goal |
| 5 | Input model | **Polling + per-frame events** | Polling for continuous movement, events for "pressed once" actions |
| 6 | Abstractions | **Platform, IRenderer, InputState** | Keeps pygame-ce from locking the project in; enables future backend migration |
| 7 | Editor stack | **Electron + React + TypeScript + Tailwind + PixiJS** | Modern, fast UI; maximizes developer productivity |
| 8 | Distribution | **Packaged `.exe`** (PyInstaller / Nuitka) | Users run games without installing Python |
| 9 | License | **MPL-2.0** (engine/editor), LGPL-2.1 (pygame-ce) | File-level copyleft; commercial use allowed; LGPL is a secondary license |

Full details:
- [Architecture and vision decisions](./PROJECT_VISION.md)
- [Technical decisions](./TECHNICAL_DECISIONS.md)

---

## Planned Features

### Engine
- [ ] **EventBus**: generic publish/consume event system, independent of pygame.
- [ ] **Platform layer**: `Platform` + `InputState`, game loop with `dt`, frame-rate cap.
- [ ] **IRenderer**: backend-agnostic drawing interface with a pygame-ce implementation.
- [ ] **Input**: keyboard and mouse, both polling and per-frame events.
- [ ] **ECS core**: entities, components, systems, queries (composition over inheritance).
- [ ] **2D layer**: transforms, sprites, camera, simple AABB physics.
- [ ] **Raycasting layer**: grid-based maps and Doom-style renderer.
- [ ] **JSON format**: typed, versioned level and prefab files shared between editor and runtime.
- [ ] **Play**: launch a separate runtime process that loads the JSON.

### Editor
- [ ] **Scene hierarchy** panel.
- [ ] **Inspector** for editing component data (written to JSON).
- [ ] **Static 2D level viewport** (PixiJS) with tiles, sprites, gizmos, grid.
- [ ] **Play/Stop** launches/stops the separate pygame-ce runtime process.
- [ ] **Asset browser**, gizmos, drag & drop, undo/redo, multi-scene support.

### Distribution
- [ ] **`.exe` packaging** of games (validate PyInstaller/Nuitka).
- [ ] Bundled pygame-ce runtime (no system-wide install required).

---

## Project Status

**This project is in early development.** The roadmap and honest expectations are documented in
[PROJECT_VISION.md](./PROJECT_VISION.md).

High-level roadmap:

| Phase | Focus |
|---|---|
| **0 — Foundations** | Monorepo layout, JSON level/prefab format |
| **1 — Python ECS Core** | Entities, components, systems, queries (no rendering) |
| **2 — 2D Layer + Runtime** | Transforms, sprites, camera, physics, windowed/headless, `.exe` demo |
| **3 — Minimal Editor** | Hierarchy, inspector, static viewport, Play (spawn), JSON save/load |
| **4 — RPG Maker-Style Editor** | Asset browser, gizmos, drag & drop, undo/redo, multi-scene |
| **5 — Open-Source Polish** | Docs, examples, editor packaging, CI |

> **Reality check:** this is a large project — months, not weeks. It is worth it if the goal is
> to **build** an engine and editor (learning / product), not merely to make games quickly
> (for that, Godot is the rational choice).

---

## Repository Structure (Planned)

```
engine/platform/       # Platform, InputState, game loop, EventBus
engine/render/         # IRenderer + pygame-ce implementation
engine/core/           # Pure ECS: entities, components, systems, queries
engine/2d/             # Transform, Sprite, Camera, AABB physics
engine/raycast/        # Grid maps, raycasting, player controller
engine/runtime/        # game.py: load JSON, run the real game
engine/package/        # Packaging to .exe (PyInstaller/Nuitka)

editor/                # Electron + React + TypeScript + Tailwind + PixiJS
shared-schema/         # Typed, versioned JSON level/prefab format
```

---

## Documents

- [PROJECT_VISION.md](./PROJECT_VISION.md) — goal, architecture decision, problems, roadmap.
- [TECHNICAL_DECISIONS.md](./TECHNICAL_DECISIONS.md) — backend, editor model, events,
  licensing, MVP plan, and risks.

---

## License

This project's engine and editor code are licensed under the **Mozilla Public License 2.0
(MPL-2.0)**.

MPL-2.0 was chosen deliberately as a balance between openness and real-world usability:

- **Commercial use is encouraged.** Games and projects built with the engine may keep their
  own code closed — you are free to ship commercial, proprietary titles on top of the engine.
- **The core stays open.** Any improvements to the engine's own source files must remain open
  under MPL-2.0, so enhancements to the core flow back to the community.
- **File-level copyleft.** MPL-2.0 applies per source file rather than to the whole project,
  which keeps the engine open without "infecting" the user's game code.

In short: the engine is a commons that keeps improving, while creators stay free to build and
sell what they make with it.

See the [LICENSE](./LICENSE) file for the full license text.

---

## Dependencies

This engine uses **pygame-ce** as its runtime rendering and input library. **pygame-ce** is
distributed under the GNU Lesser General Public License, version 2.1 (LGPL-2.1).

- **pygame-ce** is used unmodified as an external, dynamically imported Python dependency.
- The original copyright and LGPL notices for pygame-ce are retained in the `LICENSE-LGPL` file
  (or in the pygame-ce package itself).
- Users are free to replace the installed pygame-ce package with a modified version, as required
  by the LGPL.
- This project's own code remains under the MPL-2.0. The LGPL applies only to the pygame-ce
  library itself.
- The project reserves **`IRenderer`** and **`Platform`** interfaces, so the rendering backend
  could be migrated (e.g. to PySDL2 or `pygame._sdl2`) in the future without affecting game code.

See the [LICENSE](./LICENSE) file for the full license text.