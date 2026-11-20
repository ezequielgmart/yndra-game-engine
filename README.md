# Pyndra

> A Python-first 2D game engine built on an ECS core, with a modern, Unity-inspired editor and
> standalone `.exe` distribution.
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

---

## Why This Project

The Python game-development ecosystem has a clear gap:

- **Pygame** and **Arcade** are great libraries, but they have **no built-in editor**.
- Engine-like tools such as **Ursina** are **3D** and not **ECS-editor-friendly**.
- **Godot** and **Unity** are excellent, but they are **not Python-first**.

There is room for a product that combines three things the Python ecosystem lacks together:

1. A **clean, ECS-oriented engine** written from scratch in Python.
2. A **modern, friendly editor** (hierarchy, inspector, level editing, viewport with Play)
   inspired by Unity.
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
- **Modern, friendly editor** inspired by Unity: scene hierarchy, inspector, level editing,
  asset browser, and a viewport with a Play button.

---

## Architecture Overview

The engine is split into a **single authoritative Python core** and a **web-tech editor** that
only paints the state the core sends.

```
┌──────────────────────────────────────────────────────────────┐
│ ENGINE (Python, single authoritative core)                    │
│                                                               │
│  platform/          Screen, Game Loop, Input, EventBus        │
│  engine-core/       Pure ECS (no 2D, no rendering)            │
│  engine-2d/         Transform, Sprite, Camera, AABB physics   │
│  engine-raycast/    Grid maps, raycasting, player controller  │
│  engine-runtime/    Loop, input, render                       │
│  engine-editor-srv/ WebSocket server exposing the core        │
│                     (headless mode) to the editor             │
│  engine-package/    Packaging to .exe (PyInstaller/Nuitka)    │
└──────────────────────────────────────────────────────────────┘
                            ▲
                            │ WebSocket JSON-RPC (state + commands)
                            ▼
┌──────────────────────────────────────────────────────────────┐
│ EDITOR (Electron + React + TypeScript + Tailwind)             │
│  - Hierarchy, Inspector, Viewport (PixiJS), Asset browser     │
│  - Play/Stop: sends commands to the Python editor server      │
│  - Scene serialization: typed JSON shared with Python         │
└──────────────────────────────────────────────────────────────┘
```

**Strengths of this design:**
- The **Python core is unique and authoritative**.
- The **editor knows nothing about simulation**, only UI and painting received state.
- The **game runtime** uses the same core + a Python renderer. The editor does not.
- The editor is **web-tech**: modern, fast, polished (key to attracting users).

---

## Key Technical Decisions

| # | Decision | Choice | Rationale |
|---|---|---|---|
| 1 | Render in the editor viewport | **Decoupled rendering (Option B)**: Python simulates, editor paints | Guarantees "what you see in Play is what the runtime runs"; no engine divergence |
| 2 | Platform backend | **SDL2** (via Python bindings) — **no Pygame** | No immediate-mode model; full control of loop, window and events, ECS-friendly |
| 3 | Platform support | **Cross-platform**, **Windows-first** | Consistent with the `.exe` distribution goal |
| 4 | Input model | **Polling + per-frame events** | Polling for continuous movement, events for "pressed once" actions |
| 5 | Editor stack | **Electron + React + TypeScript + Tailwind + PixiJS** | Modern, fast UI; maximizes developer productivity |
| 6 | Distribution | **Packaged `.exe`** (PyInstaller / Nuitka) | Users run games without installing Python |

Full details:
- [Architecture and vision decisions](./PROJECT_VISION.md)
- [Platform layer decisions](./TECHNICAL_DECISIONS.md)

---

## Planned Features

### Engine
- [ ] **EventBus**: generic publish/consume event system, independent of SDL.
- [ ] **Platform layer**: screen/window, game loop with `dt`, frame-rate cap.
- [ ] **Input**: keyboard and mouse, both polling and per-frame events.
- [ ] **ECS core**: entities, components, systems, queries (composition over inheritance).
- [ ] **2D layer**: transforms, sprites, camera, simple AABB physics.
- [ ] **Raycasting layer**: grid-based maps and Doom-style renderer.
- [ ] **Scene format**: typed, versioned JSON shared between engine and editor.
- [ ] **Headless mode**: simulate without opening a window (for the editor).

### Editor
- [ ] **Scene hierarchy** panel.
- [ ] **Inspector** for editing component data.
- [ ] **2D level viewport** (PixiJS) with editing tools.
- [ ] **Play/Stop** to run the headless Python simulation and paint the result.
- [ ] **Asset browser**, gizmos, drag & drop, undo/redo, multi-scene support.

### Distribution
- [ ] **`.exe` packaging** of games (validate PyInstaller/Nuitka).
- [ ] Bundled native SDL2 binaries (no system-wide install required).

---

## Project Status

**This project is in early development.** The roadmap and honest expectations are documented in
[PROJECT_VISION.md](./PROJECT_VISION.md).

> **Note on the current `engine/` directory:** it contains an earlier **JavaScript-based ECS
> prototype** (used by an example project). It is a reference for ECS concepts and scene-format
> ideas, but it is **not** the target implementation. The target direction is a **Python** engine
> with an Electron/React editor, as described in this document.

High-level roadmap:

| Phase | Focus |
|---|---|
| **0 — Foundations** | Monorepo layout, scene format, protocol |
| **1 — Python ECS Core** | Entities, components, systems, queries (no rendering) |
| **2 — 2D Layer + Runtime** | Transforms, sprites, camera, physics, windowed/headless, `.exe` demo |
| **3 — Minimal Editor** | Hierarchy, inspector, viewport, Play, scene save/load |
| **4 — Unity-Style Editor** | Asset browser, gizmos, drag & drop, undo/redo, live preview |
| **5 — Open-Source Polish** | Docs, examples, editor packaging, CI |

> **Reality check:** this is a large project — months, not weeks. It is worth it if the goal is
> to **build** an engine and editor (learning / product), not merely to make games quickly
> (for that, Godot is the rational choice).

---

## Repository Structure (Planned)

```
engine/platform/       # Screen, game loop, input, EventBus, SDL2 backend
engine/core/           # Pure ECS: entities, components, systems, queries
engine/2d/             # Transform, Sprite, Camera, AABB physics
engine/raycast/        # Grid maps, raycasting, player controller
engine/runtime/        # Windowed/headless runtime and render
engine/editor_server/  # WebSocket server exposing the core to the editor
engine/package/        # Packaging to .exe (PyInstaller/Nuitka)

editor/                # Electron + React + TypeScript + Tailwind + PixiJS
shared-schema/         # Typed scene format and protocol shared by engine and editor
```

---

## Documents

- [PROJECT_VISION.md](./PROJECT_VISION.md) — goal, architecture decision, problems, roadmap.
- [TECHNICAL_DECISIONS.md](./TECHNICAL_DECISIONS.md) — platform layer decisions
  (SDL2, input, events, game loop).

---

## License

This project is licensed under the **Mozilla Public License 2.0 (MPL-2.0)**.

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
