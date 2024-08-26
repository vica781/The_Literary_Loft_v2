document.addEventListener('DOMContentLoaded', function() {
    const scrollIndicator = document.querySelector('.scroll-indicator');
    const heroContent = document.getElementById('hero-content');

    if (scrollIndicator && heroContent) {
        scrollIndicator.addEventListener('click', function() {
            heroContent.scrollIntoView({behavior: 'smooth'});
        });
    }
});

