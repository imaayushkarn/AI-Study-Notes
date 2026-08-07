from flask import Flask, request, jsonify, render_template
from google import genai
import PyPDF2
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_notes():
    text_content = ""
    
    # 1. Check if PDF is uploaded
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            try:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
            except Exception as e:
                return jsonify({"error": "Failed to read PDF."}), 400
    
    # 2. Check for pasted text if no PDF is used
    if not text_content and 'text' in request.form:
        text_content = request.form['text']
        
    if not text_content.strip():
        return jsonify({"error": "Please paste text or upload a valid PDF file."}), 400

    try:
        # 3. Securely grab the API key from Vercel
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return jsonify({"error": "Server error: API Key is missing in Vercel settings."}), 500
             
        # 4. Use the NEW Google GenAI Client
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert teacher. Read the given study material.
        Generate:
        1. Short Summary
        2. Important Points
        3. Important Definitions
        4. 15 Viva Questions
        5. 10 MCQs
        6. Flashcards
        7. Keywords
        8. One-day Revision Plan
        
        Format the response using clear HTML tags (like <h2>, <ul>, <li>, <p>, <strong>) so it looks beautiful on a webpage. Do NOT include ```html markdown blocks.
        
        Study Material:
        {text_content}
        """
        
        # Call the latest Gemini model using the new syntax
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        return jsonify({"result": response.text})
    
    except Exception as e:
        # Printing the exact error to the Vercel logs if it fails again
        print(f"Backend Crash: {e}") 
        return jsonify({"error": "AI Generation Failed. Make sure your API key is correct and valid."}), 500

if __name__ == '__main__':
    app.run(debug=True)from flask import Flask, request, jsonify, render_template
from google import genai
import PyPDF2
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_notes():
    text_content = ""
    
    # 1. Check if PDF is uploaded
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            try:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
            except Exception as e:
                return jsonify({"error": "Failed to read PDF."}), 400
    
    # 2. Check for pasted text if no PDF is used
    if not text_content and 'text' in request.form:
        text_content = request.form['text']
        
    if not text_content.strip():
        return jsonify({"error": "Please paste text or upload a valid PDF file."}), 400

    try:
        # 3. Securely grab the API key from Vercel
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return jsonify({"error": "Server error: API Key is missing in Vercel settings."}), 500
             
        # 4. Use the NEW Google GenAI Client
        client = genai.Client(api_key=api_key)
        
        prompt = f"""
        You are an expert teacher. Read the given study material.
        Generate:
        1. Short Summary
        2. Important Points
        3. Important Definitions
        4. 15 Viva Questions
        5. 10 MCQs
        6. Flashcards
        7. Keywords
        8. One-day Revision Plan
        
        Format the response using clear HTML tags (like <h2>, <ul>, <li>, <p>, <strong>) so it looks beautiful on a webpage. Do NOT include ```html markdown blocks.
        
        Study Material:
        {text_content}
        """
        
        # Call the latest Gemini model using the new syntax
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt
        )
        return jsonify({"result": response.text})
    
    except Exception as e:
        # Printing the exact error to the Vercel logs if it fails again
        print(f"Backend Crash: {e}") 
        return jsonify({"error": "AI Generation Failed. Make sure your API key is correct and valid."}), 500

if __name__ == '__main__':
    app.run(debug=True)
