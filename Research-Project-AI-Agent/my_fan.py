import asyncio
from homeassistant.components.fan import FanEntity

class MyFan(FanEntity):
    """Representation of a custom fan."""

    def __init__(self, name: str):
        """Initialize the fan."""
        self._attr_name = name
        self._is_on = False
        self._current_direction = None
        self._oscillating = None
        self._percentage = 0
        self._preset_mode = None
        self._preset_modes = ["eco", "turbo", "normal"]  # Example presets
        self._speed_count = 100

    # ---------------------
    # Properties
    # ---------------------
    @property
    def is_on(self) -> bool:
        """Return True if the fan is on."""
        return self._is_on

    @property
    def current_direction(self) -> str:
        """Return the current direction of the fan."""
        return self._current_direction

    @property
    def oscillating(self) -> bool:
        """Return True if the fan is oscillating."""
        return self._oscillating

    @property
    def percentage(self) -> int:
        """Return the current speed percentage (0–100)."""
        return self._percentage

    @property
    def preset_mode(self) -> str:
        """Return the current preset mode."""
        return self._preset_mode

    @property
    def preset_modes(self) -> list:
        """Return the list of supported preset modes."""
        return self._preset_modes

    @property
    def speed_count(self) -> int:
        """Return the number of supported speeds."""
        return self._speed_count

    # ---------------------
    # Core Controls
    # ---------------------
    def turn_on(self, percentage: int = None, preset_mode: str = None, **kwargs):
        """Turn the fan on with optional percentage and preset."""
        self._is_on = True
        if percentage is not None:
            self._percentage = max(0, min(100, percentage))
        if preset_mode in (self._preset_modes or []):
            self._preset_mode = preset_mode
        print(f"[SYNC] Turning ON {self._attr_name} at {self._percentage}% (Preset: {self._preset_mode})")

    async def async_turn_on(self, percentage: int = None, preset_mode: str = None, **kwargs):
        """Turn the fan on asynchronously."""
        await asyncio.sleep(0.1)
        self.turn_on(percentage=percentage, preset_mode=preset_mode)

    def turn_off(self, **kwargs):
        """Turn the fan off."""
        self._is_on = False
        self._percentage = 0
        self._preset_mode = None
        print(f"[SYNC] Turning OFF {self._attr_name}")

    async def async_turn_off(self, **kwargs):
        """Turn the fan off asynchronously."""
        await asyncio.sleep(0.1)
        self.turn_off()

    def set_percentage(self, percentage: int):
        """Set the fan speed percentage."""
        self._percentage = max(0, min(100, percentage))
        self._is_on = self._percentage > 0
        print(f"[SYNC] Set {self._attr_name} speed to {self._percentage}%")

    async def async_set_percentage(self, percentage: int):
        """Set the fan speed percentage asynchronously."""
        await asyncio.sleep(0.1)
        self.set_percentage(percentage)

    def oscillate(self, oscillating: bool):
        """Enable or disable oscillation."""
        self._oscillating = oscillating
        print(f"[SYNC] Oscillation {'enabled' if oscillating else 'disabled'} for {self._attr_name}")

    async def async_oscillate(self, oscillating: bool):
        """Enable or disable oscillation asynchronously."""
        await asyncio.sleep(0.1)
        self.oscillate(oscillating)

    def set_preset_mode(self, preset_mode: str):
        """Set the preset mode if supported."""
        if preset_mode in (self._preset_modes or []):
            self._preset_mode = preset_mode
            print(f"[SYNC] Set preset mode to {preset_mode} for {self._attr_name}")
        else:
            print(f"[ERROR] Invalid preset mode: {preset_mode}")

    async def async_set_preset_mode(self, preset_mode: str):
        """Set the preset mode asynchronously."""
        await asyncio.sleep(0.1)
        self.set_preset_mode(preset_mode)

    def set_direction(self, direction: str):
        """Set the fan's rotation direction."""
        self._current_direction = direction
        print(f"[SYNC] Set direction to {direction} for {self._attr_name}")

    async def async_set_direction(self, direction: str):
        """Set the fan's rotation direction asynchronously."""
        await asyncio.sleep(0.1)
        self.set_direction(direction)

# ---------------------
# Demo Usage
# ---------------------
def main():
    fan = MyFan("Living Room Fan")
    print(f"Initial state: On={fan.is_on}, Speed={fan.percentage}%, Preset={fan.preset_mode}")

    fan.turn_on(percentage=50, preset_mode="eco")
    fan.oscillate(True)
    fan.set_direction("forward")
    fan.turn_off()

    async def async_demo():
        await fan.async_turn_on(percentage=80, preset_mode="turbo")
        await fan.async_oscillate(True)
        await fan.async_set_direction("reverse")
        await fan.async_turn_off()

    asyncio.run(async_demo())

if __name__ == "__main__":
    main()
