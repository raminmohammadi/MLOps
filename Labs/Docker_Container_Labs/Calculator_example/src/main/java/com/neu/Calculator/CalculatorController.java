package com.neu.Calculator;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/calculator")
public class CalculatorController {

    @GetMapping("/add")
    public String add(@RequestParam double num1, @RequestParam double num2) {
        double result = num1 + num2;
        return createJsonResponse(num1, num2, "addition", result);
    }

    @GetMapping("/subtract")
    public String subtract(@RequestParam double num1, @RequestParam double num2) {
        double result = num1 - num2;
        return createJsonResponse(num1, num2, "subtraction", result);
    }

    @GetMapping("/multiply")
    public String multiply(@RequestParam double num1, @RequestParam double num2) {
        double result = num1 * num2;
        return createJsonResponse(num1, num2, "multiplication", result);
    }

    @GetMapping("/divide")
    public String divide(@RequestParam double num1, @RequestParam double num2) {
        try {
            if (num2 == 0) {
                throw new IllegalArgumentException("Cannot divide by zero");
            }
            double result = num1 / num2;
            return createJsonResponse(num1, num2, "division", result);
        } catch (IllegalArgumentException e) {
            return createJsonErrorResponse("Cannot divide by zero");
        }
    }

    private String createJsonResponse(double num1, double num2, String operation, double result) {
        return String.format("{\"num1\": %.2f, \"num2\": %.2f, \"operation\": \"%s\", \"result\": %.2f}",
                num1, num2, operation, result);
    }

    private String createJsonErrorResponse(String error) {
        return String.format("{\"error\": \"%s\", \"result\": %.2f}", error, 0.00);
    }
}