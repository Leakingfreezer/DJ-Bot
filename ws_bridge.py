"""
WebSocket bridge — streams pipeline state to the React UI.

Usage (automatic):
    main.py calls ws_bridge.start() once, then broadcast(state) each frame.

Usage (manual test):
    python ws_bridge.py   → starts server, prints when clients connect

The React UI connects to ws://localhost:8765 and expects JSON frames
with any subset of these keys:
    gesture, last_action, hover_target, is_playing,
    volume, waveform_scale, turntable_position,
    index_x, index_y
"""

import asyncio
import json
import threading

try:
    import websockets
except ImportError:
    raise ImportError("Run: pip install websockets")


PORT = 8765

_clients: set = set()
_loop: asyncio.AbstractEventLoop | None = None


async def _handler(ws):
    _clients.add(ws)
    try:
        await ws.wait_closed()
    finally:
        _clients.discard(ws)


async def _serve():
    async with websockets.serve(_handler, "localhost", PORT):
        print(f"[ws_bridge] listening on ws://localhost:{PORT}")
        await asyncio.Future()  # run until cancelled


def _run(loop: asyncio.AbstractEventLoop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_serve())


def start():
    """Start the WebSocket server in a background daemon thread."""
    global _loop
    if _loop is not None:
        return  # already running
    _loop = asyncio.new_event_loop()
    t = threading.Thread(target=_run, args=(_loop,), daemon=True, name="ws-bridge")
    t.start()


def broadcast(state: dict):
    """Push a state snapshot to all connected React clients (non-blocking)."""
    if _loop is None or not _clients:
        return

    msg = json.dumps(state)

    async def _send():
        dead = set()
        for ws in list(_clients):
            try:
                await ws.send(msg)
            except Exception:
                dead.add(ws)
        _clients.difference_update(dead)

    asyncio.run_coroutine_threadsafe(_send(), _loop)


# ── manual test ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import time

    start()

    # send a fake heartbeat every second so you can test the UI without the camera
    fake = {
        "gesture": "none",
        "last_action": "ws_bridge test mode",
        "hover_target": None,
        "is_playing": False,
        "volume": 50,
        "waveform_scale": 1.0,
        "turntable_position": 0.0,
        "index_x": None,
        "index_y": None,
    }

    try:
        while True:
            broadcast(fake)
            time.sleep(1)
    except KeyboardInterrupt:
        print("[ws_bridge] stopped")
