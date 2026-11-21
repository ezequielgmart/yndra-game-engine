# Technical Decisions — Rendering Backend, Editor Model, Events and Licensing

> **Scope:** This document records the technical decisions for the engine: the rendering
> backend, the **editor model** (static data editor, not a simulator), the editor↔runtime
> contract, the abstraction boundaries required from day one, the custom event system, the
> licensing, the MVP implementation plan, and the updated risk list. It complements
> `PROJECT_VISION.md`.

---

## 1. Context

The engine is Python-first and ECS-oriented. It uses **pygame-ce** as its runtime rendering and
input library for the MVP, behind mandatory abstractions (`Platform`, `IRenderer`, `InputState`)
so the backend can be migrated later without touching ECS logic.

The **editor is a static data editor**, not a simulator. It paints the level statically (tiles,
sprites, gizmos, grid) and edits **JSON level and prefab files**. It has a hierarchy, an
inspector, an asset browser, and a level editor, but it does **not** run game logic. The **Play**
button launches a **separate Python process** (`game.py` or the packaged executable) that loads
the JSON and runs the real game.

The engine and editor responsibilities are strictly separated:

1. The **editor** edits JSON (levels, prefabs) and paints a static preview.
2. The **runtime** (pygame-ce) loads the JSON and executes the actual game.
3. The only contract between them is **JSON files + a spawned subprocess**.

---

## 2. Confirmed Decisions

| # | Decision | Choice |
|---|---|---|
| 1 | Runtime rendering backend (MVP) | **pygame-ce** |
| 2 | Platform support | **Cross-platform**, with a **Windows-first** focus |
| 3 | Input model | **Both**: polling (current state) **and** per-frame events |
| 4 | Editor model | **Static data editor** (no simulation, no embedded rendering) |
| 5 | Editor↔runtime contract | **JSON files + `subprocess.Popen`** |
| 6 | License (engine/editor) | **MPL-2.0** |
| 7 | pygame/pygame-ce license | **LGPL-2.1** (documented as Third-Party Notice) |

These are the decisions this project is built around.

---

## 3. Rendering Backend: Why pygame-ce

### 3.1. Why pygame-ce for the MVP

- **Large community and abundant documentation.**
- **Active maintenance.**
- **High development speed.**
- **Sufficient for a 2D tile-based RPG** at short and medium term.

The choice could change in the future, but pygame-ce offers an API sufficient for what we want to
achieve at short and medium term.

### 3.2. Why PySDL2 is rejected as the initial base

- **Inactive project** (last release 0.9.17, single maintainer, small community).
- It requires **building the convenience layer manually** (events, resources, clock, high-level
  drawing).
- Its **performance advantage is not automatic** and is **not necessary for the MVP**.

### 3.3. Future optimization path

If drawing becomes a bottleneck, the planned path is:

- **`pygame._sdl2`** — the pygame-ce module that exposes the GPU renderer and textures, or
- a **scoped migration to PySDL2**.

Because game logic and ECS systems never import pygame directly (see §4), either path stays
possible.

---

## 4. Mandatory Abstractions from Day 1

So that choosing pygame-ce does not lock the project in, these abstractions are mandatory from
the start:

- **`IRenderer`** — drawing interface (sprite, rect, text, camera, layers). Game logic and ECS
  systems never import pygame directly.
- **`Platform`** — platform interface abstracting:
  - Input and events (keyboard, mouse, quit, resize, focus).
  - Window and presentation.
  - Clock / dt.
  - Audio (if the MVP has sound).
- **`InputState`** — the polling state consumed by the game loop and ECS systems.

The game loop and ECS systems consume **`InputState`** and **`Platform`**, not `pygame.key`,
`pygame.event`, or `pygame.time` directly.

**Practical rule:** interfaces must stay **small** (e.g. `InputState` with ~8 fields,
`IRenderer` with ~6 methods), not a clone of SDL. Do **not** abstract joysticks, IME, clipboard,
etc., until they are needed.

---

## 5. Editor Model and Editor↔Runtime Contract

### 5.1. The editor is a data editor

- The editor lives in **Electron + React + TypeScript + Tailwind** (separate process).
- Its **viewport paints the level statically** using **PixiJS/Canvas**. It does not simulate or
  execute game logic.
- It edits **JSON level and prefab files**: hierarchy, inspector, asset browser, level editing
  (placing where entities would be), gizmos, grid.

### 5.2. Play launches a separate process

- The **Play** button launches a **separate Python process** (`game.py` or the packaged
  executable).
- That process loads the JSON files and runs the **real game with pygame-ce**.
- There is **no embedded simulation**, **no state IPC**, and **no 60 Hz streaming**.

