import argparse
from repository_scraper import clone_and_scrape_repo
from code_analyzer import analyze_codebase
from docstring_generator import generate_docstrings
from readme_generator import generate_readme
from chat_interface import run_chat_interface

def main():
    parser = argparse.ArgumentParser(description="GitHub Documentation & Code Generation Tool")
    parser.add_argument('repo_url', type=str, help='GitHub repository URL to analyze.')
    parser.add_argument('--generate-readme', action='store_true', help='Generate README file.')
    parser.add_argument('--generate-docstrings', action='store_true', help='Generate docstrings for the codebase.')
    parser.add_argument('--chat', action='store_true', help='Start chat-based interface.')

    args = parser.parse_args()

    repo_data = clone_and_scrape_repo(args.repo_url)
    analysis = analyze_codebase(repo_data)

    repo_root_dir = args.repo_url.split('/')[-1].replace('.git', '')

    if args.generate_readme:
        generate_readme(analysis, repo_root_dir)  # Pass the root directory for README placement

    if args.generate_docstrings:
        generate_docstrings(analysis)

    if args.chat:
        run_chat_interface(analysis)

if __name__ == "__main__":
    main()
