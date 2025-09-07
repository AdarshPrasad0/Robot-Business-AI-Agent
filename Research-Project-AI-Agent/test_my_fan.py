import pytest
from my_fan import MyFan

@pytest.fixture
def fan():
    """Fixture to create a default fan instance."""
    return MyFan(name="Test Fan")

# 1. Turn Fan On
def test_turn_fan_on(fan):
    fan.turn_on(percentage=50)
    assert fan.is_on is True
    assert fan.percentage == 50

# 2. Turn Fan Off
def test_turn_fan_off(fan):
    fan.turn_on(percentage=50)
    fan.turn_off()
    assert fan.is_on is False
    assert fan.percentage == 0

# 3. Set Fan Speed 75%
def test_set_fan_speed_75(fan):
    fan.set_percentage(75)
    assert fan.percentage == 75
    assert fan.is_on is True

# 4. Set Fan Speed 0%
def test_set_fan_speed_zero(fan):
    fan.set_percentage(0)
    assert fan.percentage == 0
    assert fan.is_on is False

# 5. Set Fan Speed Max (100%)
def test_set_fan_speed_max(fan):
    fan.set_percentage(150)  # Should clamp to 100
    assert fan.percentage == 100
    assert fan.is_on is True

# 6. Enable Oscillation
def test_enable_oscillation(fan):
    fan.oscillate(True)
    assert fan.oscillating is True

# 7. Disable Oscillation
def test_disable_oscillation(fan):
    fan.oscillate(True)
    fan.oscillate(False)
    assert fan.oscillating is False

# 8. Change Direction: Forward → Reverse and Reverse → Forward
def test_change_direction(fan):
    fan.set_direction("forward")
    assert fan.current_direction == "forward"
    fan.set_direction("reverse")
    assert fan.current_direction == "reverse"

# 9. Activate Preset Mode
def test_activate_preset_mode(fan):
    fan.set_preset_mode("eco")
    assert fan.preset_mode == "eco"

# 10. Deactivate Preset Mode (set to None)
def test_deactivate_preset_mode(fan):
    fan.set_preset_mode("eco")
    fan.set_preset_mode(None)
    assert fan.preset_mode is None

# 11. Invalid Preset Mode
def test_invalid_preset_mode(fan, capsys):
    fan.set_preset_mode("invalid_mode")
    captured = capsys.readouterr()
    assert "invalid" in captured.out.lower()
    assert fan.preset_mode is None

# 12. Turn On Fan with Preset
def test_turn_on_with_preset(fan):
    fan.turn_on(percentage=60, preset_mode="turbo")
    assert fan.is_on is True
    assert fan.preset_mode == "turbo"
    assert fan.percentage == 60

# 13. Change Speed while Oscillating
def test_change_speed_while_oscillating(fan):
    fan.oscillate(True)
    fan.set_percentage(80)
    assert fan.percentage == 80
    assert fan.oscillating is True

# 14. Turn Off Fan while in Preset
def test_turn_off_while_in_preset(fan):
    fan.turn_on(percentage=70, preset_mode="eco")
    fan.turn_off()
    assert fan.is_on is False
    assert fan.preset_mode is None
    assert fan.percentage == 0
