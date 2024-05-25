package com.neu.Calculator;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.test.web.server.LocalServerPort;

import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class CalculatorControllerTests {

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

    @Test
    public void testAdditionEndpoint() {
        String url = "http://localhost:" + port + "/api/calculator/add?num1=2&num2=3";
        String response = restTemplate.getForObject(url, String.class);
        assertEquals("{\"num1\": 2.00, \"num2\": 3.00, \"operation\": \"addition\", \"result\": 5.00}", response);
    }

    @Test
    public void testSubtractionEndpoint() {
        String url = "http://localhost:" + port + "/api/calculator/subtract?num1=5&num2=3";
        String response = restTemplate.getForObject(url, String.class);
        assertEquals("{\"num1\": 5.00, \"num2\": 3.00, \"operation\": \"subtraction\", \"result\": 2.00}", response);
    }

    @Test
    public void testMultiplicationEndpoint() {
        String url = "http://localhost:" + port + "/api/calculator/multiply?num1=4&num2=3";
        String response = restTemplate.getForObject(url, String.class);
        assertEquals("{\"num1\": 4.00, \"num2\": 3.00, \"operation\": \"multiplication\", \"result\": 12.00}", response);
    }

    @Test
    public void testDivisionEndpoint() {
        String url = "http://localhost:" + port + "/api/calculator/divide?num1=5&num2=2";
        String response = restTemplate.getForObject(url, String.class);
        assertEquals("{\"num1\": 5.00, \"num2\": 2.00, \"operation\": \"division\", \"result\": 2.50}", response);
    }

    @Test
    public void testDivisionByZero() {
        String url = "http://localhost:" + port + "/api/calculator/divide?num1=5&num2=0";
        String response = restTemplate.getForObject(url, String.class);
        assertEquals("{\"error\": \"Cannot divide by zero\", \"result\": 0.00}", response);
    }
}
