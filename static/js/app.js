// JavaScript with animations and refresh checking
console.log('JavaScript file loaded');

// Animation Functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('hide');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

function animateRevenue(element) {
    element.classList.add('animate');
    setTimeout(() => element.classList.remove('animate'), 800);
}

function animateNewAppointment(element) {
    element.classList.add('new-appointment');
    setTimeout(() => element.classList.remove('new-appointment'), 1000);
}

function animateStatusChange(element) {
    element.classList.add('status-change');
    setTimeout(() => element.classList.remove('status-change'), 600);
}

function animateButton(button, originalText) {
    button.classList.add('loading');
    button.disabled = true;
    setTimeout(() => {
        button.classList.remove('loading');
        button.disabled = false;
        button.textContent = originalText;
    }, 1000);
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded');
    console.log('Current path:', window.location.pathname);
    
    // Animate elements on page load
    const appointmentItems = document.querySelectorAll('.appointment-item');
    appointmentItems.forEach((item, index) => {
        item.style.animationDelay = `${index * 0.1}s`;
        item.classList.add('fadeIn');
    });
    
    // Form loading states with animations
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Validate barber_id and appointment_time if they exist in this form
            const barberId = form.querySelector('#barber_id');
            const appointmentTime = form.querySelector('#appointment_time');

            if (barberId && !barberId.value) {
                e.preventDefault();
                alert('Please select a barber before booking.');
                return;
            }
            if (appointmentTime && (!appointmentTime.value || appointmentTime.disabled)) {
                e.preventDefault();
                alert('Please select an available time slot before booking.');
                return;
            }

            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.textContent;
                animateButton(submitBtn, originalText);
            }
        });
    });
    
    // Animate checkout buttons
    const checkoutBtns = document.querySelectorAll('.btn-checkout');
    checkoutBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const appointmentItem = this.closest('.appointment-item');
            if (appointmentItem) {
                animateStatusChange(appointmentItem);
                showNotification('Appointment completed! 💰', 'success');
                
                // Animate revenue update
                setTimeout(() => {
                    const revenueAmounts = document.querySelectorAll('.revenue-amount');
                    revenueAmounts.forEach(amount => animateRevenue(amount));
                }, 300);
            }
        });
    });
    
    // Animate cancel buttons
    const cancelBtns = document.querySelectorAll('.btn-cancel');
    cancelBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const appointmentItem = this.closest('.appointment-item');
            if (appointmentItem) {
                animateStatusChange(appointmentItem);
                showNotification('Appointment cancelled', 'error');
            }
        });
    });
    
    // Check for new bookings - handled by admin_dashboard.html inline script
    if (window.location.pathname.includes('/admin/dashboard')) {
        console.log('Dashboard detected');
    }
    
    // Success page animation
    if (window.location.pathname.includes('/success')) {
        const successIcon = document.querySelector('.success-icon');
        const successMessage = document.querySelector('.success-message');
        
        if (successIcon) {
            setTimeout(() => {
                successIcon.style.animation = 'checkmark 0.8s ease-in-out';
            }, 200);
        }
        
        showNotification('Appointment booked successfully! ✅', 'success');
    }
    
    // Form validation animations
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('invalid', function() {
            this.parentElement.classList.add('error');
            setTimeout(() => {
                this.parentElement.classList.remove('error');
            }, 500);
        });
        
        input.addEventListener('input', function() {
            if (this.validity.valid) {
                this.parentElement.classList.add('success');
                setTimeout(() => {
                    this.parentElement.classList.remove('success');
                }, 300);
            }
        });
    });
});