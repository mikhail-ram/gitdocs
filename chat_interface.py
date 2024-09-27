import os
import google.generativeai as genai
from dotenv import load_dotenv
from rich import print
from rich.markdown import Markdown

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

def run_chat_interface(analysis):
    print("[bold yellow]Interactive Chat Interface. Type 'exit' to quit.[/bold yellow]")
    while True:
        user_input = input("Ask me anything about the codebase: ")
        if user_input.lower() == "exit":
            break
        prompt = f"Based on the following project analysis:\n{analysis}\nAnswer this query: {user_input}"
        response = send_gemini_request(prompt)
        print(Markdown(response.text))

def send_gemini_request(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response
