import os
import openai
import requests
import json
from bs4 import BeautifulSoup
from github import Github

# Set up OpenAI API keys
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_code_from_text(text):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"Extract code from the following text:\n{text}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def extract_code_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    return extract_code_from_text(text)

def extract_code_from_image(image_path):
    # Implement OCR to extract text from image
    pass

def extract_code_from_pdf(pdf_path):
    # Implement PDF text extraction
    pass

def extract_code_from_sources(sources):
    code_snippets = []
    for source in sources:
        if source.startswith("http"):
            code_snippets.append(extract_code_from_url(source))
        elif source.endswith(".pdf"):
            code_snippets.append(extract_code_from_pdf(source))
        elif source.endswith((".png", ".jpg", ".jpeg")):
            code_snippets.append(extract_code_from_image(source))
        else:
            with open(source, 'r') as file:
                text = file.read()
                code_snippets.append(extract_code_from_text(text))
    return code_snippets

def finish_code_with_autogpt(code_snippets):
    finished_code = []
    for snippet in code_snippets:
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Finish the following code:\n{snippet}",
            max_tokens=150
        )
        finished_code.append(response.choices[0].text.strip())
    return finished_code

def push_to_github(repo_name, files):
    github_token = os.getenv("GITHUB_API_KEY")
    g = Github(github_token)
    user = g.get_user()
    repo = user.create_repo(repo_name)
    for file_name, content in files.items():
        repo.create_file(file_name, "Add file", content)

def push_to_huggingface(repo_name, files):
    hf_token = os.getenv("HUGGINGFACE_API_KEY")
    headers = {"Authorization": f"Bearer {hf_token}"}
    for file_name, content in files.items():
        response = requests.post(
            f"https://huggingface.co/api/repos/create",
            headers=headers,
            json={"name": repo_name, "private": False}
        )
        if response.status_code == 201:
            repo_url = response.json()["url"]
            response = requests.put(
                f"{repo_url}/blob/main/{file_name}",
                headers=headers,
                data=content
            )
            if response.status_code != 200:
                raise Exception(f"Failed to upload {file_name} to HuggingFace")

def automate_dev_projects(sources, repo_name):
    code_snippets = extract_code_from_sources(sources)
    finished_code = finish_code_with_autogpt(code_snippets)
    files = {f"file_{i}.py": code for i, code in enumerate(finished_code)}
    push_to_github(repo_name, files)
    push_to_huggingface(repo_name, files)

if __name__ == "__main__":
    sources = ["example.txt", "https://example.com", "example.pdf", "example.png"]
    repo_name = "automated_dev_project"
    automate_dev_projects(sources, repo_name)
