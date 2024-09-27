import os
import google.generativeai as genai
from dotenv import load_dotenv
from rich import print

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def generate_docstrings(analysis):
    for file_path, file_info in analysis.items():
        code_analysis = file_info['file_analysis']
        file_extension = os.path.splitext(file_path)[1]  # Get the file extension (e.g., .py, .js, .hs)

        prompt = f"""
        You are given a code file with extension '{file_extension}'. The file has already been analyzed for its structure and functionality. 
        Based on the following analysis, generate descriptive and detailed docstrings or comments for all the functions, classes, 
        and important sections in the code. Use the correct syntax and conventions for the programming language associated with the 
        file extension '{file_extension}' to insert the docstrings or comments.

        However, if the file extension '{file_extension}' is not a programming language (e.g., '.gitignore', 'LICENSE', etc.), 
        do not add any docstrings or comments and return the original file contents unchanged.

        Ensure that each docstring or comment provides information about the parameters, return types, exceptions raised, and usage examples. 
        The output should be the entire code file with the generated docstrings/comments inserted in the appropriate locations.
        
        Analysis:
        {code_analysis}
        """

        response = send_gemini_request(prompt)

        # Remove the backticks from the LLM response if they exist
        lines = response.text.strip().split('\n')
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1] == "```":
            lines = lines[:-1]
        enriched_code = "\n".join(lines)

        # Write the updated code back into the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(enriched_code)
        print(f"[bold green]Docstrings/comments added to {file_path}[/bold green]")

def send_gemini_request(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response
