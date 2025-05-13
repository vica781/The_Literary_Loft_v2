document.addEventListener('DOMContentLoaded', function() {
	const searchInput = document.getElementById('search-input');
	const suggestionsBox = document.getElementById('suggestions');
	const searchButton = document.getElementById('search-button');

	searchInput.addEventListener('input', function() {
		const query = searchInput.value.trim();

		if (query.length > 2) {
			fetch(`/search-suggestions/?q=${query}`)
				.then(response => response.json())
				.then(data => {
					let suggestionsHTML = data.map(item => `
                        <div class="suggestion-item">
                            <a href="/book/${item.id}/">${item.title} by ${item.author}</a>
                        </div>
                    `).join('');

					suggestionsHTML += `
                        <div class="suggestion-item search-for">
                            <a href="/search/?q=${encodeURIComponent(query)}">Search for "${query}"</a>
                        </div>
                    `;

					suggestionsBox.innerHTML = suggestionsHTML;
					suggestionsBox.style.display = 'block';
				})
				.catch(error => {
					console.error('Error fetching search suggestions:', error);
				});
		} else {
			suggestionsBox.style.display = 'none';
		}
	});

	searchButton.addEventListener('click', function() {
		const query = searchInput.value.trim();
		if (query) {
			window.location.href = `/search/?q=${encodeURIComponent(query)}`;
		}
	});

	document.addEventListener('click', function(event) {
		if (!event.target.closest('.search-bar')) {
			suggestionsBox.style.display = 'none';
		}
	});
});