from flask import Flask, render_template, request
from fuzzy_logic import evaluate_performance

app = Flask(__name__)

# Daftar karyawan untuk menampilkan hasil evaluasi
employees = []

@app.route('/')
def index():
    return render_template('index.html', employees=employees)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    nama = request.form['nama']
    productivity = float(request.form['productivity'])
    quality = float(request.form['quality'])
    discipline = float(request.form['discipline'])
    initiative = float(request.form['initiative'])

    score = evaluate_performance(productivity, quality, discipline, initiative)
    formatted_score = f"{score:.4f}"

    # Menentukan predikat berdasarkan score
    if score >= 85:
        predikat = 'Sangat Baik'
    elif score >= 70:
        predikat = 'Baik'
    elif score >= 50:
        predikat = 'Cukup'
    else:
        predikat = 'Kurang'

    # Menambahkan hasil evaluasi ke daftar karyawan
    employees.append({
        'nama': nama,
        'productivity': productivity,
        'quality': quality,
        'discipline': discipline,
        'initiative': initiative,
        'predikat': predikat,
        'score': formatted_score
    })

    return render_template('index.html', employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