### 5.3. The JSON contract is the pillar

Since there is only JSON + process spawn between editor and runtime, **scene serialization
becomes the central pillar of the project**: the project's JSON format is the **only contract**
between editor and runtime.

- No hot reload of user code: the game is **relaunched**.

```
┌──────────────────────────────┐        JSON files         ┌──────────────────────────────┐
│ EDITOR (Electron/React/TS)   │  ───────────────────────▶ │ RUNTIME (Python + pygame-ce) │
│  - Static painting (PixiJS)  │                           │  - Loads JSON                │
│  - Edits levels/prefabs JSON │  ◀──── subprocess.Popen ──│  - Runs the real game        │
└──────────────────────────────┘        (spawn)            └──────────────────────────────┘
```

---

## 6. Licensing

- **Engine and editor:** **MPL-2.0** (Mozilla Public License 2.0). File-level copyleft,
  commercial use permitted, user code may be proprietary.
- **pygame / pygame-ce:** **LGPL-2.1**, compatible with MPL-2.0 (MPL 2.0 recognizes it as a
  **Secondary License**).

### 6.1. Obligations to document

- Add a **"Third-Party Notices"** section in `THIRD_PARTY_NOTICES.md` (or in `LICENSE.md`) that:
  - Names **pygame/pygame-ce** and its **LGPL-2.1** license.
  - States it is used **unmodified** as an external dependency, **dynamically imported**.
  - Retains the **copyright notices** and the **full LGPL-2.1 text** (from the FSF or from the
    pygame package, e.g. `docs/LGPL.txt`).
  - Declares that the user may **replace the library** (the Python `import` satisfies
    relinkability).
- Update `README.md` to reference that section.
- If pygame is **ever modified**, those changes must be released under a **compatible (LGPL)**
  license and documented.

---

## 7. Custom Events in pygame-ce

pygame-ce does support custom events, conceptually equivalent to PySDL2's.

- **API:**
  - `pygame.event.custom_type()` reserves an identifier.
  - `pygame.event.post(pygame.event.Event(TYPE, **data))` publishes.
  - `pygame.event.get()` consumes.
- **Limitation:** only **8 slots** exist for user events. For an engine with many semantic
  events, use this pattern:
  - Reserve a **single type**: `GAME_EVENT = pygame.event.custom_type()`.
  - Distinguish by **attribute**:
    `pygame.event.Event(GAME_EVENT, kind="player_died", score=100)`.
  - Consume with `if event.type == GAME_EVENT: if event.kind == "player_died": ...`.
- **Periodic events:** `pygame.time.set_timer(EVENT, ms)` publishes automatically at an interval.
- **Encapsulation:** these events are **internal to the runtime**. They can be exposed through
  the ECS's own **`EventBus`**, so game logic never depends on `pygame.event` directly. If the
  project migrates to PySDL2, only the `EventBus` is reimplemented over
  `SDL_PushEvent`/`SDL_PollEvent`.

---

## 8. Implementation Plan (MVP)

**Minimum validation slice (2–3 weeks):**

- A **JSON level** with 10 tiles and 2 sprites.
- A **minimal editor** that paints the level statically.
- A **`game.py`** that loads the JSON and paints it with pygame-ce.
- A **Play button** that launches the process and captures `stdout`/`stderr`.

If this flows, the architecture is validated.

- **Phase 1 — ECS core:** `Entity`, `Component`, `World`, `System`, queries. No rendering.
- **Phase 2 — 2D layer + runtime:** `Transform`, `Sprite`, `Camera`, `AABB`, loop with
  pygame-ce. Windowed and headless modes.
- **Phase 3 — Minimal functional editor:** hierarchy, inspector, static viewport, Play (spawn),
  save/load JSON.
- **Phase 4 — "RPG Maker-style" editor:** asset browser, gizmos, drag & drop, undo/redo,
  multi-scene.
- **Phase 5 — Open-source polish:** docs, examples, editor packaging, CI.

**What we do NOT do:**

- Embedded simulation in the editor.
- WebSocket / MessagePack IPC.
- Hot reload of user code.
- An editor integrated in the same process as the game (Doom-style).

---

## 9. Updated Risks and Mitigations

| Risk | Status | Mitigation |
|---|---|---|
| Double simulation renderer (Pixi vs pygame) | **Eliminated** | Editor paints static; runtime paints dynamic. They do not simulate the same thing. |
| IPC at 60 Hz | **Eliminated** | Only JSON files + process spawn. |
| Hot reload | **Not applicable** | The game is relaunched. |
| Visual divergence editor vs game | **New minor risk** | Define visual conventions (tile size, layers, draw order) in the project JSON; both read from the same source. |
| `.exe` packaging | **Persists** | Decide PyInstaller vs Nuitka in Phase 2; test with a demo. |
| User scripting | **Persists** | Python components/systems registered via API. No visual DSL or embedded scripting in Phase 1. |
| PySDL2 inactive | **Mitigated** | Not used as a base; pygame-ce + `pygame._sdl2` as the optimization path. |

