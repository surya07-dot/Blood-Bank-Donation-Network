document.addEventListener("DOMContentLoaded", () => {
    // Auto-hide alerts after a few seconds
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alert) => {
        setTimeout(() => {
            try {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
                bsAlert.close();
            } catch (e) {
                // ignore
            }
        }, 5000);
    });
});
