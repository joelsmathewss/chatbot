from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__, template_folder='templates')

# Read FAQ data from CSV
try:
    faqs = pd.read_csv('faq.csv').to_dict('records')
except FileNotFoundError:
    faqs = []
    print("Error: faq.csv not found. Please ensure the file is in the same directory.")

# Helper function for keyword-based matching
def match_question(user_question, faq_question):
    user_words = set(user_question.lower().split())
    faq_words = set(faq_question.lower().split())
    # Count matching words
    common_words = user_words.intersection(faq_words)
    # Require at least 50% word overlap or key terms like "order", "delivery", etc.
    return len(common_words) / max(len(faq_words), 1) > 0.5 or any(keyword in user_question.lower() for keyword in ['order', 'delivery', 'payment', 'track', 'refund'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    question = request.json.get('question', '').strip()
    if not question:
        return jsonify({'answer': "Please enter a question."}), 400

    print(f"Received question: {question}")  # Debug log

    for faq in faqs:
        if not isinstance(faq, dict) or 'Question' not in faq or 'Answer' not in faq:
            print(f"Invalid FAQ entry: {faq}")  # Debug log
            continue
        if match_question(question, faq['Question']):
            print(f"Matched FAQ: {faq['Question']}")  # Debug log
            return jsonify({'answer': faq['Answer']})

    print("No FAQ match found.")  # Debug log
    return jsonify({
        'answer': "I'm sorry, I don't have an answer for that. Please use the <a href='#contact'>Contact Us</a> form for further assistance."
    })

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    message = request.form.get('message', '').strip()

    # Basic validation
    if not name or not email or not message:
        return jsonify({'success': False, 'message': 'Please fill out all fields.'}), 400
    if '@' not in email or '.' not in email:
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400

    # In a real application, save to database or send email
    return jsonify({'success': True, 'message': 'Thank you, our team will contact you shortly.'})

if __name__ == '__main__':
    app.run(debug=True)