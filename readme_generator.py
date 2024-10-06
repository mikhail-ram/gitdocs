import os
import google.generativeai as genai
from dotenv import load_dotenv
from rich import print

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def generate_readme(analysis, repo_root_dir):
    project_overview = ""
    for file_path, file_info in analysis.items():
        project_overview += file_info['file_analysis'] + "\n"

    prompt = f"Generate a comprehensive README for the following project:\n{project_overview}"
    response = send_gemini_request(prompt)

    # Path to the README file in the root of the repo
    readme_path = os.path.join(repo_root_dir, 'README.md')

    # Overwrite the README.md file
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
        f.write("\n\n---\nGenerated with ❤️ using [GitDocs](https://github.com/mikhail-ram/gitdocs).")
    print(f"[bold green]README.md generated successfully at {readme_path}![/bold green]")

def send_gemini_request(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response
