/**
 * AJAX Form Handler for Hardter TV Website
 * Handles form submissions without page reloads
 */

// Generic function to handle form submissions via AJAX
function submitFormAjax(formElement, successCallback, errorCallback) {
    const form = formElement instanceof HTMLFormElement ? formElement : document.getElementById(formElement);
    if (!form) {
        console.error('Form not found');
        return;
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const formData = new FormData(form);
        const url = form.getAttribute('action');
        const method = form.getAttribute('method') || 'POST';
        
        fetch(url, {
            method: method,
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (successCallback) {
                successCallback(data);
            } else {
                // Default success behavior
                showNotification(data.message || 'Erfolgreich gespeichert!', 'success');
                if (data.redirect) {
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 3000);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (errorCallback) {
                errorCallback(error);
            } else {
                // Default error behavior
                showNotification('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.', 'error');
            }
        });
    });
}

// Function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}-message`;
    
    // Add appropriate icon
    let icon = '';
    if (type === 'success') {
        icon = '<i class="fas fa-check-circle"></i>';
    } else if (type === 'error') {
        icon = '<i class="fas fa-exclamation-circle"></i>';
    } else if (type === 'info') {
        icon = '<i class="fas fa-info-circle"></i>';
    }
    
    notification.innerHTML = `${icon}<p>${message}</p>`;
    
    // Add to the DOM
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Function to initialize all forms with AJAX submission
function initAjaxForms() {
    // Content item form
    const contentForm = document.querySelector('.cm-form[action*="/add_content"]');
    if (contentForm) {
        submitFormAjax(contentForm, function(data) {
            showNotification('Inhalt erfolgreich hinzugefügt!', 'success');
            // Reload the content section
            if (data.html) {
                document.querySelector('.locations-grid').innerHTML = data.html;
            } else {
                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            }
        });
    }
    
    // Image form
    const imgForm = document.querySelector('.cm-form[action*="/add_img"]');
    if (imgForm) {
        submitFormAjax(imgForm, function(data) {
            showNotification('Bild erfolgreich hinzugefügt!', 'success');
            if (data.html) {
                document.querySelector('.slider-container').innerHTML = data.html;
            } else {
                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            }
        });
    }
    
    // About text form
    const aboutForm = document.querySelector('.about-form');
    if (aboutForm) {
        submitFormAjax(aboutForm, function(data) {
            showNotification('Text erfolgreich hinzugefügt!', 'success');
            if (data.html) {
                document.querySelector('.about-text').innerHTML = data.html;
            } else {
                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            }
        });
    }
    
    // Termin form
    const terminForm = document.querySelector('.termin-form');
    if (terminForm) {
        submitFormAjax(terminForm, function(data) {
            showNotification('Termin erfolgreich hinzugefügt!', 'success');
            if (data.html) {
                document.querySelector('.clean-table tbody').innerHTML = data.html;
            } else {
                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            }
        });
    }
    
    // Contact form
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        submitFormAjax(contactForm, function(data) {
            showNotification('Nachricht erfolgreich gesendet!', 'success');
            contactForm.reset();
        });
    }
    
    // Newsletter form
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        submitFormAjax(newsletterForm, function(data) {
            showNotification('Erfolgreich zum Newsletter angemeldet!', 'success');
            newsletterForm.reset();
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initAjaxForms);

// Function to handle delete operations via AJAX
function setupDeleteButtons() {
    const deleteButtons = document.querySelectorAll('.cm-delete-btn, .delete, button[onclick*="confirm"]');
    
    deleteButtons.forEach(button => {
        // Remove existing onclick handler
        const originalOnClick = button.getAttribute('onclick');
        button.removeAttribute('onclick');
        
        button.addEventListener('click', function(event) {
            event.preventDefault();
            
            // If there was a confirmation dialog, keep it
            if (originalOnClick && originalOnClick.includes('confirm')) {
                if (!confirm('Möchten Sie diesen Eintrag wirklich löschen?')) {
                    return;
                }
            }
            
            const url = button.getAttribute('href') || button.closest('form').getAttribute('action');
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                showNotification(data.message || 'Erfolgreich gelöscht!', 'success');
                
                // Remove the element from the DOM
                const itemToRemove = button.closest('.location-card, .event-item, tr, .card');
                if (itemToRemove) {
                    itemToRemove.remove();
                } else {
                    // If we can't find a specific element to remove, reload the page
                    setTimeout(() => {
                        window.location.reload();
                    }, 3000);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.', 'error');
            });
        });
    });
}

// Setup delete buttons when DOM is loaded
document.addEventListener('DOMContentLoaded', setupDeleteButtons);

// CSS for notifications
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            background-color: #f8f9fa;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 9999;
            display: flex;
            align-items: center;
            transform: translateX(120%);
            transition: transform 0.3s ease;
            max-width: 300px;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification i {
            margin-right: 10px;
            font-size: 1.2em;
        }
        
        .notification.success-message {
            background-color: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }
        
        .notification.error-message {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }
        
        .notification.info-message {
            background-color: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #17a2b8;
        }
    `;
    document.head.appendChild(style);
});
