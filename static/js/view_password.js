document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const password = document.getElementById('password');

    togglePassword.addEventListener('click', function() {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
    const confirmPasswordToggle = document.getElementById('confirm_password');

    toggleConfirmPassword.addEventListener('click', function() {
        const type = confirmPasswordToggle.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmPasswordToggle.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });
    const form = document.getElementById('registerForm');
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    const passwordError = document.getElementById('passwordError');

    form.addEventListener('submit', function(e) {
        if (password.value !== confirmPassword.value) {
            e.preventDefault();
            passwordError.textContent = "Passwords do not match";
        } else {
            passwordError.textContent = "";
        }
    });
});
