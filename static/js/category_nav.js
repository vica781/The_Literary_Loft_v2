document.addEventListener('DOMContentLoaded', function () {
    const toggler = document.querySelector('.navbar-toggler');
    const categoryNav = document.querySelector('.category-nav');

    if (toggler && categoryNav) {
        toggler.addEventListener('click', function () {
            categoryNav.classList.toggle('open');
        });
    }
});
