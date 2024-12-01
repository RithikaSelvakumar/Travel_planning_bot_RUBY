#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
from new import main  # Import your processing code from new.py
from langchain_core.messages import HumanMessage

app = Flask(__name__)

chat_history = []

@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML page

@app.route('/get_response', methods=['POST'])
def get_response():
    global chat_history
    user_input = request.json.get("message")  # Get the message from the front-end
    if not user_input:
        return jsonify({"error": "No input received"})

    # Call the `main` function from new.py to process the input
    rag_chain = main(user_input, chat_history)
    ai_msg_1 = rag_chain.invoke({"input": user_input, "chat_history": chat_history})

    bot_response = ai_msg_1['answer']
    chat_history.extend([HumanMessage(content=user_input), bot_response])

    return jsonify({"response": bot_response})  # Send the response back to front-end

if __name__ == '__main__':
    app.run(debug=True,port=5001)  # Run the Flask app
