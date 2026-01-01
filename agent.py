import os
import re
import time
import requests
import subprocess
from dotenv import load_dotenv

from app.verifier import verify
from app.metrics import record_metrics

load_dotenv()

FILE_PATH = "app/main.py"

def extract_todo():
    with open(FILE_PATH, "r") as f:
        content = f.read()

    match = re.search(r"# TODO:(.*)", content)
    return match.group(1).strip() if match else None


def ask_model(todo):
    prompt = f"""
    Write ONLY the Python code needed to fix this TODO.

    TODO: {todo}

    Rules:
    - Output only valid Python code
    - No markdown
    - No explanation
    """

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 400
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def apply_patch(code):
    with open(FILE_PATH, "a") as f:
        f.write("\n" + code + "\n")


def run_tests_in_docker():
    result = subprocess.run(
        [
            "docker", "run", "--rm",
            "-v", f"{os.getcwd()}:/workspace",
            "crankgig/todo-agent-sandbox"
        ],
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr, result.returncode


def run_tests():
    stdout, stderr, exit_code = run_tests_in_docker()
    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code
    }



def main():
    start = time.time()

    todo = extract_todo()
    if not todo:
        print("No TODO found.")
        return

    print(f"Found TODO: {todo}")

    code = ask_model(todo)
    apply_patch(code)

    test_result = run_tests()
    verification = verify(test_result)

    duration = round(time.time() - start, 2)
    record_metrics(todo, verification, duration)

    if verification["status"] == "pass":
        print("✓ Agent succeeded.")
    else:
        print(f"✗ Agent failed ({verification['failure_type']})")



if __name__ == "__main__":
    main()
