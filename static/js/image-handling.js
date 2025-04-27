// Add this to your JavaScript file or include it in a script tag

document.addEventListener("DOMContentLoaded", () => {
  // Function to handle image loading errors
  function handleImageErrors() {
    const images = document.querySelectorAll("img")

    images.forEach((img) => {
      // Skip images that already have an onerror handler
      if (img.hasAttribute("onerror")) return

      // Add error handler to load a default image if the original fails
      img.onerror = function () {
        // Extract the section from the image's parent elements
        let section = "default"
        const parent = this.closest(".news-card, .location-card, .gallery-item, .about-image")

        if (parent) {
          if (parent.classList.contains("news-card")) section = "news"
          else if (parent.classList.contains("location-card")) section = "location"
          else if (parent.classList.contains("gallery-item")) section = "gallery"
          else if (parent.classList.contains("about-image")) section = "about"
        }

        // Set default image based on section
        switch (section) {
          case "news":
            this.src = "/static/images/tennis.jpg"
            break
          case "location":
            this.src = "/static/images/image.png"
            break
          case "gallery":
            this.src = "/static/images/placeholder.jpg"
            break
          case "about":
            this.src = "/static/images/Tennisball an Linie groß.jpg"
            break
          default:
            this.src = "/static/images/placeholder.svg"
        }

        // Remove the onerror handler to prevent infinite loops
        this.onerror = null
      }
    })
  }

  // Call the function when the page loads
  handleImageErrors()

  // Also call it after any AJAX content is loaded
  // This is a simplified example - adjust based on your actual AJAX implementation
  const originalFetch = window.fetch
  window.fetch = function () {
    return originalFetch.apply(this, arguments).then((response) => {
      setTimeout(handleImageErrors, 500) // Add delay to ensure DOM is updated
      return response
    })
  }
})



