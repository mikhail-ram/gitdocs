import os
import google.generativeai as genai
from dotenv import load_dotenv
from rich import print

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def analyze_codebase(repo_data, analysis_file='code_analysis.txt'):
    # Check if the analysis file already exists
    if os.path.exists(analysis_file):
        print(f"[bold yellow]Using existing analysis from {analysis_file}...[/bold yellow]")
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_content = f.read()
        return parse_analysis_content(analysis_content)

    # If the file does not exist, generate a new code analysis
    print(f"[bold green]No previous analysis found. Generating new analysis...[/bold green]")
    all_code = ""
    for file_path, file_info in repo_data.items():
        all_code += f"File: {file_path}\nContents:\n{file_info['contents']}\n\n"
    
    # Dictionary to hold analysis
    analysis = {}
    analysis_text = ""

    for file_path, file_info in repo_data.items():
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

        # Append this analysis to the overall text
        analysis_text += f"Analysis for {file_path}:\n{file_analysis}\n\n"
    
    # Write the generated analysis to the file
    with open(analysis_file, 'w', encoding='utf-8') as f:
        f.write(analysis_text)

    return analysis

def send_gemini_request(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response

def parse_analysis_content(analysis_content):
    """
    Parses the text file's analysis content and converts it into the dictionary format
    used by the analysis function. 
    This assumes the content of the file is structured in a similar way to the analysis output.
    """
    analysis = {}
    # Split the file content into individual analyses based on the 'Analysis for' marker
    analysis_sections = analysis_content.split('Analysis for')
    
    for section in analysis_sections[1:]:  # Skip the first empty split
        lines = section.strip().split('\n')
        file_path = lines[0].strip()  # Extract file path from first line
        file_analysis = '\n'.join(lines[1:])  # The rest is the file analysis

        analysis[file_path] = {
            'file_name': os.path.basename(file_path),
            'file_analysis': file_analysis
        }

    return analysis
