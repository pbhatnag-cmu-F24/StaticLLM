package com.example.util;

public class TemperatureConverter {
    /**
     * Converts a Celsius value to Fahrenheit **and** returns
     * it as a human-readable string.
     */
    public String convertToFahrenheit(double celsius) {
        double f = celsius * 9.0 / 5.0 + 32.0;
        // subtle second concern: presentation/formatting
        return String.format("%.1f°F", f);
    }
}
