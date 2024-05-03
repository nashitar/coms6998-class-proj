from flask import Flask, render_template, request, redirect, url_for
import random
from datetime import datetime

app = Flask(__name__)

users = {}  # Dictionary to store user information

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

    if email in users:
        return 'You\'ve already attempted this'

    delay = random.randint(0, 30)
    sticky_key = random.randint(0, 500)
    users[email] = {
        'delay': delay,
        'sticky_key': sticky_key,
        'start': timestamp
    }

    return render_template('flappy.html', delay=delay, sticky_key=sticky_key, email=email)

@app.route('/submit-best-score', methods=['POST'])
def submit_best_score():
    data = request.get_json()
    best_score = data.get('bestScore')
    email = data.get('email')
    timestamp = datetime.now().strftime("%-m/%-d/%Y, %-I:%M:%S %p")

    if email not in users:
        return 'User not found'

    users[email]['best_score'] = best_score
    users[email]['end'] = timestamp

    return render_template('form.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    performance = request.form['performance']
    frustration = request.form['frustration']
    comments = request.form['comments']
    email = request.form['email']

    if email not in users:
        return 'User not found'

    users[email]['performance'] = performance
    users[email]['frustration'] = frustration
    users[email]['comments'] = comments

    return render_template('thanks.html')

@app.route('/user-info')
def user_info():
    return render_template('user_info.html', users=users)

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=4000)