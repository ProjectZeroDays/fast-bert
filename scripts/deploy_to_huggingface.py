import os
import subprocess

def deploy_to_huggingface():
    # Set the path to the Gradio app
    app_path = "app.py"

    # Set the HuggingFace repository details
    hf_repo_url = os.getenv("HF_REPO_URL")
    hf_repo_branch = os.getenv("HF_REPO_BRANCH", "main")

    # Clone the HuggingFace repository
    subprocess.run(["git", "clone", hf_repo_url, "hf_repo"], check=True)

    # Copy the Gradio app to the repository
    subprocess.run(["cp", app_path, "hf_repo/app.py"], check=True)

    # Change directory to the repository
    os.chdir("hf_repo")

    # Add the changes to the repository
    subprocess.run(["git", "add", "app.py"], check=True)

    # Commit the changes
    subprocess.run(["git", "commit", "-m", "Deploy Gradio app"], check=True)

    # Push the changes to the repository
    subprocess.run(["git", "push", "origin", hf_repo_branch], check=True)

if __name__ == "__main__":
    deploy_to_huggingface()
