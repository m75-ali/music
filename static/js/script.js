document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function() {
            const button = document.querySelector('button[type="submit"]');
            button.disabled = true;
            button.textContent = 'Submitting...';
        });
    }
});
