document.addEventListener("DOMContentLoaded", () => {
  // Fetch data for all sections
  fetchEvents()
  fetchBoardMembers()
  fetchLocations()

  function fetchEvents() {
    fetch("/api/events")
      .then((response) => response.json())
      .then((data) => {
        updateEventsUI(data)
      })
      .catch((error) => {
        console.error("Error fetching events:", error)
      })
  }

  function updateEventsUI(events) {
    const eventsList = document.getElementById("events-list")
    if (!eventsList) return

    eventsList.innerHTML = ""

    events.forEach((event) => {
      const row = document.createElement("tr")

      row.innerHTML = `
                <td style="color: rgb(211, 211, 211)">${event.date}</td>
                <td><strong>${event.title}</strong></td>
                <td style="color: rgb(211, 211, 211)">${event.time}</td>
                <td style="color: rgb(211, 211, 211)">${event.location}</td>
            `

      eventsList.appendChild(row)
    })
  }

  function fetchBoardMembers() {
    fetch("/api/board-members")
      .then((response) => response.json())
      .then((data) => {
        updateBoardMembersUI(data)
      })
      .catch((error) => {
        console.error("Error fetching board members:", error)
      })
  }

  function updateBoardMembersUI(members) {
    const boardMembersGrid = document.getElementById("board-members-grid")
    if (!boardMembersGrid) return

    boardMembersGrid.innerHTML = ""

    members.forEach((member) => {
      const card = document.createElement("div")
      card.className = "trainer-card"
      card.setAttribute("data-aos", "flip-up")

      card.innerHTML = `
                <div class="trainer-image">
                    <img src="${member.image_path}" alt="${member.name}" />
                    <div class="trainer-overlay">  alt="${member.name}" />
                    <div class="trainer-overlay">
                        <p>${member.quote || '"Tennis ist nicht nur ein Sport, es ist eine Lebenseinstellung."'}</p>
                    </div>
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
    })
  }

  function fetchLocations() {
    fetch("/api/locations")
      .then((response) => response.json())
      .then((data) => {
        updateLocationsUI(data)
      })
      .catch((error) => {
        console.error("Error fetching locations:", error)
      })
  }

  function updateLocationsUI(locations) {
    const locationsGrid = document.getElementById("locations-grid")
    if (!locationsGrid) return

    locationsGrid.innerHTML = ""

    locations.forEach((location) => {
      const card = document.createElement("div")
      card.className = "location-card"
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
            `

      locationsGrid.appendChild(card)
    })
  }
})

