from flask import Flask, request, render_template
import PyPDF2
import os

app = Flask(__name__)

# PDF Text Extraction
def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)  # Updated to PdfReader for PyPDF2 v3.0+

    # Handle encrypted PDFs (if needed)
    if reader.is_encrypted:
        reader.decrypt('')

    for page in reader.pages:
        text += page.extract_text() or ""  # Improved error handling for empty pages
    return text

# Flashcard Generation (Simple Split Logic)
def generate_flashcards(text):
    sentences = text.split('.')
    flashcards = [sentence.strip() for sentence in sentences if sentence.strip()]
    return flashcards

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("pdf")  # Safer 'get()' method
        if uploaded_file:
            text = extract_text_from_pdf(uploaded_file)
            flashcards = generate_flashcards(text)
            return render_template("index.html", flashcards=flashcards)
    return render_template("index.html", flashcards=[])

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)  # Ensure 'output' folder exists
    app.run(debug=True)
