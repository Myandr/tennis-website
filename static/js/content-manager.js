/**
 * Content Manager for Hardter TV Website
 * Handles dynamic content updates without page reloads
 */

class ContentManager {
  constructor() {
    this.setupEventListeners()
    this.setupFormHandlers()
  }

  setupEventListeners() {
    // Listen for form submissions
    document.addEventListener("submit", (e) => {
      const form = e.target
      if (
        form.classList.contains("cm-form") ||
        form.classList.contains("about-form") ||
        form.classList.contains("termin-form")
      ) {
        e.preventDefault()
        this.handleFormSubmit(form)
      }
    })

    // Listen for delete button clicks
    document.addEventListener("click", (e) => {
      if (e.target.classList.contains("cm-delete-btn") || e.target.classList.contains("delete")) {
        e.preventDefault()
        this.handleDelete(e.target)
      }
    })
  }

  setupFormHandlers() {
    // Setup drag and drop for image uploads
    const dropAreas = document.querySelectorAll(".cm-drop-area")
    dropAreas.forEach((area) => this.setupDragAndDrop(area))
  }

  async handleFormSubmit(form) {
    try {
      const formData = new FormData(form)
      const response = await fetch(form.action, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) throw new Error("Network response was not ok")

      const data = await response.json()

      if (data.success) {
        this.showNotification(data.message, "success")

        // Handle different form types
        if (form.classList.contains("cm-form")) {
          if (form.getAttribute("action").includes("add_content")) {
            this.addNewContent(data)
          } else if (form.getAttribute("action").includes("add_img")) {
            this.addNewImage(data)
          }
        } else if (form.classList.contains("about-form")) {
          this.addNewAboutText(data)
        } else if (form.classList.contains("termin-form")) {
          this.addNewTermin(data)
        }

        // Reset form
        form.reset()
        if (form.querySelector(".cm-preview")) {
          form.querySelector(".cm-preview").innerHTML = ""
        }
      }
    } catch (error) {
      console.error("Error:", error)
      this.showNotification("Ein Fehler ist aufgetreten", "error")
    }
  }

