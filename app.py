from flask import Flask, render_template, request, redirect, url_for
import random
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    email = request.args.get('email')

    return render_template('form.html', email=email)

@app.route('/flappy', methods=['POST'])
def flappy():
    email = request.form.get('email')
    timestamp = datetime.now().strftime("%-m/%-d/%Y, %-I:%M:%S %p")
    if not email:
        return 'Email is required'

    with open('subjects.txt', 'r') as file:
        emails = [line.split()[0] for line in file.readlines()]

    if email in emails:
        return 'You\'ve already attempted this'

    with open('subjects.txt', 'a') as file:
        delay = random.randint(0, 30)
        sticky_key = random.randint(0, 500)
        file.write(email + ' | ' + str(delay) + ' | ' + str(sticky_key) + ' | ' + timestamp + '\n')
    
    return render_template('flappy.html', delay=delay, sticky_key=sticky_key, email=email)

@app.route('/submit-best-score', methods=['POST'])
def submit_best_score():
    data = request.get_json()
    best_score = data.get('bestScore')
    email = data.get('email')
    timestamp = data.get('timestamp')

    print(email)

    with open('subjects.txt', 'r') as file:
        lines = file.readlines()

    with open('subjects.txt', 'w') as file:
        for line in lines:
            if line.startswith(email):
                line = line.strip() + ' | ' + timestamp +  ' | ' + str(best_score) + '\n'
            file.write(line)

    return render_template('form.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    performance = request.form['performance']
    frustration = request.form['frustration']
    comments = request.form['comments']
    email = request.form['email']

    with open('subjects.txt', 'r') as file:
        lines = file.readlines()

    with open('subjects.txt', 'w') as file:
        for line in lines:
            if line.startswith(email):
                line = line.strip() + ' | ' + performance +  ' | ' + frustration + ' | ' + comments + '\n'
            file.write(line)

    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)