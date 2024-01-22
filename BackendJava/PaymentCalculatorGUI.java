package BackendJava;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.util.List;

public class PaymentCalculatorGUI extends JFrame {
    private final JTextField[] playerNames = new JTextField[12];
    private final JTextField[] buyIns = new JTextField[12];
    private final JTextField[] buyOuts = new JTextField[12];
    private final JTextArea resultArea;

    public PaymentCalculatorGUI() {
        super("Payment Calculator");

        setLayout(new BorderLayout());

        JPanel inputPanel = new JPanel(new GridLayout(13, 3));
        inputPanel.add(new JLabel("Player Name"));
        inputPanel.add(new JLabel("Buy-in"));
        inputPanel.add(new JLabel("Buy-out"));

        for (int i = 0; i < 12; i++) {
            playerNames[i] = new JTextField(10);
            buyIns[i] = new JTextField(5);
            buyOuts[i] = new JTextField(5);
            inputPanel.add(playerNames[i]);
            inputPanel.add(buyIns[i]);
            inputPanel.add(buyOuts[i]);
        }

        JButton calculateButton = new JButton("Calculate");
        calculateButton.addActionListener(this::runCalculation);

        resultArea = new JTextArea(10, 30);
        resultArea.setEditable(false);

        add(inputPanel, BorderLayout.NORTH);
        add(calculateButton, BorderLayout.CENTER);
        add(new JScrollPane(resultArea), BorderLayout.SOUTH);

        pack();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    private void runCalculation(ActionEvent e) {
        try {
            PaymentCalculator calculator = new PaymentCalculator();
            for (int i = 0; i < 12; i++) {
                String name = playerNames[i].getText();
                if (name == null || name.trim().isEmpty()) {
                    continue; // Skip this player if the name field is empty
                }
                double buyIn = Double.parseDouble(buyIns[i].getText());
                double buyOut = Double.parseDouble(buyOuts[i].getText());
    
                Player player = new Player(name, buyIn);
                player.setFinalAmount(buyOut);
                player.calculateBalance();
                calculator.addPlayer(player);
            }
            if (calculator.getPlayersCount() < 2) {
                resultArea.setText("Error: At least 2 players are required.");
                return;
            }
    
            calculator.validateTotals();
            List<Transactions> transactions = calculator.calculateTransactions();
            StringBuilder resultText = new StringBuilder();
            for (Transactions t : transactions) {
                resultText.append(t.toString()).append("\n");
            }
            resultArea.setText(resultText.toString());
        } catch (Exception ex) {
            resultArea.setText("Error: " + ex.getMessage());
        }
    }
    

    public static void main(String[] args) {
        SwingUtilities.invokeLater(PaymentCalculatorGUI::new);
    }
}

