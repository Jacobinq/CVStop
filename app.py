from flask import Flask, render_template, request, send_file
import requests
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')  

@app.route('/Create')
def create():
    return render_template('create.html') 
 
@app.route('/about')
def about():
    return render_template('about.html')  

@app.route('/contact')
def contact():
    return render_template('contact.html')  

def create_better_pdf(cv_text):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []


    for line in cv_text.split('\n'):
        if line.strip() == '':
            story.append(Spacer(1, 12)) 
        else:
            story.append(Paragraph(line.strip(), styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

@app.route('/generate_cv', methods=['POST'])
def generate_cv():
    cv_data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "CareerObjective": request.form['CareerObjective'],
        "skills": request.form['skills'],
        "Education": request.form['Education'],
        "WorkExperience": request.form['WorkExperience'],
        "ProblemSolving": request.form['ProblemSolving'],
        "TechnicalSkills": request.form['TechnicalSkills'],
        "Achievements": request.form['Achievements'],



    }
                   
    prompt = f"""
    You are a professional CV writer.

    Your task is to generate a high-quality, professional CV based on the candidate information provided below.

    Instructions:
    - Expand each section to sound professional and complete.
    - Write a 4–5 sentence Professional Summary describing the candidate’s strengths and passions.
    - Expand Skills into a bulleted list with examples of how they are applied.
    - Expand Work Experience into 3–5 bullet points per role, describing responsibilities, technologies used, and achievements.
    - Use professional business language throughout.
    - No Markdown formatting, no asterisks, plain text only.
    - Email should appear plainly (example@example.com), no links.
    - Remove all ** and any formatting
    - Remove +'s and Bullet points
    - Insert exactly ONE blank line between each section.
    - Each section must contain approximately THREE complete, well-structured sentences.
    - Ensure the writing style is professional, polished, and articulate.
    - Expand the content slightly to sound complete, confident, and impactful without adding irrelevant information.
    - Maintain a concise tone while ensuring sentences are rich, descriptive, and grammatically sophisticated.
    - Do not add Here is the professionally written CV for.
    - When putting Name and Email put Name: and Email: infront of them.
    
    The required section headings, in this exact order, are:

    Full Name: {cv_data['name']}
    Email: {cv_data['email']}
    Career Objectives: {cv_data['CareerObjective']}
    Achievements: {cv_data['Achievements']}
    Education: {cv_data['Education']}
    Work Experience: {cv_data['WorkExperience']}
    Problem Solving: {cv_data['ProblemSolving']}
    Skills: {cv_data['skills']}
    Technical Skills: {cv_data['TechnicalSkills']}

    Use these headings exactly as shown — no deviations.
    """

    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            "model": "llama3", 
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    generated_cv_text = result['response']

    pdf_buffer = create_better_pdf(generated_cv_text)

    FileName = f"{cv_data['name'].replace(' ', '_')}_CV.pdf"

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=FileName,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)