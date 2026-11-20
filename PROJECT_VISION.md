# Project Vision — A Python-First Game Engine with a Unity-Style Editor

> **Goal:** An open-source 2D game engine written in Python, with a modern, Unity-inspired
> graphical editor (hierarchy, inspector, level editing, viewport with Play), whose games can be
> packaged as standalone `.exe` files.

---

## 1. What This Project Is

A game engine and editor for the Python ecosystem:

- **Generic ECS core** written in Python (multi-purpose, not tied to 2D).
- **2D layer** on top of the core (transforms, sprites, camera, simple physics).
- **Runtime** that can be packaged as a distributable `.exe`.
- **Modern, friendly editor** inspired by Unity: scene hierarchy, inspector, level editing,
  and a viewport with a Play button.

The core idea is a **"Godot/Unity-style editor but Python-first, built with web tech"**. This is a
real gap in the current ecosystem: engines like Pygame and Arcade have no built-in editor,
engine-like tools such as Ursina are 3D and not ECS-editor-friendly, and Godot is not
Python-first. There is room for a product in this space.

---

## 2. Core Architecture Decision (The One That Defines Everything)

The single most important decision is **where game logic runs inside the editor's viewport**.

We deliberately **do NOT** run Python rendering inside the viewport (no frame streaming,
no native window embedding). Instead we use **decoupled rendering (Option B)**:

- The **simulation lives in Python** and is the single source of truth.
- The editor's **viewport is drawn in JS** (PixiJS / Canvas) from the state Python sends.
- Python runs **headless** while editing (it simulates and exposes state).
- The **final game runtime uses a Python renderer** (pygame) with the same core, used for
  playing and distributing the game. The editor never uses that renderer.

### Why Option B

Two engines that simulate separately (JS in the editor, Python in the game) **diverge over
time**: games eventually "work in the editor but not in the `.exe`". For an open-source engine,
that destroys trust. Option B guarantees that **what you see in Play is exactly what the Python
runtime runs.**

### Rejected approaches

| Approach | Why rejected |
|---|---|
| **A. Stream frames from Python to the editor** | Adds latency and CPU cost, poor input feel; only worth it for heavy 3D. |
| **C. Editor simulates in JS (Pixi) only** | Two implementations of the engine → behavior divergence. |
| **D. Embed a native Python window in Electron** | Fragile and platform-specific (feasible on Windows, painful on Linux/macOS). |

---

## 3. Stack

```
┌──────────────────────────────────────────────────────────────┐
│ ENGINE (Python, single authoritative core)                    │
│                                                               │
│  engine-core/       Pure ECS (no 2D, no rendering)            │
│  engine-2d/         Transform, Sprite, Camera, AABB physics   │
│  engine-runtime/    Loop, input, render (pygame/pyglet)       │
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
- The **game runtime** uses the same core + a Python renderer (pygame). The editor does not.
- The editor is **web-tech**: modern, fast, polished (key to attracting users).

---

## 4. Real Problems to Expect (Honest View)

1. **Rendering written twice** (Pixi in the editor + pygame in the runtime). For 2D this is a
   small amount of code, but it must be maintained and kept aligned. Mitigation: define a shared
   **"render descriptor"** (which component produces which draw call) consumed by both renderers.
2. **Scene serialization**: a typed, versioned, shared **project format** (JSON/YAML) between the
   editor (TypeScript) and the engine (Python). Treat it as a core pillar from day one
   (JSON Schema + shared models).
3. **Packaging to `.exe`**: **PyInstaller** works but **Nuitka** gives better performance and
   cleaner binaries. Handle assets, plugins, and ensure the user doesn't need Python installed.
   Feasible but with friction (dynamic imports, plugins). Decide early.
4. **IPC and Play latency**: sending full state at 60 Hz with JSON can be heavy for many entities.
   Mitigation: **MessagePack** for frame data, or send **deltas** (only what changes). Manageable
   for 2D.
5. **Cross-platform**: start **Windows-first** (the `.exe` target). Do not promise
   macOS/Linux until solid. Electron + Python is cross-platform, but packaging each OS is work.
6. **User code hot reload**: a nice-to-have like Unity's. **Not Phase 1.** Hard to do correctly
   (reloading Python modules). Deferred.
7. **User scripting**: how engine users write logic. Start with **Python components and systems
   registered via API**. **No** visual DSL or embedded scripting at first.

---

## 5. What Makes This a Good Open-Source Project

- **Documented from day one**: protocol, project format, user-facing API.
- **Real examples**: at least one complete game included (pong → platformer).
- **Clear license** (MIT / Apache).
- **Split into packages** so it is reusable without the editor.
- **The editor is the draw**: modern, fast, not ugly (this is where React/Tailwind shines).

---

## 6. Roadmap

### Phase 0 — Foundations
- Monorepo: `engine/` (Python) + `editor/` (Electron + React) + `shared-schema/`
  (protocol and scene format).
- Define the **scene format** (typed JSON) and the **protocol** (JSON-RPC + MessagePack for frames).

### Phase 1 — Python ECS Core (independent, testable)
- `Entity`, `Component`, `World`, `System`, queries. No rendering.

### Phase 2 — 2D Layer + Runtime
- Transform, Sprite, Camera, AABB, loop with pygame. Headless and windowed modes.
- `.exe` packaging of a demo (validate PyInstaller/Nuitka).

### Phase 3 — Minimal Functional Editor
- Hierarchy + Inspector + Viewport (Pixi) + Play (headless Python simulation). Scene Save/Load.

### Phase 4 — "Unity-Style" Editor
- Asset browser, gizmos, drag & drop, undo/redo, live preview, multi-scene.

### Phase 5 — Open-Source Polish
- Docs, examples, editor packaging, CI.

---

## 7. Final Honest Recommendation

**This is a large project — months, not weeks.** But:

- **It fills the right gap** and has real value.
- **The stack fits perfectly**: Python (engine) + React/Electron/Tailwind (modern editor).
- **The correct architecture is Option B**: single Python core, JS editor that only paints,
  state-based protocol.
- **Start with the Python ECS core** and the definition of the **scene format + protocol**.
  Without those well defined, the editor is built on sand.

**What NOT to do:** start with the editor. The editor needs a stable core and a fixed protocol.
Starting from the UI leads to integration dead-ends.

**Building vs. using:** this project is worth it if the goal is to **build** an engine and editor
(learning / product). If the goal were only to **make games quickly**, using Godot would be the
rational choice. The value here is the engine itself and the Python-first editing experience.

---

## 8. Note on the Current `engine/` Directory

The existing `engine/` directory is a **JavaScript-based ECS prototype** (used by the snake
example). It is an earlier experiment. This document describes the **target direction**: a
**Python** engine with an Electron/React editor. The JavaScript prototype can serve as a
reference for ECS concepts and scene format ideas, but it is not the target implementation.