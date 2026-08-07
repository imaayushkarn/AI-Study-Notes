from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import PyPDF2
import os

app = Flask(__name__, template_folder='templates')

# Vercel will inject this environment variable securely
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

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
        # 3. Use Gemini AI to generate notes
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # The exact prompt recommended for best results
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
        
        response = model.generate_content(prompt)
        return jsonify({"result": response.text})
    
    except Exception as e:
        return jsonify({"error": "AI Generation Failed. Make sure your API key is correct."}), 500

if __name__ == '__main__':
    app.run(debug=True)