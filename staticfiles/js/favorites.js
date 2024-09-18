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

    $('.favorite-btn').click(function(e) {
        e.preventDefault();
        var bookId = $(this).data('book-id');
        var $btn = $(this);

        $.ajax({
            url: '/books/toggle-favorite/' + bookId + '/',
            method: 'POST',
            success: function(data) {
                if (data.is_favorite) {
                    $btn.addClass('active');
                } else {
                    $btn.removeClass('active');
                }
                updateFavoriteCount(data.favorite_count);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("AJAX error: " + textStatus + ' : ' + errorThrown);
            }
        });
    });

    function updateFavoriteCount(count) {
        $('#favorite-count').text(count);
    }
});