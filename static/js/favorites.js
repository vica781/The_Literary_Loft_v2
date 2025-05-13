/* global $ */
$(document).ready(function() {
	// Get CSRF token from cookies
	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}

	const csrftoken = getCookie('csrftoken');

	// Check if the HTTP method is CSRF-safe
	function csrfSafeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	// Set up AJAX to include the CSRF token for unsafe HTTP methods
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

	// Update the favorite count in the UI
	function updateFavoriteCount(count) {
		$('.favorites-count').text(count);
	}

	// Function to handle clicking the favorite button
	function handleFavoriteClick(e) {
		e.preventDefault();
		let $btn = $(this);
		let bookId = $btn.data('book-id');
		let isOnFavoritesPage = $btn.closest('.favorite-book-item').length > 0;

		// If the user is not authenticated, show a toast notification and return
		if ($btn.hasClass('guest')) {
			$('#toastNotification').toast('show');
			return;
		}

		// If the user is authenticated, send AJAX request to toggle favorite
		$.ajax({
			url: '/books/toggle-favorite/' + bookId + '/',
			method: 'POST',
			success: function(data) {
				if (data.is_favorite) {
					$btn.addClass('active');
				} else {
					$btn.removeClass('active');
					if (isOnFavoritesPage) {
						$btn.closest('.favorite-book-item').remove();
					}
				}
				updateFavoriteCount(data.favorite_count);
			},
			error: function(jqXHR, textStatus, errorThrown) {
				console.error("AJAX error: " + textStatus + ' : ' + errorThrown);
			}
		});
	}

	// Event delegation to handle clicks on favorite buttons
	$(document).on('click', '.favorite-btn', handleFavoriteClick);

	// If on the favorites page and there are no favorite books, show a message
	if ($('#favorites-container').length > 0) {
		if ($('.favorite-book-item').length === 0) {
			$('#favorites-container').html('<p class="nunito">You haven\'t added any books to your favorites yet.</p>');
		}
	}
});