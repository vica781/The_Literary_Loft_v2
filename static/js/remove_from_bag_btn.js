document.addEventListener('DOMContentLoaded', function() {
	const removeModal = document.getElementById('removeModal');
	const bookTitleSpan = document.getElementById('bookTitle');
	const removeBookIdInput = document.getElementById('removeBookId');
	const removeButtons = document.querySelectorAll('.remove-btn');

	removeButtons.forEach(button => {
		button.addEventListener('click', function(event) {
			const bookId = this.getAttribute('data-book-id');
			const bookTitle = this.getAttribute('data-book-title');

			console.log('Book ID:', bookId);
			console.log('Book Title:', bookTitle);

			if (bookTitle && bookTitleSpan) {
				bookTitleSpan.textContent = bookTitle;
			} else {
				console.error('Book title not found or bookTitleSpan not available');
			}
			if (removeBookIdInput) {
				removeBookIdInput.value = bookId;
			} else {
				console.error('removeBookIdInput not found');
			}

			// Manually show the modal
			if (removeModal) {
				$(removeModal).modal('show');
			} else {
				console.error('Modal element not found');
			}
		});
	});
});