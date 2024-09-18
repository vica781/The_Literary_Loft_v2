$(document).ready(function() {
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

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function updateFavoriteCount(count) {
        $('.favorites-count').text(count);
    }

    function handleFavoriteClick(e) {
        e.preventDefault();
        var $btn = $(this);
        var bookId = $btn.data('book-id');
        var isOnFavoritesPage = $btn.closest('.favorite-book-item').length > 0;

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

    // Use event delegation to handle clicks on favorite buttons
    $(document).on('click', '.favorite-btn', handleFavoriteClick);

    // Check if we're on the favorites page
    if ($('#favorites-container').length > 0) {
        // If there are no favorite books, show a message
        if ($('.favorite-book-item').length === 0) {
            $('#favorites-container').html('<p class="nunito">You haven\'t added any books to your favorites yet.</p>');
        }
    }
});