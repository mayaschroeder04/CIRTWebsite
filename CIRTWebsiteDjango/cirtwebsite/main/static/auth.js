function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
}

function switchForm(action) {
    const form = document.getElementById('auth-form');
    const title = document.getElementById('form-title');
    const csrfToken = getCookie('csrftoken');

    if (!csrfToken) {
        console.error('CSRF token not found.');
        return;
    }

    form.innerHTML = `<input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">`;

    switch (action) {
        case 'signup':
            title.textContent = 'Sign Up';
            form.action = '/signup/';
            form.innerHTML += `
                <input type="text" name="username" placeholder="Username" required>
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <input type="password" name="confirm_password" placeholder="Confirm Password" required>
                <button type="submit">Sign Up</button>
            `;
            break;

        case 'reset':
            title.textContent = 'Reset Password';
            form.action = '/reset_password/';
            form.innerHTML += `
                <input type="email" name="email" placeholder="Enter your email" required>
                <button type="submit">Reset Password</button>
            `;
            break;

        case 'forgot':
            title.textContent = 'Forgot Username';
            form.action = '/forgot-username/';
            form.innerHTML += `
                <input type="email" name="email" placeholder="Enter your email" required>
                <button type="submit">Recover Username</button>
            `;
            break;

        default:
            title.textContent = 'Login';
            form.action = '/login_view/';
            form.innerHTML += `
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            `;
    }
}
document.getElementById('auth-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Stop redirect

    const form = e.target;
    const responseDiv = document.getElementById('response-message');

    fetch(form.action, {  // Use the form's built-in action URL
        method: 'POST',
        body: new FormData(form),
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Accept': 'application/json'  // Ensure Django returns JSON
        }
    })
    .then(response => response.json())  // Parse JSON
    .then(data => {
        // Display message without leaving the page
        responseDiv.innerHTML = `
            <div class="${data.success ? 'success' : 'error'}">
                ${data.message}
            </div>
        `;
    })
    .catch(error => {
        responseDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
    });
});