  async handleDelete(button) {
    if (!confirm("Möchten Sie diesen Eintrag wirklich löschen?")) return

    try {
      const url = button.href || button.getAttribute("data-delete-url")
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) throw new Error("Network response was not ok")

      const data = await response.json()

      if (data.success) {
        this.showNotification(data.message, "success")

        // Remove element from DOM
        const item = button.closest(".location-card, .news-card, tr, .card")
        if (item) {
          item.style.opacity = "0"
          setTimeout(() => item.remove(), 300)
        }
      }
    } catch (error) {
      console.error("Error:", error)
      this.showNotification("Ein Fehler ist aufgetreten", "error")
    }
  }

  addNewContent(data) {
    const locationsGrid = document.querySelector(".locations-grid")
    const newCard = this.createLocationCard(data)

    // Add with animation
    newCard.style.opacity = "0"
    locationsGrid.insertBefore(newCard, locationsGrid.firstChild)
    requestAnimationFrame(() => (newCard.style.opacity = "1"))
  }

  addNewImage(data) {
    const sliderContainer = document.querySelector(".slider-container")
    const newCard = this.createImageCard(data)

    // Add with animation
    newCard.style.opacity = "0"
    sliderContainer.insertBefore(newCard, sliderContainer.firstChild)
    requestAnimationFrame(() => (newCard.style.opacity = "1"))
  }

  addNewAboutText(data) {
    const aboutText = document.querySelector(".about-text")
    const newText = this.createAboutText(data)

    // Add with animation
    newText.style.opacity = "0"
    aboutText.insertBefore(newText, aboutText.firstChild)
    requestAnimationFrame(() => (newText.style.opacity = "1"))
  }

  addNewTermin(data) {
    const tbody = document.querySelector(".clean-table tbody")
    const newRow = this.createTerminRow(data)

    // Add with animation
    newRow.style.opacity = "0"
    tbody.insertBefore(newRow, tbody.firstChild)
    requestAnimationFrame(() => (newRow.style.opacity = "1"))
  }

  createLocationCard(data) {
    const card = document.createElement("div")
    card.className = "location-card"
    card.setAttribute("data-aos", "flip-up")
    card.innerHTML = `
            <img src="data:image/jpeg;base64,${data.image}" alt="${data.heading}">
            <div class="arrow-icon"><i class="fa fa-arrow-right"></i></div>
            <div class="location-info">
                <h3>${data.heading}</h3>
                <div class="location-times">${data.text1}</div>
                <div class="location-address">${data.text2}</div>
            </div>
            <div class="expanded-info">${data.iframe}</div>
            ${
              this.isAdmin()
                ? `
                <a href="/delete_content/${data.id}" class="cm-delete-btn">Delete</a>
            `
                : ""
            }
        `
    return card
  }

  createImageCard(data) {
    const card = document.createElement("div")
    card.className = "card"
    card.setAttribute("onclick", "expandImg(this)")
    card.innerHTML = `
            <img src="data:image/jpeg;base64,${data.image}" alt="Gallery Image">
            ${
              this.isAdmin()
                ? `
                <a href="/delete_img/${data.id}" class="cm-delete-btn">Delete</a>
            `
                : ""
            }
        `
    return card
  }

  createAboutText(data) {
    const element = document.createElement(data.type === "headline" ? "h3" : "p")
    element.textContent = data.content
    if (this.isAdmin()) {
      const deleteForm = document.createElement("form")
      deleteForm.action = `/delete_about_text/${data.id}`
      deleteForm.method = "POST"
      deleteForm.style.display = "inline"
      deleteForm.innerHTML = `
                <button class="delete" type="submit">Löschen</button>
            `
      element.appendChild(deleteForm)
    }
    return element
  }

  createTerminRow(data) {
    const row = document.createElement("tr")
    row.setAttribute("data-aos", "fade-right")
    row.innerHTML = `
            <td>${data.datum}</td>
            <td><strong>${data.veranstaltung}</strong></td>
            <td>${data.uhrzeit}</td>
            <td>${data.ort}</td>
            ${
              this.isAdmin()
                ? `
                <td>
                    <form action="/delete_termin/${data.id}" method="POST" style="display: inline">
                        <button class="delete" type="submit">Löschen</button>
                    </form>
                </td>
            `
                : ""
            }
        `
    return row
  }

  setupDragAndDrop(dropArea) {
    const fileInput = dropArea.querySelector('input[type="file"]')
    const preview = dropArea.querySelector(".cm-preview")
    ;["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
      dropArea.addEventListener(eventName, preventDefaults, false)
    })

    function preventDefaults(e) {
      e.preventDefault()
      e.stopPropagation()
    }
    ;["dragenter", "dragover"].forEach((eventName) => {
      dropArea.addEventListener(eventName, () => {
        dropArea.classList.add("highlight")
      })
    })
    ;["dragleave", "drop"].forEach((eventName) => {
      dropArea.addEventListener(eventName, () => {
        dropArea.classList.remove("highlight")
      })
    })

    dropArea.addEventListener("drop", (e) => {
      const dt = e.dataTransfer
      const files = dt.files
      fileInput.files = files
      this.handleFiles(files, preview)
    })

    fileInput.addEventListener("change", () => {
      this.handleFiles(fileInput.files, preview)
    })
  }

  handleFiles(files, preview) {
    const file = files[0]
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader()
      reader.onloadend = () => {
        const img = document.createElement("img")
        img.src = reader.result
        preview.innerHTML = ""
        preview.appendChild(img)
      }
      reader.readAsDataURL(file)
    }
  }

  showNotification(message, type = "info") {
    const notification = document.createElement("div")
    notification.className = `notification ${type}-message`

    const icon = type === "success" ? "check-circle" : type === "error" ? "exclamation-circle" : "info-circle"

    notification.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <p>${message}</p>
        `

    document.body.appendChild(notification)

    requestAnimationFrame(() => {
      notification.classList.add("show")
      setTimeout(() => {
        notification.classList.remove("show")
        setTimeout(() => notification.remove(), 300)
      }, 3000)
    })
  }

  isAdmin() {
    return document.body.hasAttribute("data-is-admin")
  }
}

// Initialize the content manager when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  window.contentManager = new ContentManager()
})

