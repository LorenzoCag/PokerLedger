class PokerPayoutCalculator:
    class Player:
        def __init__(self, name, buy_in_amount):
            self.name = name
            self.buy_in_amount = buy_in_amount
            self.final_amount = 0
            self.balance = 0
        
        def calculate_balance(self):
            self.balance = self.final_amount - self.buy_in_amount
        
        def __str__(self):
            return f"Player(name={self.name}, buy_in_amount={self.buy_in_amount}, final_amount={self.final_amount}, balance={self.balance})"
    
    class Transaction:
        def __init__(self, payer, receiver, amount):
            self.payer = payer
            self.receiver = receiver
            self.amount = amount
        
        def __str__(self):
            return f"{self.payer} owes {self.receiver} ${self.amount:.2f}"
    
    def __init__(self):
        self.players = []
    
    def add_player(self, name, buy_in_amount, final_amount):
        player = self.Player(name, buy_in_amount)
        player.final_amount = final_amount
        player.calculate_balance()
        self.players.append(player)
    
    def calculate_transactions(self):
        transactions = []
        # Sort players by their balance
        self.players.sort(key=lambda player: player.balance)
        
        i, j = 0, len(self.players) - 1
        while i < j:
            debtor = self.players[i]
            creditor = self.players[j]
            amount = min(-debtor.balance, creditor.balance)

            # Create a transaction with the correct amount
            transactions.append(self.Transaction(debtor.name, creditor.name, amount))

            # Directly adjust balances
            debtor.balance += amount
            creditor.balance -= amount

        # Check if balances are settled to a sufficiently small value
            if abs(debtor.balance) < 0.01:
                i += 1
            if abs(creditor.balance) < 0.01:
                j -= 1
        return transactions
    
    def total_buy_in(self):
        return sum(player.buy_in_amount for player in self.players)
    
    def total_buy_out(self):
        return sum(player.final_amount for player in self.players)
    
    def validate_totals(self):
        if abs(self.total_buy_in() - self.total_buy_out()) > 0.001:
            raise ValueError("Total buy-in amount does not match total buy-out amount.")


import sys

calculator = PokerPayoutCalculator()

# Process command-line arguments to add players
for arg in sys.argv[1:]:
    parts = arg.split()
    if len(parts) != 3:
        print("Invalid argument format. Expected: Name BuyInAmount FinalAmount")
        continue
    name, buy_in_str, final_amount_str = parts
    try:
        buy_in_amount = float(buy_in_str)
        final_amount = float(final_amount_str)
        calculator.add_player(name, buy_in_amount, final_amount)
    except ValueError as e:
        print(f"Error converting numbers for {name}: {e}")
        continue

try:
    # First, validate the totals to ensure the total buy-in matches the total buy-out
    calculator.validate_totals()
    print("Totals validated successfully.")
    
    # Calculate and print transactions only if validation is successful
    transactions = calculator.calculate_transactions()
    print("\nTransactions:")
    for transaction in transactions:
        print(transaction)
except ValueError as e:
    # If validation fails, print the error message and skip printing transactions
    print(e)