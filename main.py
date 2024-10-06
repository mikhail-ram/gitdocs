# TODO: Add code to approve or reject docstring edits
import argparse
from rich import print
from repository_scraper import scrape_repo
from code_analyzer import analyze_codebase
from docstring_generator import generate_docstrings
from readme_generator import generate_readme
from chat_interface import run_chat_interface

def main():
    parser = argparse.ArgumentParser(description="GitHub Documentation & Code Generation Tool")
    parser.add_argument('repo_source', type=str, help='GitHub repository URL to analyze.')
    parser.add_argument('--branch', type=str, help='Specify a Git branch to scrape.', default=None)
    parser.add_argument('--generate-readme', action='store_true', help='Generate README file.')
    parser.add_argument('--generate-docstrings', action='store_true', help='Generate docstrings for the codebase.')
    parser.add_argument('--chat', action='store_true', help='Start chat-based interface.')

    args = parser.parse_args()

    repo_root_dir, repo_data = scrape_repo(args.repo_source, branch=args.branch)

    # Check if repo_data is empty before proceeding with analysis
    if not repo_data:
        print(f"[bold red]Error: No valid code files to analyze in the repository.[/bold red]")
        return

    analysis = analyze_codebase(repo_data)

    if args.generate_readme:
        generate_readme(analysis, repo_root_dir)

    if args.generate_docstrings:
        generate_docstrings(analysis)

    if args.chat:
        run_chat_interface(analysis)

if __name__ == "__main__":
    main()
