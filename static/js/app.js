// Simple JavaScript for enhanced UX
document.addEventListener('DOMContentLoaded', function() {
    // Show last refresh time
    if (window.location.pathname === '/admin/dashboard') {
        const now = new Date().toLocaleTimeString();
        console.log('Dashboard loaded at:', now);
    }
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
    
    // Real-time updates for dashboard using Server-Sent Events
    if (window.location.pathname === '/admin/dashboard') {
        const eventSource = new EventSource('/api/appointment-updates');
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.update) {
                window.location.reload();
            }
        };
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            eventSource.close();
        });
    }
});