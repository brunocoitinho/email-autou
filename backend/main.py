from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import nltk
import os
import fitz  # PyMuPDF
from typing import Optional
from dotenv import load_dotenv

# --- Basic Setup ---
load_dotenv()
app = FastAPI()

# --- CORS Middleware ---
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Gemini API Key ---
# IMPORTANT: Set up your Gemini API key in a .env file.
# Create a .env file in the backend directory and add the following line:
# GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise HTTPException(status_code=500, detail="Gemini API key not configured. Please set the GEMINI_API_KEY environment variable.")

genai.configure(api_key=gemini_api_key)


import nltk
import os

# Point NLTK to the local nltk_data directory where 'punkt' is stored
# This is necessary for serverless environments like Vercel
nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
if os.path.exists(nltk_data_path):
    nltk.data.path.append(nltk_data_path)

# Configure Gemini API
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception as e:
    print(f"Error configuring Gemini: {e}")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# --- Pydantic Models ---
class EmailInput(BaseModel):
    email_text: str

class AnalysisResponse(BaseModel):
    category: str
    suggested_response: str

# --- Helper Functions ---

def get_gemini_suggestion(text: str) -> (str, str):
    """
    Uses Gemini to classify the email and generate a suggested response.
    The prompt is designed to handle emails in both English and Portuguese.
    """
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Analyze the following email, which can be in English or Portuguese.

        First, classify the email into one of two categories:
        - 'Productive': An email that requires a specific action, decision, or a detailed response.
        - 'Unproductive': An email that is informational, a simple confirmation, spam, or does not require a direct action.

        Second, based on the content and language of the email, suggest a brief, polite, and professional response.
        - If the email is in Portuguese, the response must be in Brazilian Portuguese.
        - If the email is in English, the response must be in English.

        Email to analyze:
        ---
        {text}
        ---

        Provide the output in a clear, structured format. Follow this template exactly:
        Category: [Productive/Unproductive]
        Suggested Response: [Your suggested response here]
        """

        response = model.generate_content(prompt)
        
        # Basic parsing of the model's response
        ai_response = response.text.strip()
        
        category = "Unknown"
        suggested_response = "Could not generate a suggestion."

        lines = ai_response.split('\n')
        
        if lines and lines[0].startswith("Category:"):
            category_text = lines[0].replace("Category:", "").strip()
            if "Productive" in category_text:
                category = "Productive"
            elif "Unproductive" in category_text:
                category = "Unproductive"

        # Find the start of the suggested response
        response_start_index = -1
        for i, line in enumerate(lines):
            if line.startswith("Suggested Response:"):
                response_start_index = i
                break

        if response_start_index != -1:
            # Get the first line of the response and remove the prefix
            first_line = lines[response_start_index].replace("Suggested Response:", "").strip()
            # Get the rest of the lines
            remaining_lines = lines[response_start_index + 1:]
            # Join them all together
            full_response = [first_line] + remaining_lines
            suggested_response = "\n".join(full_response).strip()

        return category, suggested_response

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error communicating with Gemini: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the email with the AI model.")


# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "AutoU Email Analysis API is running."}


@app.post("/process-email", response_model=AnalysisResponse)
async def process_email(email_input: EmailInput):
    """
    Receives email text, processes it, and returns classification and suggestion.
    """
    category, suggested_response = get_gemini_suggestion(email_input.email_text)
    
    return AnalysisResponse(category=category, suggested_response=suggested_response)


@app.post("/upload-file", response_model=AnalysisResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Receives a file (.txt or .pdf), extracts text, and returns analysis.
    """
    contents = await file.read()
    text = ""
    
    if file.filename.endswith('.txt'):
        text = contents.decode('utf-8')
    elif file.filename.endswith('.pdf'):
        try:
            pdf_document = fitz.open(stream=contents, filetype="pdf")
            for page in pdf_document:
                text += page.get_text()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF file: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload .txt or .pdf files.")

    category, suggested_response = get_gemini_suggestion(text)
    
    return AnalysisResponse(category=category, suggested_response=suggested_response)

# --- To run this application ---
# 1. Make sure you have the libraries from requirements.txt installed.
# 2. Create a .env file in this directory with your GEMINI_API_KEY.
# 3. Run in your terminal: uvicorn main:app --reload