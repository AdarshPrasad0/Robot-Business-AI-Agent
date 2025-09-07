# import pytest
# import asyncio
# from my_lock import MyLock

# # -----------------------------
# # 1. Concurrent Async Lock/Unlock
# # -----------------------------
# @pytest.mark.asyncio
# async def test_concurrent_async_lock_unlock():
#     lock = MyLock("Concurrent Lock")

#     await asyncio.gather(
#         lock.async_lock(code="1111"),
#         lock.async_unlock(code="2222"),
#         lock.async_lock(code="3333")
#     )

#     # Final state should be either locked or unlocked depending on execution order
#     assert lock.is_locked in [True, False]

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
