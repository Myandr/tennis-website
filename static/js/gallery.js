document.addEventListener("DOMContentLoaded", () => {
    // Function to handle image loading errors for gallery images
    function handleGalleryImageErrors() {
      const galleryImages = document.querySelectorAll(".gallery-item img, .gallery-card img");
      
      galleryImages.forEach((img) => {
        // Skip images that already have an onerror handler
        if (img.hasAttribute("onerror")) return;
        
        // Add error handler to load a default image if the original fails
        img.onerror = function() {
          this.src = "/static/images/placeholder.jpg";
          // Remove the onerror handler to prevent infinite loops
          this.onerror = null;
        };
      });
    }
    
    // Call the function when the page loads
    handleGalleryImageErrors();
    
    // Also call it after any AJAX content is loaded
    // This is a simplified example - adjust based on your actual AJAX implementation
    document.addEventListener("gallery-loaded", handleGalleryImageErrors);
  });
  
  
  // Add this to your gallery management JavaScript file
  function editGalleryImage(imageId) {
    const form = document.getElementById(`edit-image-form-${imageId}`);
    const formData = new FormData(form);
    
    // Show loading indicator
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;
    submitButton.disabled = true;
    submitButton.innerHTML = 'Wird bearbeitet...';
    
    fetch(`/api/gallery/${imageId}`, {
        method: 'PUT',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Fehler beim Aktualisieren des Bildes');
            });
        }
        return response.json();
    })
    .then(data => {
        // Success handling
        showNotification('Erfolg', 'Bild wurde erfolgreich aktualisiert', 'success');
        
        // Update the UI if needed
        const imageElement = document.querySelector(`.gallery-image-${imageId} img`);
        if (imageElement && data.image && data.image.image_path) {
            // Add timestamp to prevent caching
            imageElement.src = `${data.image.image_path}?t=${new Date().getTime()}`;
        }
        
        // Close modal or reset form
        closeModal(`edit-image-modal-${imageId}`);
    })
    .catch(error => {
        // Error handling
        console.error('Error updating image:', error);
        showNotification('Fehler', error.message, 'error');
    })
    .finally(() => {
        // Reset button state
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
    });
  }
  
  // Helper function to show notifications
  function showNotification(title, message, type) {
    // You can implement this based on your UI framework
    // For example, using a simple alert:
    alert(`${title}: ${message}`);
  }
  
  // Helper function to close modals
  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        // Implement based on your modal implementation
        // For example, using Bootstrap:
        // $(modal).modal('hide');
    }
  }