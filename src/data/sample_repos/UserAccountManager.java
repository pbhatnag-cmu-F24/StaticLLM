import java.util.*;
import java.util.regex.*;
import java.io.FileWriter;
import java.io.IOException;

public class UserAccountManager {
    private Map<String, User> users = new HashMap<>();
    private List<String> logs = new ArrayList<>();
    private String logFile = "user_audit.log";

    public boolean createUser(String username, String email, String password) {
        if (!isValidEmail(email) || !isStrongPassword(password)) {
            log("Failed to create user: Invalid email or weak password.");
            return false;
        }
        User user = new User(username, email, password);
        users.put(username, user);
        log("User created: " + username);
        sendEmail(email, "Welcome to our system!");
        audit("CREATE", username);
        return true;
    }

    public boolean deleteUser(String username) {
        if (!users.containsKey(username)) {
            log("Attempted to delete non-existent user: " + username);
            return false;
        }
        users.remove(username);
        log("User deleted: " + username);
        audit("DELETE", username);
        return true;
    }

    public boolean resetPassword(String username, String newPassword) {
        if (!users.containsKey(username) || !isStrongPassword(newPassword)) {
            log("Failed to reset password for: " + username);
            return false;
        }
        User user = users.get(username);
        user.setPassword(newPassword);
        log("Password reset for user: " + username);
        sendEmail(user.getEmail(), "Your password has been updated.");
        audit("PASSWORD_RESET", username);
        return true;
    }

    private boolean isStrongPassword(String password) {
        return password.length() >= 8 &&
               Pattern.compile("[A-Z]").matcher(password).find() &&
               Pattern.compile("[a-z]").matcher(password).find() &&
               Pattern.compile("[0-9]").matcher(password).find();
    }

    private boolean isValidEmail(String email) {
        return email.contains("@") && email.contains(".");
    }

    private void sendEmail(String to, String message) {
        System.out.println("Sending email to " + to + ": " + message);
        // imagine SMTP integration here
    }

    private void log(String message) {
        logs.add(message);
        System.out.println("[LOG] " + message);
    }

    private void audit(String action, String username) {
        try (FileWriter writer = new FileWriter(logFile, true)) {
            writer.write(new Date() + " | " + action + " | " + username + "\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Inner User class
    class User {
        private String username;
        private String email;
        private String password;

        public User(String username, String email, String password) {
            this.username = username;
            this.email = email;
            this.password = password;
        }

        public String getEmail() {
            return email;
        }

        public void setPassword(String newPassword) {
            this.password = newPassword;
        }
    }
}
