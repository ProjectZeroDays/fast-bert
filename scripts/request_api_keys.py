import os
import requests
import json

def request_openai_api_key(email, password):
    url = "https://api.openai.com/v1/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json()["api_key"]
    else:
        raise Exception("Failed to obtain OpenAI API key")

def request_huggingface_api_key(email, password):
    url = "https://huggingface.co/api/auth/login"
    payload = {
        "email": email,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json()["api_key"]
    else:
        raise Exception("Failed to obtain HuggingFace API key")

def request_github_api_key(username, password):
    url = "https://api.github.com/authorizations"
    payload = {
        "scopes": ["repo", "user"],
        "note": "API key for accessing GitHub"
    }
    response = requests.post(url, auth=(username, password), data=json.dumps(payload))
    if response.status_code == 201:
        return response.json()["token"]
    else:
        raise Exception("Failed to obtain GitHub API key")

def store_api_key(service, api_key):
    with open(f"{service}_api_key.txt", "w") as file:
        file.write(api_key)

if __name__ == "__main__":
    openai_email = os.getenv("OPENAI_EMAIL")
    openai_password = os.getenv("OPENAI_PASSWORD")
    huggingface_email = os.getenv("HUGGINGFACE_EMAIL")
    huggingface_password = os.getenv("HUGGINGFACE_PASSWORD")
    github_username = os.getenv("GITHUB_USERNAME")
    github_password = os.getenv("GITHUB_PASSWORD")

    openai_api_key = request_openai_api_key(openai_email, openai_password)
    store_api_key("openai", openai_api_key)

    huggingface_api_key = request_huggingface_api_key(huggingface_email, huggingface_password)
    store_api_key("huggingface", huggingface_api_key)

    github_api_key = request_github_api_key(github_username, github_password)
    store_api_key("github", github_api_key)
