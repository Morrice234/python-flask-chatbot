from flask import Flask, render_template, request, jsonify
from actions import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    
    while True:
        user_message: str = request.form['user_message']
        
        #user_input: str = input("You: ")
        
        if user_message.lower() == 'quit':
            break
        best_match: str | None = find_best_match(user_message, [q["question"] for q in knowledge_base["questions"]])
        
        if not best_match:
            bot_response = 'I don\'t know the answer, can you teach me?'
            if bot_response == "I don\'t know the answer, can you teach me?":
                return jsonify({'bot': bot_response})
            
            new_answer: str = request.form['user_message']
            
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_message, "answer": new_answer})
                save_knowlwdge_base('knowledge_base.json', knowledge_base)
                bot_response = 'Thank you! I learned a new response!'
            
                return jsonify({'bot': bot_response})
        else:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            return jsonify({'bot': answer})
            
           

if __name__ == '__main__':
    app.run(debug=True)
