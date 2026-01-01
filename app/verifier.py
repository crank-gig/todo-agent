import re

def classify_failure(test_output: str):
    patterns = {
        "SyntaxError": r"SyntaxError",
        "ImportError": r"ImportError|ModuleNotFoundError",
        "AssertionError": r"AssertionError",
        "Timeout": r"Timeout|timed out"
    }

    for failure, pattern in patterns.items():
        if re.search(pattern, test_output):
            return failure

    return "Unknown"


def verify(test_result):
    if test_result["exit_code"] == 0:
        return {
            "status": "pass",
            "failure_type": None
        }

    failure_type = classify_failure(
        test_result["stdout"] + test_result["stderr"]
    )

    return {
        "status": "fail",
        "failure_type": failure_type
    }