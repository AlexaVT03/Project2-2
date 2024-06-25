package org.gui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;

public class OutputScreen implements ActionListener {
    private JFrame frame;
    private JLabel title, temperaturePredicition, temperatureActual;
    private JButton backButton;

    public OutputScreen(String answerString, String date) {
        frame = new JFrame("Weather Predictor");
        frame.setSize(500, 200);
        frame.setLayout(null);

        title = new JLabel("Weather stats at "+date);
        title.setSize(300, 40);
        title.setLocation(280, 20);
        frame.add(title);

        //get actual from answerString
        int indexActual = answerString.indexOf("\"actual\":") + 9;
        int endIndexActual = answerString.indexOf(",", indexActual);
        String temperatureValueActual = answerString.substring(indexActual, endIndexActual).trim();

        //get prediction from answerString
        int indexPrediction = answerString.indexOf("\"prediction\":") + 13;
        int endIndexPrediction = answerString.indexOf("}", indexPrediction);
        String temperatureValuePrediction = answerString.substring(indexPrediction, endIndexPrediction).trim();


        temperaturePredicition = new JLabel("Temperature: ......");
        // Set the value for the temperature label
        temperaturePredicition.setText("Temperature prediction value: " + temperatureValuePrediction);
        temperaturePredicition.setSize(450, 30);
        temperaturePredicition.setLocation(20, 60);
        frame.add(temperaturePredicition);

        temperatureActual = new JLabel("Temperature: ......");
        // Set the value for the temperature label
        temperatureActual.setText("Temperature actual value: " + temperatureValueActual);
        temperatureActual.setSize(450, 30);
        temperatureActual.setLocation(20, 90);
        frame.add(temperatureActual);


        //back button 
        backButton = new JButton("Try again!");
        backButton.setSize(150, 30);
        backButton.setLocation(175, 130);
        backButton.addActionListener(this);
        
        frame.add(backButton);


        frame.setLocationRelativeTo(null);
        frame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        frame.setVisible(true);

    }
        @Override
        public void actionPerformed(ActionEvent e) {
            frame.dispose();
            InputScreen inputScreen = new InputScreen();
        }
    
}
