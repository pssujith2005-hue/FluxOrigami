import os
from dotenv import load_dotenv
import google.generativeai as genai

# Force load the .env file right here
load_dotenv()

def generate_ui_code(prompt_text):
    # Configure the SDK with the key from your .env file
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Initialize the model (using the fast and efficient flash model)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # The System Prompt forces the AI to output only raw code, no chatty text
    system_instruction = """
    You are an expert UI/UX frontend developer. 
    The user will describe a UI component. 
    You must output ONLY valid HTML utilizing Tailwind CSS classes for styling.
    Do NOT include markdown formatting (like ```html), explanations, or any conversational text. 
    Return ONLY the raw HTML string.
    """
    
    full_prompt = f"{system_instruction}\n\nUser Request: {prompt_text}"
    
    try:
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"<div class='p-4 bg-red-100 text-red-700 rounded-md border border-red-300'>Error generating UI: {str(e)}</div>"