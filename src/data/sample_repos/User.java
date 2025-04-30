// File: User.java
public class User {
    private String username;
    private String password;

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public boolean authenticate(String inputPassword) {
        return password.equals(inputPassword);
    }
}
