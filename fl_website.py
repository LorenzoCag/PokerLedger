from flask import Flask, request, jsonify, render_template_string, render_template

from poker import PokerPayoutCalculator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('Website2.html')

@app.route('/pokernow')
def pokernow():
    return render_template('pokernow.html')
    

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