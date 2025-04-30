public class ReportManager {
    private DatabaseConnection db;

    public ReportManager(DatabaseConnection db) {
        this.db = db;
    }

    public List<Report> generateMonthlyReports() {
        // Fetch data from DB
        List<User> users = db.getUsers();
        // Business logic
        List<Report> reports = new ArrayList<>();
        for (User user : users) {
            reports.add(new Report(user.getId(), calculateMetrics(user)));
        }
        return reports;
    }

    public void saveReportsToDisk(List<Report> reports, String filename) {
        try (FileWriter writer = new FileWriter(filename)) {
            for (Report report : reports) {
                writer.write(report.toCSV());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void emailReports(List<Report> reports, String email) {
        // SMTP integration here
        System.out.println("Sending email to: " + email);
    }

    private Map<String, Double> calculateMetrics(User user) {
        // Complex logic
        return new HashMap<>();
    }
}

