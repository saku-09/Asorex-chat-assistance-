from flask import Flask, request, jsonify, render_template, session
import os
import sys
import uuid

# Add the 'app' directory to sys.path to handle imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from chatbot import get_response

app = Flask(__name__)
app.secret_key = "asorex_secret_key_123" # Required for sessions

@app.route("/")
def home():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    # Clear conversation context on fresh load
    session['context'] = {}
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        if not user_msg:
            return jsonify({"response": "Please say something!"})
        
        # Get context from session
        context = session.get('context', {})
        
        # Get response and updated context
        response, updated_context = get_response(user_msg, context)
        
        # Save context back to session
        session['context'] = updated_context
        
        return jsonify({"response": response})
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"response": "I'm having a bit of trouble understanding that. Could you try again?"})

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
