// netlify/functions/calculate.js

class PokerPayoutCalculator {
    constructor() {
      this.players = [];
    }
  
    addPlayer(name, buyInAmount, finalAmount) {
      const player = new Player(name, buyInAmount);
      player.finalAmount = finalAmount;
      player.calculateBalance();
      this.players.push(player);
    }
  
    calculateTransactions() {
      const transactions = [];
      // Sort players by their balance
      this.players.sort((a, b) => a.balance - b.balance);
  
      let i = 0, j = this.players.length - 1;
      while (i < j) {
        const debtor = this.players[i];
        const creditor = this.players[j];
        const amount = Math.min(-debtor.balance, creditor.balance);
  
        transactions.push(new Transaction(debtor.name, creditor.name, amount));
  
        // Adjust balances
        debtor.balance += amount;
        creditor.balance -= amount;
  
        if (Math.abs(debtor.balance) < 0.01) i++;
        if (Math.abs(creditor.balance) < 0.01) j--;
      }
      return transactions;
    }
  
    totalBuyIn() {
      return this.players.reduce((acc, player) => acc + player.buyInAmount, 0);
    }
  
    totalBuyOut() {
      return this.players.reduce((acc, player) => acc + player.finalAmount, 0);
    }
  
    validateTotals() {
      if (Math.abs(this.totalBuyIn() - this.totalBuyOut()) > 0.001) {
        throw new Error("Total buy-in amount does not match total buy-out amount.");
      }
    }
  }
  
  class Player {
    constructor(name, buyInAmount) {
      this.name = name;
      this.buyInAmount = buyInAmount;
      this.finalAmount = 0;
      this.balance = 0;
    }
  
    calculateBalance() {
      this.balance = this.finalAmount - this.buyInAmount;
    }
  }
  
  class Transaction {
    constructor(payer, receiver, amount) {
      this.payer = payer;
      this.receiver = receiver;
      this.amount = amount;
    }
  
    toString() {
      return `${this.payer} owes ${this.receiver} $${this.amount.toFixed(2)}`;
    }
  }
  
  exports.handler = async (event) => {
    if (event.httpMethod !== "POST") {
      return {
        statusCode: 405,
        body: JSON.stringify({ error: "Method Not Allowed" }),
      };
    }
  
    try {
      const data = JSON.parse(event.body);
      const calculator = new PokerPayoutCalculator();
  
      data.players.forEach(player => {
        calculator.addPlayer(player.name, player.buyIn, player.buyOut);
      });
  
      calculator.validateTotals();
      const transactions = calculator.calculateTransactions().map(transaction => transaction.toString());
  
      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ success: true, transactions: transactions }),
      };
    } catch (error) {
      return {
        statusCode: 500,
        body: JSON.stringify({ success: false, error: error.message }),
      };
    }
  };
  