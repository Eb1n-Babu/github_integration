// Custom JavaScript for interactivity - Works in dev/prod
document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus on username input
    const usernameInputs = document.querySelectorAll('input[name="username"]');
    if (usernameInputs.length > 0) {
        usernameInputs[0].focus();
    }

    // Make sample usernames clickable to fill form
    const samples = document.querySelectorAll('.list-unstyled li');
    samples.forEach(li => {
        li.style.cursor = 'pointer';
        li.addEventListener('click', () => {
            const input = document.querySelector('input[name="username"]');
            if (input) {
                input.value = li.textContent.trim();
            }
        });
    });

    // Form submission feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const btn = this.querySelector('button[type="submit"]');
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Fetching...';
            btn.disabled = true;
        });
    });
});