import os
import git
from rich import print

# Load the list of code file extensions from an external file
def load_code_extensions(file_path="code_extensions.txt"):
    with open(file_path, 'r') as f:
        extensions = {line.strip() for line in f if line.strip()}
    return extensions

CODE_FILE_EXTENSIONS = load_code_extensions()

def clone_and_scrape_repo(repo_url):
    # Extract repo name from the URL
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    
    # Check if the repo directory already exists
    if not os.path.exists(repo_name):
        print(f"[bold green]Cloning repository {repo_name}...[/bold green]")
        git.Repo.clone_from(repo_url, repo_name)
    else:
        print(f"[bold yellow]Using existing repository {repo_name}...[/bold yellow]")

    # Dictionary to hold the repository's data
    repo_data = {}

    # Walk through the repo directory recursively
    for root, dirs, files in os.walk(repo_name):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            # Only include files with valid code extensions
            if file_extension in CODE_FILE_EXTENSIONS:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    contents = f.read()

                repo_data[file_path] = {
                    'file_name': file,
                    'file_type': file_extension,
                    'contents': contents
                }

    return repo_data
