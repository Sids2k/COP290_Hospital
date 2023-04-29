// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Get the login form element
    var loginForm = document.getElementById('login-form');

    // Add submit event listener to the login form
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission

        // Get the username and password input values
        var usernameInput = document.getElementById('username-input');
        var passwordInput = document.getElementById('password-input');
        var username = usernameInput.value;
        var password = passwordInput.value;

        // Validate the username and password (replace this with your own logic)
        if (username === 'username' && password === 'password') {
            alert('Login successful!'); // Replace with your own logic
        } else {
            alert('Invalid username or password'); // Replace with your own logic
        }

        // Clear the username and password inputs
        usernameInput.value = '';
        passwordInput.value = '';
});
});