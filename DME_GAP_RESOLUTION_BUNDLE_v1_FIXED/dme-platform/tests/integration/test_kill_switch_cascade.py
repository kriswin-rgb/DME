from services.dme_core_v5.backend.global_kill_switch import (
    activate_kill_switch,
    get_kill_switch_state,
    reset_kill_switch,
)


def test_kill_switch_cascade_simple():
    reset_kill_switch()
    activate_kill_switch("integration-test")
    state = get_kill_switch_state()
    assert state.active is True
