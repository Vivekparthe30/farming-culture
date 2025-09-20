# app.py
import os
from flask import Flask, app, render_template, request
from markupsafe import Markup
import google.generativeai as genai
from dotenv import load_dotenv
import markdown2

load_dotenv()

app = Flask(__name__)


# Create the model
generation_config = {
    "temperature": 1,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/predict.html', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        previous_crop = request.form['previous_crop']
        land_size = request.form['land_size']
        land_location = request.form['land_location']
        water_type = request.form['water_type']
        soil_type = request.form['Select Soil Type']

        # Prepare the input for the Gemini model
        prompt = f"""Based on the following farming details, provide a detailed analysis and recommendations in a well-formatted markdown structure:
        - Crop: {previous_crop}
        - Land Size: {land_size} acres
        - Location: {land_location}
        - Water Type: {water_type}
        - Soil Type: {soil_type}
        
        Please include:
        give a 4 sentence summery that wheather above suggestion in 'yes' or 'no', if these plants can grow in this soil type and also how many plants can grow according to the size of the land
        """
        
        # Start chat session and send message
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)
        
        # Convert markdown to HTML and mark it as safe for rendering
        html_content = markdown2.markdown(response.text)
        safe_html = Markup(html_content)

        return render_template('predict.html', response=safe_html)

    return render_template('predict.html', response=None)

if __name__ == '__main__':
    app.run(debug=True)