import os
import json  # Import json module
import google.generativeai as genai
from dotenv import load_dotenv
from rich import print
from tqdm.rich import tqdm
from tqdm import TqdmExperimentalWarning
import warnings

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def analyze_codebase(repo_data, analysis_file='code_analysis.json'):  # Update file extension to .json
    # Check if the analysis file already exists
    if os.path.exists(analysis_file):
        print(f"[bold yellow]Using existing analysis from {analysis_file}...[/bold yellow]")
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)  # Load analysis from JSON
        return analysis

    # If the file does not exist, generate a new code analysis
    print(f"[bold green]No previous analysis found. Generating new analysis...[/bold green]")
    all_code = ""
    for file_path, file_info in repo_data.items():
        all_code += f"File: {file_path}\nContents:\n{file_info['contents']}\n\n"
    
    # Dictionary to hold analysis
    analysis = {}

    for file_path, file_info in tqdm(repo_data.items(), desc="Analyzing files", unit="file"):
        code = file_info['contents']
        prompt = f"""
        You are given a {file_info['file_type']} file as part of a larger project. 
        The entire codebase consists of multiple files, as described below.
        Perform an in-depth analysis of this file, including its purpose, functionality, and code structure.
        Additionally, perform a cross-file analysis by considering how this file interacts with other files in the codebase. 
        Use this context to infer any dependencies, relationships, or integrations between functions, classes, or modules.
        
        Entire codebase:
        {all_code}
        
        Analyze the file:
        {code}
        """

        response = send_gemini_request(prompt)
        file_analysis = response.text

        analysis[file_path] = {
            'file_name': file_info['file_name'],
            'file_analysis': file_analysis
        }

    # Write the generated analysis to the JSON file
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=4)  # Write analysis as JSON

    return analysis

def send_gemini_request(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response
