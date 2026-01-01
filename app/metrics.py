import json
import uuid
from datetime import datetime, timezone

def record_metrics(todo, verification, duration):
    data = {
        "run_id": str(uuid.uuid4()),
        "todo": todo,
        "test_passed": verification["status"] == "pass",
        "failure_type": verification["failure_type"],
        "duration_seconds": duration,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    with open("agent_metrics.jsonl", "a") as f:
        f.write(json.dumps(data) + "\n")
