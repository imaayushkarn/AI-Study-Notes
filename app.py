import os
import requests
from flask import Flask, request, jsonify, render_template
import PyPDF2

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
    
    # 2. Check for pasted text
    if not text_content and 'text' in request.form:
        text_content = request.form['text']
        
    if not text_content.strip():
        return jsonify({"error": "Please paste text or upload a valid PDF file."}), 400

    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return jsonify({"error": "Server error: API Key is missing in Vercel settings."}), 500
             
        # 3. DIRECT HTTP REQUEST (Bypasses Vercel's SDK limits)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        
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
        
        Format the response using clear HTML tags (like <h2>, <ul>, <li>, <p>, <strong>). Do NOT include ```html markdown blocks.
        
        Study Material:
        {text_content}
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        # Send to Gemini
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code != 200:
            return jsonify({"error": f"API Error: {response_data}"}), 500
            
        # Extract the text from the JSON response
        generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
        
        return jsonify({"result": generated_text})
    
    except Exception as e:
        print(f"Backend Crash: {e}") 
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)import os
import requests
from flask import Flask, request, jsonify, render_template
import PyPDF2

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
    
    # 2. Check for pasted text
    if not text_content and 'text' in request.form:
        text_content = request.form['text']
        
    if not text_content.strip():
        return jsonify({"error": "Please paste text or upload a valid PDF file."}), 400

    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return jsonify({"error": "Server error: API Key is missing in Vercel settings."}), 500
             
        # 3. DIRECT HTTP REQUEST (Bypasses Vercel's SDK limits)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        
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
        
        Format the response using clear HTML tags (like <h2>, <ul>, <li>, <p>, <strong>). Do NOT include ```html markdown blocks.
        
        Study Material:
        {text_content}
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        # Send to Gemini
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code != 200:
            return jsonify({"error": f"API Error: {response_data}"}), 500
            
        # Extract the text from the JSON response
        generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
        
        return jsonify({"result": generated_text})
    
    except Exception as e:
        print(f"Backend Crash: {e}") 
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)import os
import requests
from flask import Flask, request, jsonify, render_template
import PyPDF2

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
    
    # 2. Check for pasted text
    if not text_content and 'text' in request.form:
        text_content = request.form['text']
        
    if not text_content.strip():
        return jsonify({"error": "Please paste text or upload a valid PDF file."}), 400

    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return jsonify({"error": "Server error: API Key is missing in Vercel settings."}), 500
             
        # 3. DIRECT HTTP REQUEST (Bypasses Vercel's SDK limits)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        
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
        
        Format the response using clear HTML tags (like <h2>, <ul>, <li>, <p>, <strong>). Do NOT include ```html markdown blocks.
        
        Study Material:
        {text_content}
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        # Send to Gemini
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code != 200:
            return jsonify({"error": f"API Error: {response_data}"}), 500
            
        # Extract the text from the JSON response
        generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
        
        return jsonify({"result": generated_text})
    
    except Exception as e:
        print(f"Backend Crash: {e}") 
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
