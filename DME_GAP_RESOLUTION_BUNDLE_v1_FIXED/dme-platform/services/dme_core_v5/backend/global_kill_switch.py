from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import threading
import time

_LOCK = threading.Lock()


@dataclass
class KillSwitchState:
    active: bool = False
    reason: Optional[str] = None
    activated_at: Optional[float] = None


_state = KillSwitchState()


def activate_kill_switch(reason: str) -> KillSwitchState:
    """Activate the global kill switch with a reason."""
    with _LOCK:
        _state.active = True
        _state.reason = reason
        _state.activated_at = time.time()
        return KillSwitchState(**_state.__dict__)


def reset_kill_switch() -> KillSwitchState:
    """Reset the kill switch (controlled recovery only)."""
    with _LOCK:
        _state.active = False
        _state.reason = None
        _state.activated_at = None
        return KillSwitchState(**_state.__dict__)


def get_kill_switch_state() -> KillSwitchState:
    """Return a copy of the current kill switch state."""
    with _LOCK:
        return KillSwitchState(**_state.__dict__)
