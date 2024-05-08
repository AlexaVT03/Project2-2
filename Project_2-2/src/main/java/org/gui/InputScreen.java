package org.gui;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import org.main.API_requester;
import java.util.HashMap;

public class InputScreen implements ActionListener {
    private JFrame frame;
    private JLabel label1, label2;
    private JTextField day, month, year;
    private JButton computeButton;
    public InputScreen() {
        frame = new JFrame("Weather Predictor");
        frame.setSize(450, 250);
        frame.setLayout(null);

        label1 = new JLabel("Please input the date for which you would like to predict the weather:");
        label1.setSize(400, 30);
        label1.setLocation(20, 20);
        frame.add(label1);

        label2 = new JLabel("Please use the following format: dd/mm/yyyy, e.g. 01/01/2001");
        label2.setSize(400, 30);
        label2.setLocation(20, 40);
        frame.add(label2);

        day = new JTextField();
        day.setSize(50, 30);
        day.setLocation(110, 100);
        frame.add(day);

        month = new JTextField();
        month.setSize(50, 30);
        month.setLocation(170, 100);
        frame.add(month);

        year = new JTextField();
        year.setSize(100, 30);
        year.setLocation(230, 100);
        frame.add(year);

        computeButton = new JButton("Predict!");
        computeButton.setSize(100, 30);
        computeButton.setLocation(170, 150);
        computeButton.addActionListener(this);
        frame.add(computeButton);

        frame.setLocationRelativeTo(null);
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        // Get the parameters for the API request
        // Get the date
        int day = Integer.parseInt(this.day.getText());
        int month = Integer.parseInt(this.month.getText());
        int year = Integer.parseInt(this.year.getText());
        String date = year + "-" + month + "-" + day;
        // Get the location
        int latitude = 20;
        int longitude = 20;
        // Put those in the HashMap
        HashMap<String, String> params = new HashMap<>();
        params.put("date", date);
        params.put("latitude", String.valueOf(latitude));
        params.put("longitude", String.valueOf(longitude));
        // Make the request to the API
        String answer = API_requester.sendRequestToAPI("predict_temp", "GET", params);
        frame.dispose();
        // Pass the answer (in JSON) to the output screen
        OutputScreen outputScreen = new OutputScreen(answer);
    }
}
