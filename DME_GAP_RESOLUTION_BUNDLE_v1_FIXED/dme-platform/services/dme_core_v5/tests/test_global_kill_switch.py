from services.dme_core_v5.backend.global_kill_switch import (
    activate_kill_switch,
    get_kill_switch_state,
    reset_kill_switch,
)


def test_kill_switch_cycle():
    reset_kill_switch()
    state = get_kill_switch_state()
    assert state.active is False

    activate_kill_switch("unit-test")
    state = get_kill_switch_state()
    assert state.active is True
    assert state.reason == "unit-test"

    reset_state = reset_kill_switch()
    assert reset_state.active is False
