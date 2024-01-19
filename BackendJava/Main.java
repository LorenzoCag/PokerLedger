package BackendJava;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        // Check if command-line arguments are provided
        if (args.length == 0) {
            System.out.println("No input provided. Please provide player details.");
            return;
        }

        // Concatenate command-line arguments into a single string
        // This is necessary if the input is provided as separate arguments
        StringBuilder inputBuilder = new StringBuilder();
        for (String arg : args) {
            inputBuilder.append(arg).append(" ");
        }

        // Initialize the PaymentCalculator
        PaymentCalculator calculator = new PaymentCalculator();

        try {
            // Parse the input to create Player objects and calculate their balances
            calculator.parseInput(inputBuilder.toString().trim());

            calculator.validateTotals(); //check if the total buy in and total buy out are the same

            // Calculate the transactions required to settle all balances
            List<Transactions> transactions = calculator.calculateTransactions();

            // Check if there are any transactions to display
            if (transactions.isEmpty()) {
                System.out.println("No transactions required.");
            } else {
                // Display each transaction
                for (Transactions transaction : transactions) {
                    System.out.println(transaction);
                }
            }
        } catch (Exception e) {
            // Catch any exceptions that may occur during parsing or calculation
            System.out.println("An error occurred: " + e.getMessage());
            e.printStackTrace();
        }
    
    }
}

