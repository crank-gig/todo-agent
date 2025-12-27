import os
import re
import json
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()

VITE_GITHUB_ACCESS_TOKEN = os.getenv("VITE_GITHUB_ACCESS_TOKEN")
if not VITE_GITHUB_ACCESS_TOKEN:
    raise RuntimeError("VITE_GITHUB_ACCESS_TOKEN is not set")

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


def run_tests():
    result = subprocess.run(
        ["pytest"],
        capture_output=True,
        text=True
    )
    return result.stdout, result.returncode


def main():
    todo = extract_todo()

    if not todo:
        print("No TODO found.")
        return

    print(f"Found TODO: {todo}")

    code = ask_model(todo)
    print("\nGenerated code:\n", code)

    apply_patch(code)

    print("\nRunning tests...")
    output, exit_code = run_tests()
    print(output)

    if exit_code == 0:
        print("✓ Week 1 agent succeeded.")
    else:
        print("✗ Tests failed. Agent incomplete.")


if __name__ == "__main__":
    main()
