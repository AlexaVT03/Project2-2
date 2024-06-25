import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class GUI extends JFrame {
    private JComboBox<String> cityComboBox;
    private JComboBox<String> modelComboBox;
    private JComboBox<String> dateComboBox;
    private JLabel trueValueLabel;
    private JLabel forecastLabel;
    private JLabel dateLabel;
    private Predictor predictor;

    public GUI() {
        predictor = new Predictor();

        setTitle("Prediction GUI");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new FlowLayout());

        // make choice for city
        JLabel cityLabel = new JLabel("Select City:");
        cityComboBox = new JComboBox<>(Predictor.cityNames);
        add(cityLabel);
        add(cityComboBox);

        // make choice for the model (LSTM or ARIMA)
        JLabel modelLabel = new JLabel("Select Model:");
        modelComboBox = new JComboBox<>(new String[]{"SARIMA", "LSTM"}); // stats vs ai
        add(modelLabel);
        add(modelComboBox);

        // choice for the date
        JLabel dateLabel = new JLabel("Select Date:");
        String[] dateStrings = TrueValues.dateTimeStrings;
        dateComboBox = new JComboBox<>(dateStrings);
        add(dateLabel);
        add(dateComboBox);

        // button for prediction, appears underneath gui atm
        JButton predictButton = new JButton("Predict");
        predictButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                updatePrediction();
            }
        });
        add(predictButton);

        // actual (true) temperature
        JLabel trueValueTitleLabel = new JLabel("True Value:");
        trueValueLabel = new JLabel();
        add(trueValueTitleLabel);
        add(trueValueLabel);

        // forecast, predicted temp value
        JLabel forecastTitleLabel = new JLabel("Forecast:");
        forecastLabel = new JLabel();
        add(forecastTitleLabel);
        add(forecastLabel);

        setSize(800, 300); // Set initial size with larger height
        setLocationRelativeTo(null); // Center the window
    }

    // update forecast dynamically based on model, city, date
    private void updatePrediction() {
        int selectedTimePoint = dateComboBox.getSelectedIndex();
        int selectedCityIndex = cityComboBox.getSelectedIndex();
        String selectedModel = (String) modelComboBox.getSelectedItem();
        Double[] prediction = Predictor.getForecast(selectedTimePoint, selectedCityIndex, selectedModel);
        String date = Predictor.getDate(selectedTimePoint);

        // print results in gui
        trueValueLabel.setText("True Value: " + prediction[0]);
        forecastLabel.setText("Forecast: " + prediction[1]);
        dateLabel.setText("Date: " + date);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                GUI gui = new GUI();
                gui.setVisible(true);
            }
        });
    }
}

