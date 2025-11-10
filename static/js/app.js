// Simple JavaScript for enhanced UX
document.addEventListener('DOMContentLoaded', function() {
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.textContent = 'Loading...';
                submitBtn.disabled = true;
            }
        });
    });
    
    // Auto-refresh dashboard every 30 seconds
    if (window.location.pathname === '/admin/dashboard') {
        setInterval(() => {
            window.location.reload();
        }, 30000);
    }
});