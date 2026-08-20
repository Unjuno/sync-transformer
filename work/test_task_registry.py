import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sync_experiments.tasks import TASKS, get_task

def test_registry_has_ten_unique_tasks_and_two_tracks():
    assert len(TASKS) == 10
    assert len({t.task_id for t in TASKS}) == 10
    assert {t.track for t in TASKS} == {"forecasting", "trajectory"}

def test_ett_is_the_only_validated_task():
    assert get_task("ett").status == "validated_cpu"
    assert all(t.status != "validated_cpu" for t in TASKS if t.task_id != "ett")
