import csv
from poker import PokerPayoutCalculator
from werkzeug.utils import secure_filename
from flask import request, jsonify


import os








def parse_csv(filepath):
    players_data = []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['PLAYER'].strip()
            buy_in = float(row['BUY-IN'])
            stack = float(row['STACK'])
            net = float(row['NET'])

            # If 'BUY-OUT' is empty or zero, use 'STACK' + 'NET' value if it's greater than the buy-in, else just the buy-in
            buy_out = float(row['BUY-OUT']) if row['BUY-OUT'] else (buy_in + net) if (buy_in + net) > buy_in else buy_in

            player_info = {
                'name': name,
                'buy_in': buy_in,
                'buy_out': buy_out
            }
            players_data.append(player_info)

    return players_data

def process_player_data(players_data, calculator):
    for player in players_data:
        calculator.add_player(player['name'], player['buy_in'], player['buy_out'])

    # Perform the payout calculations as per the calculator's functionality
    try:
        calculator.validate_totals()
        return calculator.calculate_transactions()
    except ValueError as e:
        return str(e)

# Assuming 'filepath' is the path to your CSV file
calculator = PokerPayoutCalculator()  # Define the "calculator" variable

filepath = 'path_to_your_csv_file.csv'  # Replace with the path to your CSV file
players_data = parse_csv(filepath)  # Pass the "filepath" variable as an argument

transactions = process_player_data(players_data, calculator)
for transaction in transactions:
    print(transaction)


