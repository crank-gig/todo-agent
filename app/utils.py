import os
import requests

def ask_groq(todo):
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

def ask_anthropic(todo):
    prompt = f"""
    Write ONLY the Python code needed to fix this TODO.

    TODO: {todo}

    Rules:
    - Output only valid Python code
    - No markdown
    - No explanation
    """

    url = "https://api.anthropic.com/v1/messages"

    headers = {
        "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    payload = {
        "model": "claude-3-5-sonnet-20240620",
        "max_tokens": 500,
        "temperature": 0.2,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

def ask_github(todo):
    prompt = f"""
Write ONLY the Python code needed to fix this TODO.

TODO: {todo}

Rules:
- Output only valid Python code
- No markdown
- No explanation
"""

    url = "https://models.inference.ai.azure.com/chat/completions"

    headers = {
        "Authorization": f"Bearer {os.getenv("VITE_GITHUB_ACCESS_TOKEN")}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4.1-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]


def ask_model(todo):
    prompt = f"""
    Write ONLY the Python code needed to fix this TODO.

    TODO: {todo}

    Rules:
    - Output only valid Python code
    - No markdown
    - No explanation
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    headers = {
        "Authorization": f"Bearer {os.getenv("OPENROUTER_API_KEY")}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Week1-Hello-Agent"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]