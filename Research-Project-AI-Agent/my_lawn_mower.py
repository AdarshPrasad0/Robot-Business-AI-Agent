import asyncio

class MyLawnMower:
    """Representation of a smart lawn mower with multiple activity states."""

    VALID_ACTIVITIES = ["MOWING", "DOCKED", "PAUSED", "RETURNING", "ERROR"]

    def __init__(self, name: str):
        self._name = name
        self._activity = "DOCKED"
        self._error_message = None

    @property
    def activity(self) -> str:
        """Return the current activity of the mower."""
        return self._activity

    @property
    def error_message(self) -> str:
        """Return the last error message if any."""
        return self._error_message

    def start_mowing(self):
        """Start mowing from docked or paused state."""
        if self._activity == "ERROR":
            print(f"[ERROR] Cannot start mowing. Error present: {self._error_message}")
            return
        print(f"[INFO] {self._name} starting mowing.")
        self._activity = "MOWING"

    def dock(self):
        """Dock the mower (stop and dock)."""
        if self._activity == "ERROR":
            print(f"[ERROR] Cannot dock. Error present: {self._error_message}")
            return
        print(f"[INFO] {self._name} docking.")
        self._activity = "DOCKED"

    def return_to_dock(self):
        """Return mower to the dock."""
        if self._activity == "ERROR":
            print(f"[ERROR] Cannot return to dock. Error present: {self._error_message}")
            return
        print(f"[INFO] {self._name} returning to dock.")
        self._activity = "RETURNING"

    def pause(self):
        """Pause mowing only if currently mowing or returning."""
        if self._activity in ["MOWING", "RETURNING"]:
            print(f"[INFO] {self._name} paused.")
            self._activity = "PAUSED"
        else:
            print(f"[WARN] Cannot pause while {self._activity}.")

    def resume(self):
        """Resume mowing only if paused."""
        if self._activity == "PAUSED":
            print(f"[INFO] {self._name} resuming mowing.")
            self._activity = "MOWING"
        else:
            print(f"[WARN] Cannot resume while {self._activity}.")

    def set_error(self, message: str):
        """Set mower to error state with a message."""
        print(f"[ERROR] {self._name} encountered an error: {message}")
        self._activity = "ERROR"
        self._error_message = message

    def clear_error(self):
        """Clear error and return mower to docked state."""
        print(f"[INFO] {self._name} error cleared. Returning to docked state.")
        self._error_message = None
        self._activity = "DOCKED"

    async def async_start_mowing(self):
        """Async version of start mowing."""
        await asyncio.sleep(0.1)
        self.start_mowing()

    async def async_dock(self):
        """Async version of docking."""
        await asyncio.sleep(0.1)
        self.dock()

    async def async_return_to_dock(self):
        """Async version of return to dock."""
        await asyncio.sleep(0.1)
        self.return_to_dock()
