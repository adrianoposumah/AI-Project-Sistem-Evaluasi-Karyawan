from flask import Flask, render_template, request
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

# List to store evaluation results
evaluations = []

# Define fuzzy variables
def define_fuzzy_variables():
    management = ctrl.Antecedent(np.arange(0, 11, 1), 'management')
    job_specific = ctrl.Antecedent(np.arange(0, 11, 1), 'job_specific')
    personality = ctrl.Antecedent(np.arange(0, 11, 1), 'personality')
    score = ctrl.Consequent(np.arange(0, 101, 1), 'score')

    # Custom membership functions
    management['poor'] = fuzz.trimf(management.universe, [0, 0, 2.5])
    management['mediocre'] = fuzz.trimf(management.universe, [0, 2.5, 5])
    management['average'] = fuzz.trimf(management.universe, [2.5, 5, 7.5])
    management['decent'] = fuzz.trimf(management.universe, [5, 7.5, 10])
    management['excellent'] = fuzz.trimf(management.universe, [7.5, 10, 10])

    job_specific['poor'] = fuzz.trimf(job_specific.universe, [0, 0, 2.5])
    job_specific['mediocre'] = fuzz.trimf(job_specific.universe, [0, 2.5, 5])
    job_specific['average'] = fuzz.trimf(job_specific.universe, [2.5, 5, 7.5])
    job_specific['decent'] = fuzz.trimf(job_specific.universe, [5, 7.5, 10])
    job_specific['excellent'] = fuzz.trimf(job_specific.universe, [7.5, 10, 10])

    personality['poor'] = fuzz.trimf(personality.universe, [0, 0, 2.5])
    personality['mediocre'] = fuzz.trimf(personality.universe, [0, 2.5, 5])
    personality['average'] = fuzz.trimf(personality.universe, [2.5, 5, 7.5])
    personality['decent'] = fuzz.trimf(personality.universe, [5, 7.5, 10])
    personality['excellent'] = fuzz.trimf(personality.universe, [7.5, 10, 10])

    score['unsatisfactory'] = fuzz.trimf(score.universe, [0, 0, 46])
    score['satisfactory'] = fuzz.trimf(score.universe, [45, 46, 66.5])
    score['good'] = fuzz.trimf(score.universe, [59, 67, 80])
    score['very_good'] = fuzz.trimf(score.universe, [73, 81, 93.5])
    score['outstanding'] = fuzz.trimf(score.universe, [87, 100, 100])

    return management, job_specific, personality, score

# Define the fuzzy control system
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
    # Retrieve form data
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

    # Define the sub weights
    sub_weights_A = [0.21, 0.21, 0.29, 0.29]
    sub_weights_B = [0.09, 0.146, 0.146, 0.09, 0.09, 0.146, 0.146, 0.146]
    sub_weights_C = [0.31, 0.23, 0.23, 0.23]

    # Define the criteria weights
    weight_A = 0.23
    weight_B = 0.56
    weight_C = 0.21

    # Calculate degrees
    def calculate_degree(value, min_val, max_val):
        return (value - min_val) / (max_val - min_val)

    degrees_A = [calculate_degree(A1, 1, 4), calculate_degree(A2, 1, 3), calculate_degree(A3, 1, 4), calculate_degree(A4, 1, 4)]
    degrees_B = [calculate_degree(B1, 1, 3), calculate_degree(B2, 1, 5), calculate_degree(B3, 1, 5), calculate_degree(B4, 1, 3),
                 calculate_degree(B5, 1, 3), calculate_degree(B6, 1, 5), calculate_degree(B7, 1, 5), calculate_degree(B8, 1, 5)]
    degrees_C = [calculate_degree(C1, 1, 4), calculate_degree(C2, 1, 3), calculate_degree(C3, 1, 3), calculate_degree(C4, 1, 3)]

    # Calculate criteria totals
    total_A = sum(degree * weight for degree, weight in zip(degrees_A, sub_weights_A))
    total_B = sum(degree * weight for degree, weight in zip(degrees_B, sub_weights_B))
    total_C = sum(degree * weight for degree, weight in zip(degrees_C, sub_weights_C))

    # Normalize totals to a 0-10 scale for fuzzy logic
    total_A_normalized = total_A * 10
    total_B_normalized = total_B * 10
    total_C_normalized = total_C * 10

    weight_A = total_A_normalized * weight_A
    weight_B = total_B_normalized * weight_B
    weight_C = total_C_normalized * weight_C

    weight_A_normalized = weight_A * 10
    weight_B_normalized = weight_B * 10
    weight_C_normalized = weight_C * 10
    # Define fuzzy variables and control system
    management, job_specific, personality, score = define_fuzzy_variables()
    scoring = define_fuzzy_control_system(management, job_specific, personality, score)

    # Pass inputs to the ControlSystem using Antecedent labels
    scoring.input['management'] = total_A_normalized
    scoring.input['job_specific'] = total_B_normalized
    scoring.input['personality'] = total_C_normalized

    # Crunch the numbers
    scoring.compute()

    # Get the score and determine the predikat based on memberships
    total_score = scoring.output['score']

    # Get membership values for score
    score_membership = {
        'unsatisfactory': fuzz.interp_membership(score.universe, score['unsatisfactory'].mf, total_score),
        'satisfactory': fuzz.interp_membership(score.universe, score['satisfactory'].mf, total_score),
        'good': fuzz.interp_membership(score.universe, score['good'].mf, total_score),
        'very_good': fuzz.interp_membership(score.universe, score['very_good'].mf, total_score),
        'outstanding': fuzz.interp_membership(score.universe, score['outstanding'].mf, total_score)
    }

    # Determine the predikat
    predikat = []
    for label, membership_value in score_membership.items():
        if membership_value > 0:
            predikat.append(label.replace('_', ' ').title())
    
    predikat = ' - '.join(predikat)

    total_A = f"{weight_A_normalized:.4f}"
    total_B = f"{weight_B_normalized:.4f}"
    total_C = f"{weight_C_normalized:.4f}"
    total_score = f"{total_score:.4f}"

    # Save the evaluation result
    evaluations.append({
        'nama': nama,
        'total_A': total_A,
        'total_B': total_B,
        'total_C': total_C,
        'predikat': predikat,
        'total_score': total_score
    })

    # Render the result in the template
    return render_template('index.html', evaluations=evaluations)

if __name__ == '__main__':
    app.run(debug=True)
