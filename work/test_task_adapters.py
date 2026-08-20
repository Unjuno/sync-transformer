import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from sync_experiments.adapters import AdapterNotReady, PendingAdapter, adapter_for

def test_pending_adapter_fails_explicitly():
    with pytest.raises(AdapterNotReady):
        PendingAdapter("traffic", "METR-LA").load()

def test_ett_adapter_is_selected():
    assert adapter_for("ett", "outputs").task_id == "ett"
