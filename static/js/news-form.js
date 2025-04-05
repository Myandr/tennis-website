document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Skip if it's a link to another page
            if (this.tagName === 'A') return;
            
            const tabId = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to current button and content
            this.classList.add('active');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // File upload preview
    const fileInput = document.getElementById('image');
    const fileNameDisplay = document.getElementById('file-name');
    const imagePreview = document.getElementById('image-preview');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const fileName = this.files[0].name;
                fileNameDisplay.textContent = fileName;
                
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);
            } else {
                fileNameDisplay.textContent = '';
                imagePreview.src = '/static/images/placeholder.jpg';
            }
        });
    }
    
    // Live preview for news
    const titleInput = document.getElementById('title');
    const dateInput = document.getElementById('date');
    const excerptInput = document.getElementById('excerpt');
    const titlePreview = document.getElementById('title-preview');
    const datePreview = document.getElementById('date-preview');
    const excerptPreview = document.getElementById('excerpt-preview');
    
    if (titleInput) {
        titleInput.addEventListener('input', function() {
            titlePreview.textContent = this.value || 'Titel der News';
        });
    }
    
    if (dateInput) {
        dateInput.addEventListener('input', function() {
            const date = new Date(this.value);
            const formattedDate = date.toLocaleDateString('de-DE', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
            datePreview.textContent = formattedDate;
        });
        
        // Set today's date as default
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        dateInput.value = `${year}-${month}-${day}`;
        
        // Trigger input event to update preview
        const inputEvent = new Event('input');
        dateInput.dispatchEvent(inputEvent);
    }
    
    if (excerptInput) {
        excerptInput.addEventListener('input', function() {
            excerptPreview.textContent = this.value || 'Kurzbeschreibung der News...';
        });
    }
    
    // Load news for delete tab
    const deleteNewsList = document.getElementById('delete-news-list');
    const archiveNewsList = document.getElementById('archive-news-list');
    
    // Function to load news
    function loadNews() {
        // Load news for deletion
        if (deleteNewsList) {
            fetch('/api/news?archived=false')
                .then(response => response.json())
                .then(data => {
                    if (data.length === 0) {
                        deleteNewsList.innerHTML = '<p class="no-results">Keine News vorhanden</p>';
                        return;
                    }
                    
                    deleteNewsList.innerHTML = '';
                    data.forEach(news => {
                        const newsCard = createNewsCard(news, true, false);
                        deleteNewsList.appendChild(newsCard);
                    });
                })
                .catch(error => {
                    console.error('Error loading news:', error);
                    deleteNewsList.innerHTML = '<p class="error-message">Fehler beim Laden der News</p>';
                });
        }
        
        // Load news for archiving
        if (archiveNewsList) {
            fetch('/api/news?archived=false')
                .then(response => response.json())
                .then(data => {
                    if (data.length === 0) {
                        archiveNewsList.innerHTML = '<p class="no-results">Keine News vorhanden</p>';
                        return;
                    }
                    
                    archiveNewsList.innerHTML = '';
                    data.forEach(news => {
                        const newsCard = createNewsCard(news, false, true);
                        archiveNewsList.appendChild(newsCard);
                    });
                })
                .catch(error => {
                    console.error('Error loading news:', error);
                    archiveNewsList.innerHTML = '<p class="error-message">Fehler beim Laden der News</p>';
                });
        }
    }
    
    // Create news card for the lists
    function createNewsCard(news, showDelete, showArchive) {
        const card = document.createElement('div');
        card.className = 'news-card';
        card.dataset.id = news.id;
        
        const formattedDate = new Date(news.date).toLocaleDateString('de-DE', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
        
        card.innerHTML = `
            <div class="news-card-image">
                <img src="${news.image_url}" alt="${news.title}">
            </div>
            <div class="news-card-content">
                <div class="news-card-date">${formattedDate}</div>
                <h3 class="news-card-title">${news.title}</h3>
                <p class="news-card-excerpt">${news.excerpt}</p>
                <div class="news-card-actions">
                    ${showDelete ? '<button class="action-button delete-button" data-id="' + news.id + '">Löschen</button>' : ''}
                    ${showArchive ? '<button class="action-button archive-button" data-id="' + news.id + '">Archivieren</button>' : ''}
                </div>
            </div>
        `;
        
        // Add event listeners for buttons
        if (showDelete) {
            const deleteButton = card.querySelector('.delete-button');
            deleteButton.addEventListener('click', function() {
                const newsId = this.getAttribute('data-id');
                if (confirm('Möchten Sie diese News wirklich löschen?')) {
                    deleteNews(newsId);
                }
            });
        }
        
        if (showArchive) {
            const archiveButton = card.querySelector('.archive-button');
            archiveButton.addEventListener('click', function() {
                const newsId = this.getAttribute('data-id');
                if (confirm('Möchten Sie diese News ins Archiv verschieben?')) {
                    archiveNews(newsId);
                }
            });
        }
        
        return card;
    }
    
    // Delete news function
    function deleteNews(newsId) {
        fetch(`/api/news/${newsId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Remove the card from the DOM
            const card = document.querySelector(`.news-card[data-id="${newsId}"]`);
            if (card) {
                card.remove();
            }
            
            // Check if there are no more news
            if (deleteNewsList && deleteNewsList.children.length === 0) {
                deleteNewsList.innerHTML = '<p class="no-results">Keine News vorhanden</p>';
            }
            
            alert('News erfolgreich gelöscht!');
        })
        .catch(error => {
            console.error('Error deleting news:', error);
            alert('Fehler beim Löschen der News');
        });
    }
    
    // Archive news function
    function archiveNews(newsId) {
        fetch(`/api/news/${newsId}/archive`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Remove the card from the DOM
            const card = document.querySelector(`.news-card[data-id="${newsId}"]`);
            if (card) {
                card.remove();
            }
            
            // Check if there are no more news
            if (archiveNewsList && archiveNewsList.children.length === 0) {
                archiveNewsList.innerHTML = '<p class="no-results">Keine News vorhanden</p>';
            }
            
            alert('News erfolgreich archiviert!');
        })
        .catch(error => {
            console.error('Error archiving news:', error);
            alert('Fehler beim Archivieren der News');
        });
    }
    
    // Load news when the page loads
    loadNews();
    
    // Form submission
    const addNewsForm = document.getElementById('add-news-form');
    if (addNewsForm) {
        addNewsForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/api/news', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                alert('News erfolgreich hinzugefügt!');
                this.reset();
                
                // Reset preview
                imagePreview.src = '/static/images/placeholder.jpg';
                fileNameDisplay.textContent = '';
                titlePreview.textContent = 'Titel der News';
                excerptPreview.textContent = 'Kurzbeschreibung der News...';
                
                // Set today's date again
                const today = new Date();
                const year = today.getFullYear();
                const month = String(today.getMonth() + 1).padStart(2, '0');
                const day = String(today.getDate()).padStart(2, '0');
                dateInput.value = `${year}-${month}-${day}`;
                
                // Trigger input event to update preview
                const inputEvent = new Event('input');
                dateInput.dispatchEvent(inputEvent);
            })
            .catch(error => {
                console.error('Error adding news:', error);
                alert('Fehler beim Hinzufügen der News');
            });
        });
    }
});
