import os
import git
from rich import print

# Load the list of code file extensions from an external file
def load_code_extensions(file_path="code_extensions.txt"):
    with open(file_path, 'r') as f:
        extensions = {line.strip() for line in f if line.strip()}
    return extensions

CODE_FILE_EXTENSIONS = load_code_extensions()

def scrape_repo(repo_source, branch=None):
    # Check if the source is a GitHub URL or a local folder
    if repo_source.endswith('.git'):
        # If it's a GitHub URL, clone the repository
        repo_name = repo_source.split('/')[-1].replace('.git', '')

        # Check if the repo directory already exists
        if not os.path.exists(repo_name):
            print(f"[bold green]Cloning repository {repo_name}...[/bold green]")
            repo = git.Repo.clone_from(repo_source, repo_name, branch=branch)
        else:
            print(f"[bold yellow]Using existing repository {repo_name}...[/bold yellow]")
            repo = git.Repo(repo_name)

        # If a branch is specified, check it out
        if branch:
            print(f"[bold green]Checking out branch: {branch}...[/bold green]")
            repo.git.checkout(branch)
        else:
            # If no branch is specified, ensure the default branch is checked out
            branch = repo.git.rev_parse('--abbrev-ref', 'HEAD')
            print(f"[bold green]Using default branch: {branch}[/bold green]")

    elif os.path.isdir(repo_source):
        # If it's a local folder, use it directly
        print(f"[bold yellow]Using local directory {repo_source}...[/bold yellow]")
        repo_name = repo_source
    else:
        print(f"[bold red]Error: Invalid repository source. Please provide a valid GitHub URL or local folder path.[/bold red]")
        return None, {}

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

    return repo_name, repo_data
