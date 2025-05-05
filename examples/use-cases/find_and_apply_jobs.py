import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY in your .env file")
    genai.configure(api_key=api_key)

def find_jobs():
    # Initialize the model
    model = genai.GenerativeModel('gemini-pro')
    
    # Example job search task
    task = """
    Help me find software engineering jobs:
    1. Search for entry-level software engineering positions
    2. Focus on remote positions
    3. List companies that are currently hiring
    4. Provide application tips
    5. Suggest ways to make applications stand out
    """
    
    try:
        response = model.generate_content(task)
        print("\nJob Search Results:")
        print("==================")
        print(response.text)
    except Exception as e:
        print(f"Error during job search: {str(e)}")

def get_application_tips():
    model = genai.GenerativeModel('gemini-pro')
    
    task = """
    Provide detailed tips for job applications:
    1. Resume optimization
    2. Cover letter writing
    3. Interview preparation
    4. Follow-up strategies
    5. Common mistakes to avoid
    """
    
    try:
        response = model.generate_content(task)
        print("\nApplication Tips:")
        print("================")
        print(response.text)
    except Exception as e:
        print(f"Error getting application tips: {str(e)}")

def main():
    print("Job Search and Application Assistant")
    print("===================================")
    
    try:
        setup_gemini()
        find_jobs()
        get_application_tips()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Please make sure you have set your GEMINI_API_KEY in the .env file")

if __name__ == "__main__":
    main() 