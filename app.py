from flask import Flask, render_template, request
from fuzzy_logic import evaluate_performance

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    productivity = float(request.form['productivity'])
    quality = float(request.form['quality'])
    discipline = float(request.form['discipline'])
    initiative = float(request.form['initiative'])

    score = evaluate_performance(productivity, quality, discipline, initiative)
    return render_template('results.html', score=score)

if __name__ == '__main__':
    app.run(debug=True)
