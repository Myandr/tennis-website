document.addEventListener('DOMContentLoaded', function() {
    const archiveGrid = document.getElementById('archive-grid');
    const searchInput = document.getElementById('archive-search');
    const yearFilter = document.getElementById('year-filter');
    
    let allNews = [];
    
    // Load archived news
    function loadArchivedNews() {
        fetch('/api/news?archived=true')
            .then(response => response.json())
            .then(data => {
                allNews = data;
                
                if (data.length === 0) {
                    archiveGrid.innerHTML = '<p class="no-results">Keine archivierten News vorhanden</p>';
                    return;
                }
                
                // Populate year filter
                populateYearFilter(data);
                
                // Display all news initially
                displayNews(data);
            })
            .catch(error => {
                console.error('Error loading archived news:', error);
                archiveGrid.innerHTML = '<p class="error-message">Fehler beim Laden der archivierten News</p>';
            });
    }
    
    // Populate year filter with available years
    function populateYearFilter(newsData) {
        const years = new Set();
        
        newsData.forEach(news => {
            const year = new Date(news.date).getFullYear();
            years.add(year);
        });
        
        // Sort years in descending order
        const sortedYears = Array.from(years).sort((a, b) => b - a);
        
        // Add years to the filter
        sortedYears.forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearFilter.appendChild(option);
        });
    }
    
    // Display news in the grid
    function displayNews(newsData) {
        archiveGrid.innerHTML = '';
        
        if (newsData.length === 0) {
            archiveGrid.innerHTML = '<p class="no-results">Keine News gefunden</p>';
            return;
        }
        
        newsData.forEach(news => {
            const card = createNewsCard(news);
            archiveGrid.appendChild(card);
        });
    }
    
    // Create a news card
    function createNewsCard(news) {
        const card = document.createElement('div');
        card.className = 'archive-card';
        card.dataset.id = news.id;
        
        const formattedDate = new Date(news.date).toLocaleDateString('de-DE', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
        
        card.innerHTML = `
            <div class="archive-card-image">
                <img src="${news.image_url}" alt="${news.title}">
            </div>
            <div class="archive-card-content">
                <div class="archive-card-date">${formattedDate}</div>
                <h3 class="archive-card-title">${news.title}</h3>
                <p class="archive-card-excerpt">${news.excerpt}</p>
                <div class="archive-card-actions">
                    <a href="/news/${news.id}" class="read-more">Weiterlesen</a>
                    ${isAdmin ? '<button class="delete-button" data-id="' + news.id + '">Löschen</button>' : ''}
                </div>
            </div>
        `;
        
        // Add event listener for delete button if admin
        if (isAdmin) {
            const deleteButton = card.querySelector('.delete-button');
            deleteButton.addEventListener('click', function() {
                const newsId = this.getAttribute('data-id');
                if (confirm('Möchten Sie diese archivierte News wirklich löschen?')) {
                    deleteNews(newsId);
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
            // Remove the news from the array
            allNews = allNews.filter(news => news.id !== parseInt(newsId));
            
            // Remove the card from the DOM
            const card = document.querySelector(`.archive-card[data-id="${newsId}"]`);
            if (card) {
                card.remove();
            }
            
            // Check if there are no more news
            if (allNews.length === 0) {
                archiveGrid.innerHTML = '<p class="no-results">Keine archivierten News vorhanden</p>';
            }
            
            alert('Archivierte News erfolgreich gelöscht!');
        })
        .catch(error => {
            console.error('Error deleting news:', error);
            alert('Fehler beim Löschen der archivierten News');
        });
    }
    
    // Filter news by search term and year
    function filterNews() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedYear = yearFilter.value;
        
        let filteredNews = allNews;
        
        // Filter by search term
        if (searchTerm) {
            filteredNews = filteredNews.filter(news => 
                news.title.toLowerCase().includes(searchTerm) || 
                news.excerpt.toLowerCase().includes(searchTerm) || 
                news.content.toLowerCase().includes(searchTerm)
            );
        }
        
        // Filter by year
        if (selectedYear !== 'all') {
            filteredNews = filteredNews.filter(news => {
                const newsYear = new Date(news.date).getFullYear().toString();
                return newsYear === selectedYear;
            });
        }
        
        // Display filtered news
        displayNews(filteredNews);
    }
    
    // Add event listeners for search and filter
    if (searchInput) {
        searchInput.addEventListener('input', filterNews);
    }
    
    if (yearFilter) {
        yearFilter.addEventListener('change', filterNews);
    }
    
    // Check if user is admin (set by the server in a script tag)
    const isAdmin = typeof window.isAdmin !== 'undefined' ? window.isAdmin : false;
    
    // Load news when the page loads
    loadArchivedNews();
});
