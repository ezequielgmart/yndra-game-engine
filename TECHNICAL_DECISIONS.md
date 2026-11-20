# Platform Layer Decisions — SDL2, Input, Events and the Game Loop

> **Scope:** This document records the decisions for the **platform layer** of the engine
> (window, game loop, input, and the pub/sub event system). It is the low-level layer that sits
> **below** the ECS and knows nothing about entities or game logic. It complements
> `PROJECT_VISION.md`.

---

## 1. Context

The engine is Python-first and ECS-oriented. We deliberately **do not use Pygame**, because its
immediate-mode model ("something draws something") does not fit an ECS architecture. Instead we
build a thin, explicit platform layer over **SDL2**, giving full control of the loop, the
window, and the event flow.

The platform layer is responsible only for:

1. Creating a **screen** (window + drawing surface).
2. Providing a **global Screen object** used to paint.
3. Running the **game loop** (infinite while active).
4. Executing **`update` every frame** while the loop is running.
5. A **publish/consume (pub/sub) event system**.
6. **Input detection** (keyboard and mouse) for now.

Everything else (entities, components, systems, rendering, scene serialization, editor) sits on
top and is out of scope here.

---

## 2. Confirmed Decisions

| # | Decision | Choice |
|---|---|---|
| 1 | Platform backend | **SDL2** (via Python bindings such as PySDL2) |
| 2 | Platform support | **Cross-platform**, with a **Windows-first** focus from the start |
| 3 | Input model | **Both**: polling (current state) **and** per-frame events |

These are the decisions this layer is built around.

---

## 3. Why SDL2 (and Not Pygame)

- **No immediate-mode model.** SDL2 gives us a window, an event queue, and a drawing surface, but
  **does not impose** a "draw in place" API on the architecture. We control the frame and the
  flow, which fits ECS.
- **Reinvents Pygame, not SDL.** Pygame is essentially a higher-level wrapper over SDL. Dropping
  Pygame (but keeping SDL2) removes the opinionated model **without** losing native video/input.
- **Cross-platform by nature**, which satisfies the cross-platform goal while we focus on Windows
  first.
- **Minimal dependency footprint.** A thin layer over SDL2 is small and auditable.

---

## 4. Layer Responsibilities

### 4.1 Screen / Window
- Create a window with configurable **title** and **size**.
- Expose a **global Screen object** used for painting.
- `present()` shows the current frame; the renderer/systems never touch the window directly.
- Handle **close** (window close / `Quit`) to shut down cleanly.

### 4.2 Game Loop
- The loop runs **`while running`** (not `while True`). `running` is cleared on `Quit` or an exit
  key (e.g. Esc), guaranteeing a clean shutdown.
- Each frame computes **delta time (`dt` seconds)**, which is passed to `update(dt)`.
- **Frame order** is fixed:
  1. Pump platform input (SDL event pump).
  2. Update input state (polling state + per-frame event queue).
  3. `update(dt)` (game logic, later ECS systems).
  4. `present()` (show the frame).
  5. Frame-rate cap / vsync.
- A **frame-rate cap** (default 60 FPS, configurable) prevents burning CPU. Vsync may be used
  where available.

### 4.3 Input
Two complementary models, both supported:

- **Polling (current state):** e.g. `input.is_key_down(Key.W)`, current mouse position, whether a
  button is held. Best for continuous movement.
- **Per-frame events:** a queue of discrete events (`KeyDown`, `KeyUp`, `MouseButtonDown`,
  `MouseMove`, `Quit`, ...), drained every frame. Best for "pressed once" actions.

Key points:
- SDL events are **translated** into the engine's own event types; **raw SDL codes never leak**
  into game logic.
- A dedicated **key enum** maps keys to engine-level identifiers.
- Mouse coordinates are **normalized** (window space vs. logical space) as needed.
- The **per-frame event queue is cleared each frame**; the **polling state persists** and is
  updated from raw input each frame.

---

## 5. Event System (Pub/Sub)

The engine uses a **publish/consume** event model, but **platform input and game events are kept
as separate concerns**:

```
SDL event pump  ──►  InputAdapter (normalizes keyboard/mouse)
                          │
                          ▼
                    EventBus (pub/sub)  ◄── systems publish/consume
```

- The **platform input layer** only reads OS input and translates it into normalized events.
- The **EventBus** is **generic and independent of SDL**. It supports subscribe / publish /
  consume, and is the channel through which game systems communicate.
- An **adapter** connects platform input to the EventBus (or exposes polling state, depending on
  the consumer).

### EventBus design points
- **Per-frame consumption:** the action-event queue is drained once per frame.
- **Ownership:** the bus is **per-World** (not a global singleton), to avoid global coupling and
  keep simulation and editor isolated. (Platform input state may be a global resource of the
  World, but the pub/sub bus itself is scoped.)
- **Safe iteration:** publishing during a dispatch must not mutate the list being iterated
  (buffer/defer publishes to the next dispatch).
- **Subscribe/unsubscribe** must be explicit and clean.

---

## 6. Module Layout (Planned)

```
engine/platform/
├── window.py          # Screen: create, title, size, present, close, is_open
├── loop.py            # GameLoop: while running -> pump -> update(dt) -> present -> cap
├── input.py           # InputAdapter: polling state + per-frame events
├── events.py          # EventBus: subscribe / publish / consume
└── backend/
    └── sdl2_backend.py  # Concrete SDL2 implementation, isolated behind an interface
```

- The **backend is isolated behind an interface**, so SDL2 can later be swapped (e.g. GLFW)
  without touching window/loop/input contracts.

---

## 7. Implementation Order

1. **EventBus** (`events.py`) — pure logic, no window, testable in isolation.
2. **Screen/Window** (`window.py` + backend) — open a window, present, close.
3. **InputAdapter** (`input.py`) — translate keyboard/mouse to engine events (polling + events).
4. **GameLoop** (`loop.py`) — `while running: pump -> update(dt) -> present`, with clean exit.

This order validates the pub/sub model before introducing SDL, then builds outward.

---

## 8. Non-Goals (Out of Scope for This Layer)

- ECS (`Entity`, `Component`, `System`) — built on top.
- Game rendering (sprites, raycasting) — in `engine-2d` / `engine-raycast`, using Screen
  primitives.
- Scene serialization / project format.
- Editor / WebSocket protocol.
- Audio, gamepads (not yet).

---

## 9. Windows-First, Cross-Platform

- The design is **cross-platform** (SDL2 enables this).
- **Windows is the primary target** at the start (consistent with the `.exe` distribution goal).
- SDL2 native binaries must be **bundled/shipped** with the project so the platform layer does not
  depend on a system-wide SDL2 installation.
- macOS/Linux support is kept possible by design but not guaranteed/promised until validated.

---

## 10. Definition of Done (First Working Window)

- Opens a window with configurable title and size.
- Paints a background (or a test rectangle).
- Receives keyboard and mouse input via **both** polling and per-frame events.
- Runs update every frame with a stable `dt`.
- Closes cleanly via the window close button and an exit key (e.g. Esc).
- Releases all resources on exit (no leaks).