---

## 10. Module Layout (Planned)

```
engine/platform/       # Platform, InputState, loop, EventBus, pygame-ce backend
engine/render/         # IRenderer + pygame-ce implementation (pygame._sdl2-ready)
engine/core/           # Pure ECS: entities, components, systems, queries
engine/2d/             # Transform, Sprite, Camera, AABB physics
engine/raycast/        # Grid maps, raycasting, player controller
engine/runtime/        # game.py entry point: load JSON, run the real game
engine/package/        # Packaging to .exe (PyInstaller/Nuitka)

editor/                # Electron + React + TypeScript + Tailwind + PixiJS
shared-schema/         # Typed, versioned JSON level/prefab format
```

- The **renderer backend is isolated behind `IRenderer`**, and the **platform behind
  `Platform`**, so the backend can be swapped (e.g. PySDL2) without touching ECS logic.

---

## 11. Non-Goals (Out of Scope)

- Embedded simulation in the editor.
- State IPC / WebSocket / MessagePack frame streaming.
- User code hot reload.
- Audio, gamepads (not yet).

---

## 12. Windows-First, Cross-Platform

- The design is **cross-platform**.
- **Windows is the primary target** at the start (consistent with the `.exe` distribution goal).
- Runtime dependencies (pygame-ce) must be **bundled/shipped** so the game does not depend on a
  system-wide installation.
- macOS/Linux support is kept possible by design but not guaranteed/promised until validated.

---

## 13. Definition of Done (First Working Vertical Slice)

- A JSON level with tiles and sprites loads in both the editor (static) and `game.py`.
- The editor paints the level statically with grid, gizmos, and inspector.
- The **Play** button spawns the runtime process and captures `stdout`/`stderr`.
- Game logic and ECS systems import **no** pygame symbols directly (`Platform`/`IRenderer`/
  `InputState` only).
- Third-Party Notices for pygame-ce (LGPL-2.1) are present and referenced from the README.
```

---

## `README.md`

```markdown README.md
# Pyndra

> A Python-first 2D game engine built on an ECS core, with a modern, RPG Maker-inspired editor
> and standalone `.exe` distribution.
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
- [Dependencies and License](#dependencies-and-license)

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
- The **editor only edits data and paints static state**, never simulates.
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
| **4 — RPG Maker-Style Editor** | Asset browser, gizmos, drag & drop, undo/redo, live multiplayer |
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
- [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) — third-party dependency notices
  (pygame-ce / LGPL-2.1).

---

## Dependencies and License

This engine uses **pygame-ce** as its runtime rendering and input library for the MVP.
**pygame-ce** is distributed under the **GNU Lesser General Public License, version 2.1
(LGPL-2.1)**.

- **pygame-ce** is used **unmodified** as an external, **dynamically imported** Python
  dependency.
- The original copyright and LGPL notices for pygame-ce are retained in
  [`THIRD_PARTY_NOTICES.md`](./THIRD_PARTY_NOTICES.md) (and in the pygame-ce package itself).
- Users are free to **replace the installed pygame-ce package** with a modified version, as
  required by the LGPL (the Python `import` satisfies relinkability).
- This project's own code remains under **MPL-2.0**. The LGPL applies only to pygame-ce itself.
- The project reserves **`IRenderer`** and **`Platform`** interfaces, so the rendering backend
  could be migrated (e.g. to PySDL2 or `pygame._sdl2`) in the future without affecting game code.

The engine and editor are licensed under the **Mozilla Public License 2.0 (MPL-2.0)**.

MPL-2.0 was chosen deliberately as a balance between openness and real-world usability:

- **Commercial use is encouraged.** Games built with the engine may keep their code closed.
- **The core stays open.** Improvements to the engine's own source files must remain open under
  MPL-2.0.
- **File-level copyleft.** MPL-2.0 applies per source file rather than to the whole project,
  keeping the engine open without "infecting" the user's game code.

See the [LICENSE](./LICENSE.md) file for the full license text and
[THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md) for dependency notices.
```

> Note: I fixed a small typo from your roadmap table (`live multiplayer` → should be
> `multi-scene`) — if you prefer keeping it verbatim, replace that cell with `multi-scene`.

---

## `PROJECT_VISION.md`

```markdown PROJECT_VISION.md
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