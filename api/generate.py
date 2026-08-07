import os
import requests
import PyPDF2
from flask import Flask, request, jsonify

# No more HTML templates! Python just handles the data now.
app = Flask(__name__)

@app.route('/api/generate', methods=['POST'])
def generate_notes():
    text_content = ""
    
    # 1. Handle PDF
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            try:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n"
            except Exception as e:
                return jsonify({"error": "Failed to read PDF."}), 400
    
    # 2. Handle Text
    if not text_content and 'text' in request.form:
        text_content = request.form['text']
        
    if not text_content.strip():
        return jsonify({"error": "Please paste text or upload a PDF."}), 400

    # 3. Direct API Call to Gemini
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
             return jsonify({"error": "Server error: API Key missing."}), 500
             
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        
        prompt = f"""
        You are an expert teacher. Read the given study material. Generate:
        1. Short Summary
        2. Important Points
        3. Important Definitions
        4. 15 Viva Questions
        5. 10 MCQs
        6. Flashcards
        7. Keywords
        8. One-day Revision Plan
        
        Format the response using HTML tags (<h2>, <ul>, <li>, <p>, <strong>). Do NOT include ```html markdown blocks.
        
        Study Material:
        {text_content}
        """
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code != 200:
            return jsonify({"error": f"API Error: {response_data}"}), 500
            
        generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"result": generated_text})
    
    except Exception as e:
        return jsonify({"error": f"Crash: {str(e)}"}), 500

# Required for Vercel
if __name__ == '__main__':
    app.run(debug=True)
