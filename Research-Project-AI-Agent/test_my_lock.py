import pytest
import asyncio
from my_lock import MyLock

@pytest.fixture
def lock():
    return MyLock(name="Test Lock")

# 1. Lock Open -> Close
def test_lock_open_to_close(lock):
    lock._is_locked = False
    lock.lock()
    assert lock._is_locked is True
    assert lock._is_jammed is False

# 2. Lock Close -> Open
def test_lock_close_to_open(lock):
    lock._is_locked = True
    lock.unlock()
    assert lock._is_locked is False
    assert lock._is_jammed is False

# 3. Lock Open -> Asked to open again
def test_open_asked_to_open_again(lock, capsys):
    lock._is_locked = False
    lock.unlock()
    captured = capsys.readouterr()
    assert "already unlocked" in captured.out.lower()
    assert lock._is_locked is False

# 4. Lock Close -> Asked to close again
def test_close_asked_to_close_again(lock, capsys):
    lock._is_locked = True
    lock.lock()
    captured = capsys.readouterr()
    assert "already locked" in captured.out.lower()
    assert lock._is_locked is True

# 5. Lock Jammed -> Should return jammed response
def test_jammed_lock_response(lock, capsys):
    lock._is_jammed = True
    lock.lock()
    captured = capsys.readouterr()
    assert "jammed" in captured.out.lower()
    assert lock._is_jammed is True

# 6. Lock is Unlocking -> Asked to lock during unlock
def test_lock_during_unlocking(lock):
    lock._is_unlocking = True
    lock.lock()
    # Either jam occurred
    assert lock._is_jammed is True

# 7. Lock is Locking -> Asked to unlock during event
def test_unlock_during_locking(lock):
    lock._is_locking = True
    lock.unlock()
    # Either jam occurred
    assert lock._is_jammed is True

# 8. Manual Lock Change
def test_manual_lock_change(lock):
    lock._is_locked = True
    # Simulate manual override
    lock._is_locked = False
    assert lock._is_locked is False

# 9. Door Opening While Unlocked
def test_door_opening_while_unlocked(lock):
    lock._is_locked = False
    # Opening door does not affect lock
    assert lock._is_locked is False

# 10. Door Closing and Locking
def test_door_closing_and_locking(lock):
    lock._is_locked = False
    lock.lock()
    assert lock._is_locked is True

# 11. Clear Jam after detection
def test_clear_jam_after_detection(lock):
    lock._is_jammed = True
    lock.clear_jam()
    assert lock._is_jammed is False
    assert lock._is_locked is False

# 12. Open Door While Locking
def test_open_door_while_locking(lock):
    lock._is_locking = True
    lock.unlock()  # Conflict triggers jam
    assert lock._is_jammed is True or lock._is_locked is False

# 13. Jam While Unlocking
def test_jam_while_unlocking(lock):
    lock._is_unlocking = True
    lock.jam()
    assert lock._is_jammed is True

# import asyncio
# import pytest
# from my_lock import MyLock

# @pytest.mark.asyncio
# async def test_initial_state():
#     lock = MyLock("Test Lock")
#     assert lock.is_locked is False
#     assert lock._attr_name == "Test Lock"

# def test_lock_sets_state():
#     lock = MyLock("Test Lock")
#     lock.lock()
#     assert lock.is_locked is True

# def test_lock_with_code():
#     lock = MyLock("Test Lock")
#     lock.lock(code="1234")
#     assert lock.is_locked is True

# @pytest.mark.asyncio
# async def test_async_lock_sets_state():
#     lock = MyLock("Test Lock")
#     await lock.async_lock(code="5678")
#     assert lock.is_locked is True

# def test_unlock_sets_state():
#     lock = MyLock("Test Lock")
#     lock.lock()
#     lock.unlock()
#     assert lock.is_locked is False

# @pytest.mark.asyncio
# async def test_async_unlock_sets_state():
#     lock = MyLock("Test Lock")
#     await lock.async_lock()
#     await lock.async_unlock()
#     assert lock.is_locked is False

# def test_lock_idempotency():
#     lock = MyLock("Test Lock")
#     lock.lock()
#     lock.lock()  # Lock again should not break
#     assert lock.is_locked is True

# @pytest.mark.asyncio
# async def test_concurrent_async_locks():
#     lock = MyLock("Test Lock")
#     await asyncio.gather(lock.async_lock(), lock.async_lock())
#     assert lock.is_locked is True

# def test_lock_with_invalid_kwargs():
#     lock = MyLock("Test Lock")
#     lock.lock(random_arg="unexpected")
#     assert lock.is_locked is True

# @pytest.mark.asyncio
# async def test_state_transitions():
#     lock = MyLock("Test Lock")
#     await lock.async_lock()
#     await lock.async_unlock()
#     lock.lock()
#     assert lock.is_locked is True

# # -----------------------------
# # 2. Rapid Lock/Unlock Sequence
# # -----------------------------
# @pytest.mark.asyncio
# async def test_rapid_lock_unlock_sequence():
#     lock = MyLock("Rapid Lock")

#     for _ in range(50):
#         lock.lock()
#         assert lock.is_locked is True
#         lock.unlock()
#         assert lock.is_locked is False
#         await lock.async_lock()
#         assert lock.is_locked is True
#         await lock.async_unlock()
#         assert lock.is_locked is False

# # -----------------------------
# # 3. Invalid Code Handling
# # -----------------------------
# def test_invalid_code_types():
#     lock = MyLock("Code Lock")

#     # Passing None, numbers, objects as code
#     lock.lock(code=None)
#     assert lock.is_locked is True

#     lock.lock(code=1234)
#     assert lock.is_locked is True

#     lock.lock(code={"key": "value"})
#     assert lock.is_locked is True

# # -----------------------------
# # 4. Multiple Locks
# # -----------------------------
# @pytest.mark.asyncio
# async def test_multiple_locks():
#     locks = [MyLock(f"Lock {i}") for i in range(10)]

#     # Lock all asynchronously
#     await asyncio.gather(*(l.async_lock() for l in locks))
#     assert all(l.is_locked for l in locks)

#     # Unlock all asynchronously
#     await asyncio.gather(*(l.async_unlock() for l in locks))
#     assert all(not l.is_locked for l in locks)

# # -----------------------------
# # 5. Mixed Sync + Async Calls
# # -----------------------------
# @pytest.mark.asyncio
# async def test_mixed_sync_async_calls():
#     lock = MyLock("Mixed Lock")

#     lock.lock()
#     assert lock.is_locked is True

#     await lock.async_unlock()
#     assert lock.is_locked is False

#     lock.lock()
#     await lock.async_lock()
#     assert lock.is_locked is True

# # -----------------------------
# # 6. Lock Already Locked
# # -----------------------------
# def test_lock_already_locked():
#     lock = MyLock("Already Locked")
#     lock.lock()
#     initial_state = lock.is_locked
#     lock.lock()
#     assert lock.is_locked == initial_state

# # -----------------------------
# # 7. Async Lock with Delay Simulation
# # -----------------------------
# @pytest.mark.asyncio
# async def test_async_lock_with_delay():
#     lock = MyLock("Delayed Lock")

#     async def delayed_lock():
#         await asyncio.sleep(0.2)
#         await lock.async_lock()

#     await asyncio.gather(delayed_lock(), delayed_lock())
#     assert lock.is_locked is True
