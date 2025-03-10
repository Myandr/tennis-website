document.addEventListener("DOMContentLoaded", () => {
  // Admin controls
  const toggleEditModeButton = document.getElementById("toggle-edit-mode")
  const loadingSpinner = document.getElementById("loading-spinner")

  // Section header edit elements
  const sectionHeaderEditOverlay = document.getElementById("section-header-edit-overlay")
  const sectionHeaderEditForm = document.getElementById("section-header-edit-form")
  const cancelSectionEditButton = document.getElementById("cancel-section-edit")
  const editSectionId = document.getElementById("edit-section-id")
  const editSectionTitle = document.getElementById("edit-section-title")
  const editSectionSubtitle = document.getElementById("edit-section-subtitle")
  const editSectionLinkText = document.getElementById("edit-section-link-text")
  const editSectionLinkUrl = document.getElementById("edit-section-link-url")

  // Event edit elements
  const eventEditOverlay = document.getElementById("event-edit-overlay")
  const eventEditForm = document.getElementById("event-edit-form")
  const eventFormTitle = document.getElementById("event-form-title")
  const cancelEventEditButton = document.getElementById("cancel-event-edit")
  const addEventButton = document.getElementById("add-event-button")
  const editEventId = document.getElementById("edit-event-id")

  // Board member edit elements
  const boardMemberEditOverlay = document.getElementById("board-member-edit-overlay")
  const boardMemberEditForm = document.getElementById("board-member-edit-form")
  const boardMemberFormTitle = document.getElementById("board-member-form-title")
  const cancelBoardMemberEditButton = document.getElementById("cancel-board-member-edit")
  const addBoardMemberButton = document.getElementById("add-board-member-button")
  const editBoardMemberId = document.getElementById("edit-board-member-id")
  const currentBoardMemberImage = document.getElementById("current-board-member-image")

  // Location edit elements
  const locationEditOverlay = document.getElementById("location-edit-overlay")
  const locationEditForm = document.getElementById("location-edit-form")
  const locationFormTitle = document.getElementById("location-form-title")
  const cancelLocationEditButton = document.getElementById("cancel-location-edit")
  const addLocationButton = document.getElementById("add-location-button")
  const editLocationId = document.getElementById("edit-location-id")
  const currentLocationImage = document.getElementById("current-location-image")

  // Confirmation dialog
  const confirmDialog = document.getElementById("confirm-dialog")
  const confirmMessage = document.getElementById("confirm-message")
  const confirmCancel = document.getElementById("confirm-cancel")
  const confirmOk = document.getElementById("confirm-ok")

  let isEditMode = false
  const sectionData = {}
  let eventsData = []
  let boardMembersData = []
  let locationsData = []
  let confirmCallback = null

  // Initialize data
  fetchSectionHeaders()
  fetchEvents()
  fetchBoardMembers()
  fetchLocations()

  // Toggle edit mode
  toggleEditModeButton.addEventListener("click", () => {
    isEditMode = !isEditMode
    document.body.classList.toggle("edit-mode", isEditMode)
    toggleEditModeButton.textContent = isEditMode ? "Beenden" : "Bearbeiten"

    if (isEditMode) {
      // Add click event listeners to editable elements
      document.querySelectorAll(".editable").forEach((element) => {
        element.addEventListener("click", openSectionHeaderEditForm)
      })
    } else {
      // Remove click event listeners
      document.querySelectorAll(".editable").forEach((element) => {
        element.removeEventListener("click", openSectionHeaderEditForm)
      })
    }
  })

  // ===== SECTION HEADERS =====

  function fetchSectionHeaders() {
    const sections = ["termine", "vorstand", "locations"]

    sections.forEach((section) => {
      fetch(`/api/section-headers/${section}`)
        .then((response) => response.json())
        .then((data) => {
          sectionData[section] = data
          updateSectionHeaderUI(section, data)
        })
        .catch((error) => {
          console.error(`Error fetching ${section} section header:`, error)
        })
    })
  }

  function updateSectionHeaderUI(sectionId, data) {
    const titleElement = document.querySelector(`.editable[data-field="title"][data-section="${sectionId}"]`)
    const subtitleElement = document.querySelector(`.editable[data-field="subtitle"][data-section="${sectionId}"]`)
    const linkTextElement = document.querySelector(`.editable[data-field="link_text"][data-section="${sectionId}"]`)

    if (titleElement) titleElement.textContent = data.title
    if (subtitleElement) subtitleElement.textContent = data.subtitle
    if (linkTextElement) {
      linkTextElement.textContent = data.link_text
      linkTextElement.href = data.link_url
    }
  }

  function openSectionHeaderEditForm(event) {
    if (!isEditMode) return

    const element = event.currentTarget
    const sectionId = element.dataset.section
    const field = element.dataset.field

    if (!sectionId || !field) return

    const data = sectionData[sectionId]
    if (!data) return

    editSectionId.value = sectionId
    editSectionTitle.value = data.title
    editSectionSubtitle.value = data.subtitle
    editSectionLinkText.value = data.link_text
    editSectionLinkUrl.value = data.link_url

    sectionHeaderEditOverlay.style.display = "flex"
  }

  // Close section header edit form
  cancelSectionEditButton.addEventListener("click", () => {
    sectionHeaderEditOverlay.style.display = "none"
  })

  // Submit section header edit form
  sectionHeaderEditForm.addEventListener("submit", (event) => {
    event.preventDefault()

    const sectionId = editSectionId.value
    const formData = new FormData()

    formData.append("title", editSectionTitle.value)
    formData.append("subtitle", editSectionSubtitle.value)
    formData.append("link_text", editSectionLinkText.value)
    formData.append("link_url", editSectionLinkUrl.value)

    loadingSpinner.style.display = "block"

    fetch(`/api/section-headers/${sectionId}`, {
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
        sectionData[sectionId] = data
        updateSectionHeaderUI(sectionId, data)
        sectionHeaderEditOverlay.style.display = "none"
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error updating section header:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Speichern der Daten. Bitte versuchen Sie es später erneut.")
      })
  })

  // ===== EVENTS =====

  function fetchEvents() {
    loadingSpinner.style.display = "block"

    fetch("/api/events")
      .then((response) => response.json())
      .then((data) => {
        eventsData = data
        updateEventsUI(data)
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error fetching events:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Laden der Termine. Bitte versuchen Sie es später erneut.")
      })
  }

  function updateEventsUI(events) {
    const eventsList = document.getElementById("events-list")
    eventsList.innerHTML = ""

    events.forEach((event) => {
      const row = document.createElement("tr")
      row.dataset.id = event.id

      row.innerHTML = `
                <td style="color: rgb(211, 211, 211)">${event.date}</td>
                <td><strong>${event.title}</strong></td>
                <td style="color: rgb(211, 211, 211)">${event.time}</td>
                <td style="color: rgb(211, 211, 211)">${event.location}</td>
                ${
                  isEditMode
                    ? `
                <td class="admin-column">
                    <button class="edit-event-button admin-button small">Bearbeiten</button>
                    <button class="delete-event-button admin-button small cancel">Löschen</button>
                </td>
                `
                    : ""
                }
            `

      eventsList.appendChild(row)

      if (isEditMode) {
        row.querySelector(".edit-event-button").addEventListener("click", () => {
          openEventEditForm(event.id)
        })

        row.querySelector(".delete-event-button").addEventListener("click", () => {
          openConfirmDialog(`Sind Sie sicher, dass Sie den Termin "${event.title}" löschen möchten?`, () =>
            deleteEvent(event.id),
          )
        })
      }
    })
  }

  // Add event button
  if (addEventButton) {
    addEventButton.addEventListener("click", () => {
      openEventEditForm()
    })
  }

  function openEventEditForm(eventId = null) {
    eventFormTitle.textContent = eventId ? "Termin bearbeiten" : "Termin hinzufügen"
    editEventId.value = eventId || ""

    if (eventId) {
      const event = eventsData.find((e) => e.id === eventId)
      if (event) {
        document.getElementById("edit-event-date").value = event.date
        document.getElementById("edit-event-title").value = event.title
        document.getElementById("edit-event-time").value = event.time
        document.getElementById("edit-event-location").value = event.location
      }
    } else {
      eventEditForm.reset()
    }

    eventEditOverlay.style.display = "flex"
  }

  // Close event edit form
  cancelEventEditButton.addEventListener("click", () => {
    eventEditOverlay.style.display = "none"
  })

  // Submit event edit form
  eventEditForm.addEventListener("submit", (event) => {
    event.preventDefault()

    const eventId = editEventId.value
    const formData = new FormData(eventEditForm)

    loadingSpinner.style.display = "block"

    const url = eventId ? `/api/events/${eventId}` : "/api/events"
    const method = eventId ? "PUT" : "POST"

    fetch(url, {
      method: method,
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok")
        }
        return response.json()
      })
      .then((data) => {
        fetchEvents() // Refresh events
        eventEditOverlay.style.display = "none"
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error saving event:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Speichern des Termins. Bitte versuchen Sie es später erneut.")
      })
  })

  function deleteEvent(eventId) {
    loadingSpinner.style.display = "block"

    fetch(`/api/events/${eventId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok")
        }
        return response.json()
      })
      .then((data) => {
        fetchEvents() // Refresh events
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error deleting event:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Löschen des Termins. Bitte versuchen Sie es später erneut.")
      })
  }

  // ===== BOARD MEMBERS =====

  function fetchBoardMembers() {
    loadingSpinner.style.display = "block"

    fetch("/api/board-members")
      .then((response) => response.json())
      .then((data) => {
        boardMembersData = data
        updateBoardMembersUI(data)
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error fetching board members:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Laden der Vorstandsmitglieder. Bitte versuchen Sie es später erneut.")
      })
  }

  function updateBoardMembersUI(members) {
    const boardMembersGrid = document.getElementById("board-members-grid")
    boardMembersGrid.innerHTML = ""

    members.forEach((member) => {
      const card = document.createElement("div")
      card.className = "trainer-card"
      card.dataset.id = member.id
      card.setAttribute("data-aos", "flip-up")

      card.innerHTML = `
                <div class="trainer-image">
                    <img src="${member.image_path}" alt="${member.name}" />
                    <div class="trainer-overlay">
                        <p>${member.quote || '"Tennis ist nicht nur ein Sport, es ist eine Lebenseinstellung."'}</p>
                    </div>
                    ${
                      isEditMode
                        ? `
                    <div class="admin-actions">
                        <button class="edit-board-member-button admin-button small">Bearbeiten</button>
                        <button class="delete-board-member-button admin-button small cancel">Löschen</button>
                    </div>
                    `
                        : ""
                    }
                </div>
                <div class="trainer-info">
                    <h3 class="trainer-name">${member.name}</h3>
                    <div class="trainer-title" style="border-bottom: 1px solid grey; padding-bottom: 15px;">${member.position}</div>
                    <p class="trainer-description">
                        ${member.email ? `<strong>Email:</strong> ${member.email}<br>` : ""}
                        ${member.phone ? `<strong>Tel. Nr.:</strong> ${member.phone}` : ""}
                    </p>
                </div>
            `

      boardMembersGrid.appendChild(card)

      if (isEditMode) {
        card.querySelector(".edit-board-member-button").addEventListener("click", () => {
          openBoardMemberEditForm(member.id)
        })

        card.querySelector(".delete-board-member-button").addEventListener("click", () => {
          openConfirmDialog(`Sind Sie sicher, dass Sie das Vorstandsmitglied "${member.name}" löschen möchten?`, () =>
            deleteBoardMember(member.id),
          )
        })
      }
    })
  }

  // Add board member button
  if (addBoardMemberButton) {
    addBoardMemberButton.addEventListener("click", () => {
      openBoardMemberEditForm()
    })
  }

  function openBoardMemberEditForm(memberId = null) {
    boardMemberFormTitle.textContent = memberId ? "Vorstandsmitglied bearbeiten" : "Vorstandsmitglied hinzufügen"
    editBoardMemberId.value = memberId || ""

    if (memberId) {
      const member = boardMembersData.find((m) => m.id === memberId)
      if (member) {
        document.getElementById("edit-board-member-name").value = member.name
        document.getElementById("edit-board-member-position").value = member.position
        document.getElementById("edit-board-member-email").value = member.email
        document.getElementById("edit-board-member-phone").value = member.phone
        document.getElementById("edit-board-member-quote").value = member.quote

        // Show current image
        currentBoardMemberImage.innerHTML = `<img src="${member.image_path}" alt="${member.name}" style="max-width: 100px; max-height: 100px;">`
        currentBoardMemberImage.style.display = "block"
      }
    } else {
      boardMemberEditForm.reset()
      currentBoardMemberImage.innerHTML = ""
      currentBoardMemberImage.style.display = "none"
    }

    boardMemberEditOverlay.style.display = "flex"
  }

  // Close board member edit form
  cancelBoardMemberEditButton.addEventListener("click", () => {
    boardMemberEditOverlay.style.display = "none"
  })

  // Submit board member edit form
  boardMemberEditForm.addEventListener("submit", (event) => {
    event.preventDefault()

    const memberId = editBoardMemberId.value
    const formData = new FormData(boardMemberEditForm)

    // Validate image for new board members
    if (!memberId && !formData.get("image").size) {
      alert("Bitte wählen Sie ein Bild aus.")
      return
    }

    loadingSpinner.style.display = "block"

    const url = memberId ? `/api/board-members/${memberId}` : "/api/board-members"
    const method = memberId ? "PUT" : "POST"

    fetch(url, {
      method: method,
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok")
        }
        return response.json()
      })
      .then((data) => {
        fetchBoardMembers() // Refresh board members
        boardMemberEditOverlay.style.display = "none"
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error saving board member:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Speichern des Vorstandsmitglieds. Bitte versuchen Sie es später erneut.")
      })
  })

  function deleteBoardMember(memberId) {
    loadingSpinner.style.display = "block"

    fetch(`/api/board-members/${memberId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok")
        }
        return response.json()
      })
      .then((data) => {
        fetchBoardMembers() // Refresh board members
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error deleting board member:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Löschen des Vorstandsmitglieds. Bitte versuchen Sie es später erneut.")
      })
  }

  // ===== LOCATIONS =====

  function fetchLocations() {
    loadingSpinner.style.display = "block"

    fetch("/api/locations")
      .then((response) => response.json())
      .then((data) => {
        locationsData = data
        updateLocationsUI(data)
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error fetching locations:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Laden der Standorte. Bitte versuchen Sie es später erneut.")
      })
  }

  function updateLocationsUI(locations) {
    const locationsGrid = document.getElementById("locations-grid")
    locationsGrid.innerHTML = ""

    locations.forEach((location) => {
      const card = document.createElement("div")
      card.className = "location-card"
      card.dataset.id = location.id
      card.setAttribute("data-aos", "flip-up")

      if (location.link) {
        card.setAttribute("onclick", `window.location.href='${location.link}';`)
      }

      card.innerHTML = `
                <img src="${location.image_path}" alt="${location.title}" />
                <div class="arrow-icon"><i class="fa fa-arrow-right"></i></div>
                <div class="location-info">
                    <h3>${location.title}</h3>
                    ${location.description ? `<div class="location-times">${location.description}</div>` : ""}
                    ${location.address ? `<div class="location-address">${location.address}</div>` : ""}
                </div>
                ${
                  isEditMode
                    ? `
                <div class="admin-actions">
                    <button class="edit-location-button admin-button small">Bearbeiten</button>
                    <button class="delete-location-button admin-button small cancel">Löschen</button>
                </div>
                `
                    : ""
                }
            `

      locationsGrid.appendChild(card)

      if (isEditMode) {
        const editButton = card.querySelector(".edit-location-button")
        const deleteButton = card.querySelector(".delete-location-button")

        // Stop propagation to prevent navigation when clicking buttons
        editButton.addEventListener("click", (e) => {
          e.stopPropagation()
          openLocationEditForm(location.id)
        })

        deleteButton.addEventListener("click", (e) => {
          e.stopPropagation()
          openConfirmDialog(`Sind Sie sicher, dass Sie den Standort "${location.title}" löschen möchten?`, () =>
            deleteLocation(location.id),
          )
        })
      }
    })
  }

  // Add location button
  if (addLocationButton) {
    addLocationButton.addEventListener("click", () => {
      openLocationEditForm()
    })
  }

  function openLocationEditForm(locationId = null) {
    locationFormTitle.textContent = locationId ? "Standort bearbeiten" : "Standort hinzufügen"
    editLocationId.value = locationId || ""

    if (locationId) {
      const location = locationsData.find((l) => l.id === locationId)
      if (location) {
        document.getElementById("edit-location-title").value = location.title
        document.getElementById("edit-location-description").value = location.description
        document.getElementById("edit-location-address").value = location.address
        document.getElementById("edit-location-link").value = location.link

        // Show current image
        currentLocationImage.innerHTML = `<img src="${location.image_path}" alt="${location.title}" style="max-width: 100px; max-height: 100px;">`
        currentLocationImage.style.display = "block"
      }
    } else {
      locationEditForm.reset()
      currentLocationImage.innerHTML = ""
      currentLocationImage.style.display = "none"
    }

    locationEditOverlay.style.display = "flex"
  }

  // Close location edit form
  cancelLocationEditButton.addEventListener("click", () => {
    locationEditOverlay.style.display = "none"
  })

  // Submit location edit form
  locationEditForm.addEventListener("submit", (event) => {
    event.preventDefault()

    const locationId = editLocationId.value
    const formData = new FormData(locationEditForm)

    // Validate image for new locations
    if (!locationId && !formData.get("image").size) {
      alert("Bitte wählen Sie ein Bild aus.")
      return
    }

    loadingSpinner.style.display = "block"

    const url = locationId ? `/api/locations/${locationId}` : "/api/locations"
    const method = locationId ? "PUT" : "POST"

    fetch(url, {
      method: method,
      body: formData,
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok")
        }
        return response.json()
      })
      .then((data) => {
        fetchLocations() // Refresh locations
        locationEditOverlay.style.display = "none"
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error saving location:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Speichern des Standorts. Bitte versuchen Sie es später erneut.")
      })
  })

  function deleteLocation(locationId) {
    loadingSpinner.style.display = "block"

    fetch(`/api/locations/${locationId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok")
        }
        return response.json()
      })
      .then((data) => {
        fetchLocations() // Refresh locations
        loadingSpinner.style.display = "none"
      })
      .catch((error) => {
        console.error("Error deleting location:", error)
        loadingSpinner.style.display = "none"
        alert("Fehler beim Löschen des Standorts. Bitte versuchen Sie es später erneut.")
      })
  }

  // ===== CONFIRMATION DIALOG =====

  function openConfirmDialog(message, callback) {
    confirmMessage.textContent = message
    confirmCallback = callback
    confirmDialog.style.display = "flex"
  }

  confirmCancel.addEventListener("click", () => {
    confirmDialog.style.display = "none"
    confirmCallback = null
  })

  confirmOk.addEventListener("click", () => {
    confirmDialog.style.display = "none"
    if (confirmCallback) {
      confirmCallback()
      confirmCallback = null
    }
  })
})

