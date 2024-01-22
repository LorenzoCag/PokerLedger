package BackendJava;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

public class PaymentCalculator {
    final List<Player> players;

    public PaymentCalculator() {
        players = new ArrayList<>();
    }

    public void addPlayer(Player player) {
        players.add(player);
    }

    public int getPlayersCount() {
        return players.size();
    }


    public void parseInput(String input) {
        String[] parts = input.split(" "); //splits input by spaces and puts them into an array
        for (int i = 0; i < parts.length; i += 3) {
            String name = parts[i];
            double buyInAmount = Double.parseDouble(parts[i + 1]);
            double finalAmount = Double.parseDouble(parts[i + 2]);

            Player player = new Player(name, buyInAmount);
            player.setFinalAmount(finalAmount);
            player.calculateBalance();
            players.add(player);
        }
    }


    //Players sorted by balance. Negative means they owe money, 
    //positive means they are owed. A loop then iterates over the list,
    //and the amount is th eminimum amount between the absolute value of
    //the creditor and the debtor. This is then added to the list of transactions.
    //at the end, if the debtor's balance is 0, you move on to the next transaction,
    //while if the creditor balance is 0, you move on to the next creditor.
    public List<Transactions> calculateTransactions() {     
        // Sort players by balance
        players.sort(Comparator.comparingDouble(Player::getBalance));

        List<Transactions> transactions = new ArrayList<>();
        int i = 0, j = players.size() - 1;

        while (i < j) {
            Player debtor = players.get(i);
            Player creditor = players.get(j);

            double amount = Math.min(-debtor.getBalance(), creditor.getBalance());
            transactions.add(new Transactions(debtor.getName(), creditor.getName(), amount));

            debtor.setFinalAmount(debtor.getFinalAmount() + amount);
            creditor.setFinalAmount(creditor.getFinalAmount() - amount);
            debtor.calculateBalance();
            creditor.calculateBalance();

            if (-debtor.getBalance() < 0.01) i++;
            if (creditor.getBalance() < 0.01) j--;
        }

        return transactions;
    }

    public double totalBuyIn() {
        double total = 0;
        for (Player player : players) {
            total += player.getBuyInAmount();
        }
        return total;
    }

    public double totalBuyOut() {
        double total = 0;
        for (Player player : players) {
            total += player.getFinalAmount();
        }
        return total;
    }

    public void validateTotals() {
        double totalBuyIn = totalBuyIn();
        double totalBuyOut = totalBuyOut();

        if (Math.abs(totalBuyIn - totalBuyOut) > 0.001) { // Using a small threshold to account for rounding errors
            throw new IllegalArgumentException("Error: Total buy-in amount (" + totalBuyIn +
                    ") does not match total buy-out amount (" + totalBuyOut + ").");
        }
    }
}

