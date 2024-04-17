package org.main;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class APITest {
    public static void main(String[] args) {
        ProcessBuilder processBuilder = new ProcessBuilder("python", "Project_2-2/Python/connection_test.py");
        try {
            Process process = processBuilder.start();
            // Wait briefly for the server to start up
            try {
                Thread.sleep(2500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            // Execute API requests after the Python script has started
            System.out.println("First response:\n" + sendRequestToAPI("greet", "GET"));
            System.out.println("Second response:\n" + sendRequestToAPI("shutdown", "POST"));

        } catch (IOException e) {
            e.printStackTrace();
        }
    }



    public static String sendRequestToAPI(String adress, String requestType) {
        String finalResponse = "";
        try {
            
            // Set up the request
            HttpClient client = HttpClient.newHttpClient();
            String URL = "http://localhost:5100/" + adress;
            HttpRequest.Builder requestBuilder = HttpRequest.newBuilder().uri(URI.create(URL));

            // Check the request type
            if (requestType.equalsIgnoreCase("POST")) {
                requestBuilder = requestBuilder.POST(HttpRequest.BodyPublishers.noBody());
            } else if (requestType.equalsIgnoreCase("GET")) {
                requestBuilder = requestBuilder.GET();
            } else {
                return "Invalid request type";
            }

            // Send HTTP request to the Flask API
            HttpRequest request = requestBuilder.build();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println("Response status code: " + response.statusCode());
            finalResponse = response.body();
            
        } catch (IOException | InterruptedException e) {
            if(adress.equalsIgnoreCase("shutdown") && requestType.equalsIgnoreCase("POST") ){ // Added to handle the server shuttign down, as it doesn't return a response
                return "Server is shut down";
            }else{
                e.printStackTrace();
            }
        }
        return finalResponse;
    }
}
