package org.gui;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import org.main.API_requester;
import java.util.HashMap;

public class InputScreen implements ActionListener {
    private JFrame frame;
    private JLabel label1, label2, label3;
    private JTextField day, month, year;
    private JButton computeButton;
    public InputScreen() {
        frame = new JFrame("Weather Predictor");
        frame.setSize(500, 250);
        frame.setLayout(null);

        label1 = new JLabel("Please input the date for which you would like to predict the weather:");
        label1.setSize(500, 30);
        label1.setLocation(20, 20);
        frame.add(label1);

        label2 = new JLabel("Please use the following format: dd/mm/yyyy, e.g. 01/01/2001");
        label2.setSize(500, 30);
        label2.setLocation(20, 40);
        frame.add(label2);

        day = new JTextField();
        day.setSize(50, 30);
        day.setLocation(125, 70);
        frame.add(day);

        month = new JTextField();
        month.setSize(50, 30);
        month.setLocation(200, 70);
        frame.add(month);

        year = new JTextField();
        year.setSize(75, 30);
        year.setLocation(275, 70);
        frame.add(year);

        label3 = new JLabel("Please pick a model to predict:");
        label3.setSize(500, 30);
        label3.setLocation(20, 100);
        frame.add(label3);


        //Options
        String[] models = {"Linear Regression"};
        //Drop down menu
        JComboBox<String> dropDownMenu = new JComboBox<>(models);

        dropDownMenu.addActionListener(new ActionListener() {

            @Override
            public void actionPerformed(ActionEvent e) {
                 // Get string dropdown 
                String selectedModel = (String) dropDownMenu.getSelectedItem();
                label3.setText("Selected model: "+selectedModel);
            }
            
        });
        dropDownMenu.setSize(150, 30);
        dropDownMenu.setLocation(175, 130);
        frame.add(dropDownMenu);

        computeButton = new JButton("Predict!");
        computeButton.setSize(150, 30);
        computeButton.setLocation(175, 180);
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
        String day = this.day.getText();
        String month = this.month.getText();
        String year = this.year.getText();
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
        OutputScreen outputScreen = new OutputScreen(answer, date);
    }
}
