// Facebook mockup interactions
const FacebookMockup = {
    init() {
        this.setupNavigation();
        this.setupPostInteractions();
    },

    setupNavigation() {
        // Handle navigation link clicks
        const navLinks = document.querySelectorAll('.fb-nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                // Remove active class from all links
                navLinks.forEach(l => l.classList.remove('active'));
                // Add active class to clicked link
                link.classList.add('active');
            });
        });
    },

    setupPostInteractions() {
        // Add hover effects to engagement sections
        document.querySelectorAll('.post-engagement').forEach(section => {
            section.style.cursor = 'pointer';
            section.addEventListener('mouseover', () => {
                section.style.backgroundColor = '#f0f2f5';
            });
            section.addEventListener('mouseout', () => {
                section.style.backgroundColor = 'transparent';
            });
        });

        // Make buttons interactive with conditional click behavior
        document.querySelectorAll('.post .btn').forEach(button => {
            button.addEventListener('click', (e) => {
                // Add animation effect to all buttons
                button.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    button.style.transform = 'scale(1)';
                }, 100);

                // Only prevent default if the button does not have an `href` attribute
                if (!button.hasAttribute('href')) {
                    e.preventDefault();
                }
            });
        });

        // Add hover effect to book cards
        document.querySelectorAll('.book-card').forEach(card => {
            card.addEventListener('mouseover', () => {
                card.style.transform = 'translateY(-2px)';
                card.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
            });
            card.addEventListener('mouseout', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
            });
        });
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    FacebookMockup.init();
});
