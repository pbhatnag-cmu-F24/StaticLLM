// File: AdminUser.java
public class AdminUser {
    private String name;
    private String role;

    public void createUser() {
        System.out.println("Creating user in DB...");
        // simulate DB logic
    }

    public void printUserInfo() {
        System.out.println("Name: " + name + ", Role: " + role);
    }

    public void sendNotification() {
        System.out.println("Sending notification...");
    }
}
