import asyncio
from homeassistant.components.lock import LockEntity

class MyLock(LockEntity):
    """Representation of a custom lock with jammed state and automatic jam detection."""

    def __init__(self, name: str):
        """Initialize the lock."""
        self._attr_name = name
        self._is_locked = False
        self._is_jammed = False
        self._is_locking = False
        self._is_unlocking = False

    @property
    def is_locked(self) -> bool:
        """Return true if the lock is locked."""
        return self._is_locked

    @property
    def is_jammed(self) -> bool:
        """Return true if the lock is jammed."""
        return self._is_jammed

    def jam(self):
        """Manually set the lock to a jammed state."""
        print(f"[ALERT] {self._attr_name} is JAMMED!")
        self._is_jammed = True
        self._is_locking = False
        self._is_unlocking = False

    def clear_jam(self):
        """Clear a jammed lock."""
        print(f"[INFO] Clearing jam on {self._attr_name}")
        self._is_jammed = False
        self._is_locked = False  # Safety reset
        self._is_locking = False
        self._is_unlocking = False

    async def async_lock(self, **kwargs):
        """Lock the lock asynchronously."""
        if self._is_jammed:
            print(f"[ERROR] Cannot lock {self._attr_name} — it is jammed!")
            return
        if self._is_locking or self._is_unlocking:
            print(f"[JAM] Conflict detected while locking {self._attr_name}")
            self.jam()
            return
        if self._is_locked:
            print(f"[INFO] {self._attr_name} is already locked.")
            return

        code = kwargs.get("code")
        print(f"[ASYNC] Locking {self._attr_name} with code: {code}")
        self._is_locking = True
        await asyncio.sleep(0.1)  # Simulate locking time
        self._is_locked = True
        self._is_locking = False

    async def async_unlock(self, **kwargs):
        """Unlock the lock asynchronously."""
        if self._is_jammed:
            print(f"[ERROR] Cannot unlock {self._attr_name} — it is jammed!")
            return
        if self._is_unlocking or self._is_locking:
            print(f"[JAM] Conflict detected while unlocking {self._attr_name}")
            self.jam()
            return
        if not self._is_locked:
            print(f"[INFO] {self._attr_name} is already unlocked.")
            return

        code = kwargs.get("code")
        print(f"[ASYNC] Unlocking {self._attr_name} with code: {code}")
        self._is_unlocking = True
        await asyncio.sleep(0.1)  # Simulate unlocking time
        self._is_locked = False
        self._is_unlocking = False

    def lock(self, **kwargs):
        """Synchronous lock (with jam detection)."""
        asyncio.run(self.async_lock(**kwargs))

    def unlock(self, **kwargs):
        """Synchronous unlock (with jam detection)."""
        asyncio.run(self.async_unlock(**kwargs))

def main():
    """Demonstration of MyLock usage."""
    my_lock = MyLock("Front Door")

    print(f"Initial state: Locked={my_lock.is_locked}, Jammed={my_lock.is_jammed}")
    my_lock.lock(code="1234")
    print(f"After lock: Locked={my_lock.is_locked}, Jammed={my_lock.is_jammed}")
    my_lock.unlock()
    print(f"After unlock: Locked={my_lock.is_locked}, Jammed={my_lock.is_jammed}")

    # Simulate jam during conflict
    async def conflict_demo():
        task1 = asyncio.create_task(my_lock.async_lock(code="1111"))
        task2 = asyncio.create_task(my_lock.async_unlock(code="2222"))
        await asyncio.gather(task1, task2)
        print(f"After conflict: Locked={my_lock.is_locked}, Jammed={my_lock.is_jammed}")

    asyncio.run(conflict_demo())

    # Clear jam
    my_lock.clear_jam()
    print(f"After clearing jam: Locked={my_lock.is_locked}, Jammed={my_lock.is_jammed}")

if __name__ == "__main__":
    main()
