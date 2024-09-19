from flask import Flask, jsonify
from flask_cors import CORS
import git
import os
import json

app = Flask(__name__)

# Configure CORS to allow requests from any origin ('*')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Directory to clone the repository to
CLONE_DIR = os.path.join(os.getcwd(), "cloned_repo")

# Function to clone a GitHub repository
def clone_repo(token, repo_url, branch, dest_dir):
    """
    Clones a GitHub repository using GitPython.
    """
    # Format the repo URL with token authentication
    token_repo_url = repo_url.replace("https://", f"https://{token}@")

    # Remove the existing directory if it exists to ensure fresh clone
    if os.path.exists(dest_dir):
        print(f"Removing existing directory: {dest_dir}")
        os.system(f"rm -rf {dest_dir}")

    try:
        print(f"Cloning repository from {repo_url} (branch: {branch}) into {dest_dir}")
        git.Repo.clone_from(token_repo_url, dest_dir, branch=branch)
        print(f"Repository successfully cloned to {dest_dir}")
        return True
    except Exception as e:
        print(f"Error occurred while cloning the repository: {str(e)}")
        return False

# Function to load JSON file content from the cloned repository
def load_json_file(json_file_path):
    """
    Loads the content of a JSON file.
    """
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}")
        return None

# Route to check the status and clone a repo
@app.route("/status", methods=["GET"])
def status():
    # Hardcoded values for GitHub token, repo URL, branch, and destination directory
    token = os.getenv('GITHUB_TOKEN')  # Replace with your GitHub token
    repo_url = "https://github.com/yedhukrishnagirish/TiddlyProjectRepo"  # Replace with the repo URL
    branch = "main"  # Replace with your branch name (e.g., 'main', 'dev', etc.)
    json_file_path = os.path.join(CLONE_DIR, "Document Configuration", "configuration.json")

    # Clone the repository
    clone_success = clone_repo(token, repo_url, branch, CLONE_DIR)

    if not clone_success:
        return jsonify({"error": "Failed to clone repository"}), 500

    # Load JSON file content from the cloned repo
    status_data = load_json_file(json_file_path)

    if status_data is None:
        return jsonify({"error": "Failed to read configuration.json from cloned repository"}), 500

    # Return the JSON data as a response
    return jsonify(status_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
