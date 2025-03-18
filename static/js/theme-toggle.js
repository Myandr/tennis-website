// Theme toggle functionality
document.addEventListener("DOMContentLoaded", () => {
  // Check for saved theme preference
  const savedTheme = localStorage.getItem("theme")

  // Set initial theme
  if (savedTheme === "dark") {
    document.documentElement.classList.add("dark")
    updateThemeIcon("dark")
  } else {
    document.documentElement.classList.remove("dark")
    updateThemeIcon("light")
  }

  // Create theme toggle button if it doesn't exist
  if (!document.querySelector(".theme-toggle")) {
    const toggleBtn = document.createElement("button")
    toggleBtn.className = "theme-toggle"
    toggleBtn.setAttribute("aria-label", "Toggle black/white sections")
    toggleBtn.innerHTML = '<i class="fas fa-adjust"></i>' // Using adjust icon for black/white toggle
    document.body.appendChild(toggleBtn)

    // Update icon based on current theme
    updateThemeIcon(document.documentElement.classList.contains("dark") ? "dark" : "light")

    // Add click event listener
    toggleBtn.addEventListener("click", toggleTheme)
  }
})

// Toggle between light and dark themes
function toggleTheme() {
  if (document.documentElement.classList.contains("dark")) {
    document.documentElement.classList.remove("dark")
    localStorage.setItem("theme", "light")
    updateThemeIcon("light")
  } else {
    document.documentElement.classList.add("dark")
    localStorage.setItem("theme", "dark")
    updateThemeIcon("dark")
  }
}

// Update the theme toggle icon
function updateThemeIcon(theme) {
  const toggleBtn = document.querySelector(".theme-toggle")
  if (toggleBtn) {
    // Using the same icon but with different title to indicate current state
    toggleBtn.innerHTML =
      theme === "dark"
        ? '<i class="fas fa-adjust" title="Switch to black background"></i>'
        : '<i class="fas fa-adjust" title="Switch to white background"></i>'
  }
}

