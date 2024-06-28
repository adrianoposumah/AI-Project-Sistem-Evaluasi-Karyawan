from flask import Flask, render_template, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

evaluations = []

def define_fuzzy_variables():
    management = ctrl.Antecedent(np.arange(0, 101, 1), 'management')
    job_specific = ctrl.Antecedent(np.arange(0, 101, 1), 'job_specific')
    personality = ctrl.Antecedent(np.arange(0, 101, 1), 'personality')
    score = ctrl.Consequent(np.arange(0, 101, 1), 'score')

    management['poor'] = fuzz.trimf(management.universe, [0, 0, 25])
    management['mediocre'] = fuzz.trimf(management.universe, [0, 25, 50])
    management['average'] = fuzz.trimf(management.universe, [25, 50, 75])
    management['decent'] = fuzz.trimf(management.universe, [50, 75, 100])
    management['excellent'] = fuzz.trimf(management.universe, [75, 100, 100])

    job_specific['poor'] = fuzz.trimf(job_specific.universe, [0, 0, 25])
    job_specific['mediocre'] = fuzz.trimf(job_specific.universe, [0, 25, 50])
    job_specific['average'] = fuzz.trimf(job_specific.universe, [25, 50, 75])
    job_specific['decent'] = fuzz.trimf(job_specific.universe, [50, 75, 100])
    job_specific['excellent'] = fuzz.trimf(job_specific.universe, [75, 100, 100])

    personality['poor'] = fuzz.trimf(personality.universe, [0, 0, 25])
    personality['mediocre'] = fuzz.trimf(personality.universe, [0, 25, 50])
    personality['average'] = fuzz.trimf(personality.universe, [25, 50, 75])
    personality['decent'] = fuzz.trimf(personality.universe, [50, 75, 100])
    personality['excellent'] = fuzz.trimf(personality.universe, [75, 100, 100])


    score['unsatisfactory'] = fuzz.trimf(score.universe, [0, 0, 46])
    score['satisfactory'] = fuzz.trimf(score.universe, [22.5, 46, 66.5])
    score['good'] = fuzz.trimf(score.universe, [59, 67, 80])
    score['very_good'] = fuzz.trimf(score.universe, [73, 81, 93.5])
    score['outstanding'] = fuzz.trimf(score.universe, [87, 100, 100])

    return management, job_specific, personality, score

def define_fuzzy_control_system(management, job_specific, personality, score):
    rule1 = ctrl.Rule(management['poor'] | job_specific['poor'] | personality['poor'], score['unsatisfactory'])
    rule2 = ctrl.Rule(management['mediocre'] | job_specific['mediocre'] | personality['mediocre'], score['satisfactory'])
    rule3 = ctrl.Rule(management['average'] | job_specific['average'] | personality['average'], score['good'])
    rule4 = ctrl.Rule(management['decent'] | job_specific['decent'] | personality['decent'], score['very_good'])
    rule5 = ctrl.Rule(management['excellent'] | job_specific['excellent'] | personality['excellent'], score['outstanding'])

    scoring_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
    scoring = ctrl.ControlSystemSimulation(scoring_ctrl)
    
    return scoring

@app.route('/')
def index():
    return render_template('index.html', evaluations=evaluations)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    nama = request.form['nama']
    A1 = int(request.form['A1'])
    A2 = int(request.form['A2'])
    A3 = int(request.form['A3'])
    A4 = int(request.form['A4'])
    B1 = int(request.form['B1'])
    B2 = int(request.form['B2'])
    B3 = int(request.form['B3'])
    B4 = int(request.form['B4'])
    B5 = int(request.form['B5'])
    B6 = int(request.form['B6'])
    B7 = int(request.form['B7'])
    B8 = int(request.form['B8'])
    C1 = int(request.form['C1'])
    C2 = int(request.form['C2'])
    C3 = int(request.form['C3'])
    C4 = int(request.form['C4'])

    sub_weights_A = [0.21, 0.21, 0.29, 0.29]
    sub_weights_B = [0.09, 0.146, 0.146, 0.09, 0.09, 0.146, 0.146, 0.146]
    sub_weights_C = [0.31, 0.23, 0.23, 0.23]

    def calculate_degree(value, min_val, max_val):
            return (value - min_val) / (max_val - min_val)

    degrees_A = [round(calculate_degree(A1, 1, 3), 2), round(calculate_degree(A2, 1, 3), 2),
                    round(calculate_degree(A3, 1, 4), 2), round(calculate_degree(A4, 1, 4), 2)]
    degrees_B = [round(calculate_degree(B1, 1, 3), 2), round(calculate_degree(B2, 1, 5), 2),
                    round(calculate_degree(B3, 1, 5), 2), round(calculate_degree(B4, 1, 3), 2),
                    round(calculate_degree(B5, 1, 3), 2), round(calculate_degree(B6, 1, 5), 2),
                    round(calculate_degree(B7, 1, 5), 2), round(calculate_degree(B8, 1, 5), 2)]
    degrees_C = [round(calculate_degree(C1, 1, 4), 2), round(calculate_degree(C2, 1, 3), 2),
                    round(calculate_degree(C3, 1, 3), 2), round(calculate_degree(C4, 1, 3), 2)]


    total_A = sum(degree * weight for degree, weight in zip(degrees_A, sub_weights_A))
    total_B = sum(degree * weight for degree, weight in zip(degrees_B, sub_weights_B))
    total_C = sum(degree * weight for degree, weight in zip(degrees_C, sub_weights_C))

    weight_A = 0.23
    weight_B = 0.56
    weight_C = 0.21

    total_A_normalized = round(total_A * 100, 2)
    total_B_normalized = round(total_B * 100, 2)
    total_C_normalized = round(total_C * 100, 2)

    weight_A = total_A_normalized * weight_A
    weight_B = total_B_normalized * weight_B
    weight_C = total_C_normalized * weight_C

    weight_A = round(weight_A, 2)
    weight_B = round(weight_B, 2)
    weight_C = round(weight_C, 2)

    total_score = round((weight_A + weight_B + weight_C),2)

    management, job_specific, personality, score = define_fuzzy_variables()
    scoring = define_fuzzy_control_system(management, job_specific, personality, score)

    scoring.input['management'] = total_A_normalized
    scoring.input['job_specific'] = total_B_normalized
    scoring.input['personality'] = total_C_normalized

    scoring.compute()

    final_score = scoring.output['score']

    score_membership = {
        'unsatisfactory': fuzz.interp_membership(score.universe, score['unsatisfactory'].mf, total_score),
        'satisfactory': fuzz.interp_membership(score.universe, score['satisfactory'].mf, total_score),
        'good': fuzz.interp_membership(score.universe, score['good'].mf, total_score),
        'very_good': fuzz.interp_membership(score.universe, score['very_good'].mf, total_score),
        'outstanding': fuzz.interp_membership(score.universe, score['outstanding'].mf, total_score)
    }

    predikat = []
    for label, membership_value in score_membership.items():
        if membership_value > 0:
            predikat.append(label.replace('_', ' ').title())
    
    predikat = ' - '.join(predikat)

    total_A = f"{total_A_normalized:.4f}"
    total_B = f"{total_B_normalized:.4f}"
    total_C = f"{total_C_normalized:.4f}"
    final_score = f"{final_score:.4f}"

    evaluations.append({
        'nama': nama,
        'total_A': total_A,
        'total_B': total_B,
        'total_C': total_C,
        'predikat': predikat,
        'total_score': final_score
    })

    return render_template('index.html', evaluations=evaluations)

if __name__ == '__main__':
    app.run(debug=True)
