import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from rich import print
from tqdm.rich import tqdm
from tqdm import TqdmExperimentalWarning
import time
import warnings
import google.api_core.exceptions

warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def analyze_codebase(repo_data, analysis_file='code_analysis.json'):
    # Check if the analysis file already exists
    if os.path.exists(analysis_file):
        print(f"[bold yellow]Using existing analysis from {analysis_file}...[/bold yellow]")
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        return analysis

    print(f"[bold green]No previous analysis found. Generating new analysis...[/bold green]")
    
    all_code = ""
    total_loc = 0  # Initialize a counter for total lines of code
    
    for file_path, file_info in repo_data.items():
        file_contents = file_info['contents']
        all_code += f"File: {file_path}\nContents:\n{file_contents}\n\n"
        
        # Count lines in the current file and add to total LOC
        file_loc = len(file_contents.splitlines())
        total_loc += file_loc
    
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

    # Add the total lines of code to the analysis dictionary
    analysis['total_loc'] = total_loc

    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, ensure_ascii=False, indent=4)

    return analysis

def send_gemini_request(prompt, retries=3):
    model = genai.GenerativeModel("gemini-1.5-flash")
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            return response
        except google.api_core.exceptions.ResourceExhausted as e:
            delay = 4 * (attempt + 1)
            print(f"[bold red]Resource exhausted on attempt {attempt + 1}/{retries}: {e}. Retrying in {delay} seconds...[/bold red]")
            time.sleep(delay)
    raise Exception("Max retries reached. Resource exhausted.")
