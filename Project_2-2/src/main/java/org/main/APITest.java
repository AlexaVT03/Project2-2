package org.main;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.io.IOException;

public class APITest {
    public static void main(String[] args) {
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder().uri(URI.create("http://localhost:5100/greet")).build();
        try {
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println("Response status code: " + response.statusCode());
            System.out.println("Response body: " + response.body());
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}
