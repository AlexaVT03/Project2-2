package org.main;

import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.Map;

/**
 * The API_requester class is responsible for sending requests to an API endpoint and handling the responses.
 */
public class API_requester {
    public static void main(String[] args) {
        ProcessBuilder processBuilder = new ProcessBuilder("python", "Project_2-2/Python/API_client.py");
        try {
            processBuilder.start();
            // Wait briefly for the server to start up
            try {
                Thread.sleep(2500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            // Send a request to the /predict endpoint with parameters
            Map<String, String> params = Map.of(
                "latitude", "34.05",
                "longitude", "-118.25",
                "date", "2023-05-05"
            );
            System.out.println("Sending prediction request...");
            String predictionResponse = sendRequestToAPI("predict_temp", "GET", params);
            System.out.println("Prediction response:\n" + predictionResponse);

            System.out.println("Sending shutdown request...");
            String shutdownResponse = sendRequestToAPI("shutdown", "POST", null);
            System.out.println("Shutdown response:\n" + shutdownResponse);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Sends a request to an API endpoint.
     *
     * @param address     the address of the API endpoint
     * @param requestType the type of the request (POST or GET)
     * @param queryParams the query parameters to include in the request
     * @return the response from the API endpoint
     */
    public static String sendRequestToAPI(String address, String requestType, Map<String, String> queryParams) {
    String finalResponse = "";
    try {
        // Build the URI with query parameters if present
        String baseURL = "http://localhost:5100/" + address;
        String encodedParams = queryParams != null ? queryParams.entrySet().stream()
            .map(entry -> URLEncoder.encode(entry.getKey(), StandardCharsets.UTF_8) + "=" + URLEncoder.encode(entry.getValue(), StandardCharsets.UTF_8))
            .reduce((p1, p2) -> p1 + "&" + p2)
            .map(params -> "?" + params)
            .orElse("")
            : "";

        URI uri = URI.create(baseURL + encodedParams);
        HttpRequest.Builder requestBuilder = HttpRequest.newBuilder().uri(uri);

        // Check the request type
        if (requestType.equalsIgnoreCase("POST")) {
            requestBuilder.POST(HttpRequest.BodyPublishers.noBody());
        } else if (requestType.equalsIgnoreCase("GET")) {
            requestBuilder.GET();
        } else {
            return "Invalid request type";
        }

        // Send HTTP request to the Flask API
        HttpRequest request = requestBuilder.build();
        HttpResponse<String> response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Response status code: " + response.statusCode());
        finalResponse = response.body();

    } catch (IOException | InterruptedException e) {
        if(address.equalsIgnoreCase("shutdown") && requestType.equalsIgnoreCase("POST")){ // Handling server shutdown
            return "Server is shut down";
        } else {
            e.printStackTrace();
        }
    }
    return finalResponse;
    }

    /**
     * Starts the API by executing a Python script.
     * This method creates a process builder to run the Python script and waits briefly for the server to start up.
     */
    public static void startAPI() {
        ProcessBuilder processBuilder = new ProcessBuilder("python", "Project_2-2/Python/API_client.py");
        try {
            processBuilder.start();
            // Wait briefly for the server to start up
            try {
                Thread.sleep(2500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
