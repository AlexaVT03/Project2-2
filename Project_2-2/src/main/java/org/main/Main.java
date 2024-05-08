package org.main;

import org.gui.GUI;
import org.gui.InputScreen;
import org.main.API_requester;

public class Main {
    public static void main(String[] args) {
        API_requester.startAPI();
        InputScreen inputScreen = new InputScreen();
        System.out.println("Hello world!");
    }
}