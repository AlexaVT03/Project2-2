package org.gui;

import javax.swing.*;

public class OutputScreen {
    private JFrame frame;
    private JLabel title, temperature;

    public OutputScreen(String answerString) {
        frame = new JFrame("Weather Predictor");
        frame.setSize(550, 550);
        frame.setLayout(null);

        title = new JLabel("Weather stats at [user input]");
        title.setSize(300, 40);
        title.setLocation(280, 20);
        frame.add(title);
        // Get the temperature value from the JSON answer, this needs to be done better as now it just looks for : and }
        String temperatureValue = answerString.substring(answerString.indexOf(":") + 1, answerString.indexOf("}")).trim();
        temperature = new JLabel("Temperature: ......");
        // Set the value for the temperature label
        temperature.setText("Temperature: " + temperatureValue);
        temperature.setSize(150, 30);
        temperature.setLocation(20, 60);
        frame.add(temperature);

        frame.setLocationRelativeTo(null);
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
