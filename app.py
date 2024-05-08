import textwrap
from flask import Flask, render_template, request, jsonify
import markdown

import google.generativeai as genai

app = Flask(__name__)

def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/get", methods = ["GET", "POST"])
def chat():
    if request.method == 'POST':
        try:
            msg = request.form["msg"]
            input_text = msg
            genai.configure(api_key='AIzaSyAlU2UVOfoqC1-tWEcO-IFfNo8v03FW66c')

            # Set up the model
            generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
            }

            safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            ]

            system_instruction = "You are Adam, the friendly UTS mascot at the University of Technology Sarawak, who assists applicants throughout the admission process. You can't use any emoji to reply. You can only help applicants with matters related to admission. Anything other than admission inquiries is beyond your scope of assistance. You mustn't prompt different style of word such as italic, bold and underlined with long meaasge. You only can introduced yourself one time. Now, here is the overview of the programs offered by various schools:\n\nSchool of Foundation Studies:\nOffers two foundation programs:\nFoundation in Arts\nFoundation in Science\n\nUndergraduate Programs:\nSchool of Engineering and Technology:\nBachelor’s degrees in:\nFood Technology (Hons)\nCivil Engineering (Hons)\nElectrical Engineering (Hons)\nMechanical Engineering (Hons)\nScience in Occupational Safety and Health (Hons)\n\nSchool of Business and Management:\nBachelor’s degrees in:\nAccountancy (Hons)\nBusiness (Hons) Marketing\nBusiness Administration (Hons)\nTechnology Management (Hons)\n\nSchool of Computing & Creative Media:\nBachelor’s degrees in:\nComputer Science (Hons)\nIndustrial Design (Hons)\nCreative Digital Media (Hons)\nMobile Game Development (Hons)\n\nSchool of Built Environment:\nBachelor’s degrees in:\nQuantity Surveying (Hons)\nScience (Hons) in Architecture\nInterior Design (Hons)\nScience (Honours) in Property and Construction Management\n\nPostgraduate Studies (School of Postgraduate Studies):\nOffers master’s programs in:\nComputing\nArchitecture\nEngineering\nProject Management\nBusiness Administration\nApplied Sciences\nBusiness Management\n\nAlso provides PhD programs in:\nComputing\nEngineering\nApplied Science\nBusiness Management\n\n"
            model = genai.GenerativeModel("gemini-1.5-pro-latest",
                                        generation_config=generation_config,
                                        system_instruction=system_instruction,
                                        safety_settings=safety_settings)
            
            response = model.generate_content(input_text)

            bot_response = response.text if hasattr(response, 'text') else str(response)

            bot_response_markdown = to_markdown(bot_response)  # Convert to Markdown

            # Convert Markdown to HTML
            botHtml = markdown.markdown(bot_response_markdown, extensions=['fenced_code'])

            return jsonify({"sender": "Bot", "message": bot_response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
