package BackendJava;
public class Transactions {
    final String payer;    // The name of the player who owes money
    final String receiver; // The name of the player who is owed money
    final double amount;   // The amount of money to be paid


    public Transactions(String payer, String receiver, double amount) {
        this.payer = payer;
        this.receiver = receiver;
        this.amount = amount;
    }




    public String toString() {
        return payer + " owes " + receiver + " $" + String.format("%.2f", amount);
    }
}

