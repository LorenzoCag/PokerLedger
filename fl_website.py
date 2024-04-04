from flask import Flask, request, jsonify, render_template_string

from poker import PokerPayoutCalculator

app = Flask(__name__)

@app.route('/')
def index():
    html_content = '''
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <title>Poker Payout Manager</title>
    <style>
        /* Additional styles for button alignment */
        .form-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .button-group {
            display: flex;
            gap: 10px;
        }
        #tournament-form {
            margin-top: 20px;
            display: flex;
            flex-direction: column;
        }
        .player-group {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 20px;
        }
        
    </style>
</head>
<body>
    <nav class="container-fluid">
        <ul>
            <li><strong>Poker Cash Game Payout Calculator</strong></li>
        </ul>
        <ul>
            <li><a href="#">Home</a></li>
            
        </ul>
    </nav>
    <main class="container">
        <div class="grid">
            <section>
                <hgroup>
                    <h2>Payout Calculator</h2>
                    <h3>Manage your players and payouts</h3>
                </hgroup>
                <!-- Form Header for Buttons -->
                <div class="form-header">
                    <div></div> <!-- Placeholder for left alignment -->
                    <div class="button-group">
                        <button type="button" onclick="addPlayer()">Add Another Player</button>
                        <button type="button" onclick="resetForm()">Reset</button>
                        <button type="button" id="calculate-payouts" onclick="calculatePayouts()">Calculate Payouts</button>


                    </div>
                </div>
                <!-- Form Begins Here -->
                <form id="tournament-form">
                    <!-- Existing Player Groups Will Go Here -->
                </form>
                <h3>Payouts</h3>
                <div id="payouts" class="payouts-box">
                    <!-- Payouts will be displayed here -->
                </div>
            </section>
        </div>
    </main>
    <footer class="container">
        <small>
            <a href="#">Privacy Policy</a> • <a href="#">Terms of Service</a>
        </small>
    </footer>

    <script>
        let playerCount = 1;

        function addPlayer() {
            const form = document.getElementById('tournament-form');
            const playerGroup = document.createElement('div');
            playerGroup.className = 'player-group';

            const fields = ['name', 'buy-in', 'buy-out'];
            fields.forEach(field => {
                const div = document.createElement('div');
                const label = document.createElement('label');
                label.htmlFor = `player${playerCount}-${field}`;
                label.textContent = `Player ${playerCount} ${field.charAt(0).toUpperCase() + field.slice(1).replace('-', ' ')}`;
                const input = document.createElement('input');
                input.type = field === 'name' ? 'text' : 'number';
                input.id = `player${playerCount}-${field}`;
                input.name = `player${playerCount}-${field}`;
                input.placeholder = field === 'name' ? `Enter player ${playerCount} name` : '$';
                input.required = true;
                div.appendChild(label);
                div.appendChild(input);
                playerGroup.appendChild(div);
            });

            form.appendChild(playerGroup);
            playerCount++;
        }
        function resetForm() {
    const form = document.getElementById('tournament-form');
    form.innerHTML = ''; // Clear all child elements (player input groups)
    playerCount = 1; // Reset player count to initial value

    // Optionally clear the payouts section if you're displaying results there
    const payoutsElement = document.getElementById('payouts');
    if (payoutsElement) {
        payoutsElement.innerHTML = '';
    }
}

        function calculatePayouts() {
    event.preventDefault(); // Prevent the default form action
    const players = [];
    for (let i = 1; i < playerCount; i++) {
        players.push({
            name: document.getElementById(`player${i}-name`).value,
            buyIn: parseFloat(document.getElementById(`player${i}-buy-in`).value),
            buyOut: parseFloat(document.getElementById(`player${i}-buy-out`).value)
        });
    }

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ players: players })
    })
    .then(response => response.json())
    .then(data => {
        const payoutsElement = document.getElementById('payouts');
        payoutsElement.innerHTML = ''; // Clear previous results
        if (data.success) {
            data.transactions.forEach(transaction => {
                const p = document.createElement('p');
                p.textContent = transaction;
                payoutsElement.appendChild(p);
            });
        } else {
            // If there was an error, display it
            payoutsElement.textContent = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        const payoutsElement = document.getElementById('payouts');
        payoutsElement.textContent = 'Error: Unable to calculate payouts.';
    });
}
    </script>
</body>
</html>

    '''
    return render_template_string(html_content)

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