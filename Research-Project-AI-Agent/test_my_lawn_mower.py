import pytest
from my_lawn_mower import MyLawnMower

@pytest.fixture
def mower():
    return MyLawnMower(name="Test Mower")

class TestMyLawnMower:

    # 1. Start Mowing from Docked
    def test_start_mowing_from_docked(self, mower):
        mower.start_mowing()
        assert mower.activity == "MOWING"

    # 2. Complete Mowing and Dock
    def test_complete_mowing_and_dock(self, mower):
        mower.start_mowing()
        mower.dock()
        assert mower.activity == "DOCKED"

    # 3. Return to Dock Manually
    def test_return_to_dock_manually(self, mower):
        mower.start_mowing()
        mower.return_to_dock()
        assert mower.activity == "RETURNING"

    # 4. Pause Mowing
    def test_pause_mowing(self, mower):
        mower.start_mowing()
        mower.pause()
        assert mower.activity == "PAUSED"

    # 5. Resume Mowing from Paused
    def test_resume_from_paused(self, mower):
        mower.start_mowing()
        mower.pause()
        mower.resume()
        assert mower.activity == "MOWING"

    # 6. Error while Mowing -> Sends response to LLM
    def test_error_while_mowing(self, mower, capsys):
        mower.start_mowing()
        mower.set_error("Blade jam detected")
        captured = capsys.readouterr()
        assert mower.activity == "ERROR"
        assert "Blade jam detected" in captured.out

    # 7. Error while Returning -> Sends response to LLM
    def test_error_while_returning(self, mower, capsys):
        mower.start_mowing()
        mower.return_to_dock()
        mower.set_error("Path blocked")
        captured = capsys.readouterr()
        assert mower.activity == "ERROR"
        assert "Path blocked" in captured.out

    # 8. Recover From Error -> Restarts on its own
    def test_recover_from_error(self, mower):
        mower.start_mowing()
        mower.set_error("Low blade speed")
        mower.clear_error()
        mower.start_mowing()  # Should restart automatically
        assert mower.activity == "MOWING"

    # 9. Pause While Returning
    def test_pause_while_returning(self, mower, capsys):
        mower.start_mowing()
        mower.return_to_dock()
        mower.pause()
        captured = capsys.readouterr()
        assert "cannot pause" in captured.out.lower()
        assert mower.activity == "RETURNING"

    # 10. Error While Paused
    def test_error_while_paused(self, mower):
        mower.start_mowing()
        mower.pause()
        mower.set_error("Motor overheated")
        assert mower.activity == "ERROR"

    # 11. Docking Interrupted by User
    def test_docking_interrupted_by_user(self, mower):
        mower.start_mowing()
        mower.return_to_dock()
        mower.start_mowing()  # User interrupts docking
        assert mower.activity in ["MOWING", "RETURNING"]
