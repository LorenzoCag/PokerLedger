from flask import Flask, request, jsonify, render_template_string, render_template

from poker import PokerPayoutCalculator
from parsing import parse_csv, process_player_data
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Website2.html')

@app.route('/pokernow')
def pokernow():
    return render_template('pokernow.html')


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['csvfile']
    filename = secure_filename(file.filename)
    filepath = os.path.join('path_to_temp_directory', filename)  # Replace with your desired path
    file.save(filepath)

    players_data = parse_csv(filepath)
    transactions = process_player_data(players_data, PokerPayoutCalculator())
    
    
    # Remove the temporary CSV file after processing
    os.remove(filepath)

    return jsonify({
        'success': True if transactions else False,
        'transactions': [str(transaction) for transaction in transactions] if transactions else "Failed to process CSV."
    })
    

    # return render_template_string(html_content)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    calculator = PokerPayoutCalculator()
    for player in data['players']:
        name = player['name']
        buy_in = player['buyIn']
        final_amount = player['buyOut']
        calculator.add_player(name, buy_in, final_amount)

    try:
        transactions = calculator.calculate_transactions()
        calculator.validate_totals()
        transactions_output = [str(transaction) for transaction in transactions]
        return jsonify({'success': True, 'transactions': transactions_output})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)