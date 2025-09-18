// Auto-Close Alert After 15 Seconds (for dev-alert)
document.addEventListener('DOMContentLoaded', function() {
    const alertElement = document.getElementById('dev-alert');
    if (alertElement) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alertElement);
            bsAlert.close();
        }, 15000); // 15 seconds
    }
});