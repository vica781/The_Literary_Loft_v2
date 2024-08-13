document.addEventListener('DOMContentLoaded', function() {
    const scrollIndicator = document.querySelector('.scroll-indicator');
    const heroContent = document.getElementById('hero-content');

    if (scrollIndicator && heroContent) {
        scrollIndicator.addEventListener('click', function() {
            heroContent.scrollIntoView({behavior: 'smooth'});
        });
    }
});

function updateCartCount(count) {
  document.querySelector('.cart-count').textContent = count;
}

updateCartCount(10); // 10 is the count of items in the cart