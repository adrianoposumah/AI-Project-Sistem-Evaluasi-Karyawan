from flask import Flask, render_template, request

app = Flask(__name__)

# List to store evaluation results
evaluations = []

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

    # Calculate total score
    value_A = (total_A * weight_A)
    value_B = (total_B * weight_B)
    value_C = (total_C * weight_C)

    total_score = value_A + value_B + value_C
    total_score *= 100

    # Determine evaluation result
    if total_score < 46:
        predikat = "Unsatisfactory"
    elif 46 <= total_score < 66.5:
        predikat = "Satisfactory"
        if total_score >= 66:
            predikat += " - Good"
    elif 66.5 <= total_score < 80:
        predikat = "Good"
        if total_score < 67:
            predikat = "Satisfactory - " + predikat
        if total_score >= 79.5:
            predikat += " - Very Good"
    elif 80 <= total_score < 93.5:
        predikat = "Very Good"
        if total_score < 81:
            predikat = "Good - " + predikat
        if total_score >= 93:
            predikat += " - Outstanding"
    else:
        predikat = "Outstanding"
        if total_score < 94:
            predikat = "Very Good - " + predikat

    # Format the results to 4 decimal places
    value_A = f"{value_A:.4f}"
    value_B = f"{value_B:.4f}"
    value_C = f"{value_C:.4f}"
    total_score = f"{total_score:.4f}"

    # Save the evaluation result
    evaluations.append({
        'nama': nama,
        'total_A': value_A,
        'total_B': value_B,
        'total_C': value_C,
        'predikat': predikat,
        'total_score': total_score
    })

    # Render the result in the template
    return render_template('index.html', evaluations=evaluations)

if __name__ == '__main__':
    app.run(debug=True)
