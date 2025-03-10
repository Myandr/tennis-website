document.addEventListener("DOMContentLoaded", () => {
  // Only run if admin controls exist
  if (!document.querySelector(".admin-controls")) return

  const toggleEditModeButton = document.getElementById("toggle-edit-mode")
  const editOverlay = document.getElementById("edit-overlay")
  const editForm = document.getElementById("about-edit-form")
  const cancelEditButton = document.getElementById("cancel-edit")
  const editField = document.getElementById("edit-field")
  const editContent = document.getElementById("edit-content")
  const editImage = document.getElementById("edit-image")
  const imageUploadGroup = document.getElementById("image-upload-group")
  const loadingSpinner = document.getElementById("loading-spinner")

  let aboutData = {}
  let isEditMode = false

  // Fetch about data
  fetchAboutData()

  function fetchAboutData() {
    loadingSpinner.style.display = "block"

    fetch("/api/about")
      .then((response) => response.json())
      .then((data) => {
        aboutData = data
        updateUI(data)
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error fetching about data:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Laden der Daten. Bitte versuchen Sie es später erneut.")
      })
  }

  function updateUI(data) {
    document.getElementById("about-title").textContent = data.title
    document.getElementById("about-welcome-text").textContent = data.welcome_text
    document.getElementById("about-club-title").textContent = data.club_title
    document.getElementById("about-club-text").textContent = data.club_text
    document.getElementById("about-goals-title").textContent = data.goals_title
    document.getElementById("about-goals-text").textContent = data.goals_text
    document.getElementById("about-membership-title").textContent = data.membership_title
    document.getElementById("about-membership-text").textContent = data.membership_text
    document.getElementById("about-image").src = data.image_path
  }

  // Toggle edit mode
  toggleEditModeButton.addEventListener("click", () => {
    isEditMode = !isEditMode
    document.body.classList.toggle("edit-mode", isEditMode)
    toggleEditModeButton.textContent = isEditMode ? "Beenden" : "Bearbeiten"

    if (isEditMode) {
      // Add click event listeners to editable elements
      document.querySelectorAll(".editable, .about-image").forEach((element) => {
        element.addEventListener("click", openEditForm)
      })
    } else {
      // Remove click event listeners
      document.querySelectorAll(".editable, .about-image").forEach((element) => {
        element.removeEventListener("click", openEditForm)
      })
    }
  })

  // Open edit form
  function openEditForm(event) {
    if (!isEditMode) return

    const element = event.currentTarget
    const field = element.dataset.field || (element.classList.contains("about-image") ? "image_path" : null)

    if (!field) return

    editField.value = field

    if (field === "image_path") {
      imageUploadGroup.style.display = "block"
      editContent.parentElement.style.display = "none"
    } else {
      imageUploadGroup.style.display = "none"
      editContent.parentElement.style.display = "block"
      editContent.value = aboutData[field] || element.textContent.trim()
    }

    editOverlay.style.display = "flex"
  }

  // Close edit form
  cancelEditButton.addEventListener("click", () => {
    editOverlay.style.display = "none"
  })

  // Submit edit form
  editForm.addEventListener("submit", (event) => {
    event.preventDefault()

    const field = editField.value
    const formData = new FormData()

    if (field === "image_path") {
      if (editImage.files.length > 0) {
        formData.append("image", editImage.files[0])
      } else {
        alert("Bitte wählen Sie ein Bild aus.")
        return
      }
    } else {
      formData.append(field, editContent.value)
    }

    loadingSpinner.style.display = "block"

    fetch("/api/about", {
      method: "PUT",
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok")
        }
        return response.json()
      })
      .then((data) => {
        aboutData = data
        updateUI(data)
        editOverlay.style.display = "none"
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error updating about data:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Speichern der Daten. Bitte versuchen Sie es später erneut.")
      })
  })
})

