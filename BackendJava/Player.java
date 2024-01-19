package BackendJava;
public class Player {
    final String name;
    final double buyInAmount;
    private double finalAmount;
    private double balance; // Balance is gain or loss


    public Player(String name, double buyInAmount) {
        this.name = name;
        this.buyInAmount = buyInAmount;
        this.finalAmount = 0; // Initially set to 0, will be updated later
        this.balance = 0; // Initially set to 0, will be calculated based on finalAmount
    }

    // Getters and Setters

    public String getName() {
        return name;
    }

    public double getBuyInAmount() {
        return buyInAmount;
    }


    public double getFinalAmount() {
        return finalAmount;
    }

    public void setFinalAmount(double finalAmount) {
        this.finalAmount = finalAmount;
    }

    public double getBalance() {
        return balance;
    }

    //calculates balance at the end
    public void calculateBalance() {
        this.balance = this.finalAmount - this.buyInAmount;
    }

    @Override
    public String toString() {
        return "Player{" +
                "name='" + name + '\'' +
                ", buyInAmount=" + buyInAmount +
                ", finalAmount=" + finalAmount +
                ", balance=" + balance +
                '}';
    }
}
