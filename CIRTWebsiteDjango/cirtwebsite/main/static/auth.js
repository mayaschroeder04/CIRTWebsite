// Event listener for form submission
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('auth-form');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);  // No need to pass form.action here
    } else {
        console.error("Error: Form with ID 'auth-form' not found.");
    }

   const { route, params } = getParamsFromHash();
   console.log("HASH", route);  // <- try adding this

   switch (route) {
        case "#set-password":
            switchForm("set_password");
            break;
       case "#verify_otp":
           switchForm("login_otp")
           break;
        default:
            switchForm();
    }
});
// React to hash changes (like when login redirects to #verify_otp)
window.addEventListener("hashchange", () => {
    const { route } = getParamsFromHash();
    console.log("HASH CHANGED:", route);

    switch (route) {
        case "#set-password":
            switchForm("set_password");
            break;
        case "#verify_otp":
            switchForm("login_otp");
            break;
        default:
            switchForm();
    }
});

// Extract parameters from the hash manually
function getParamsFromHash() {
    const hash = window.location.hash;
    const [route, paramString] = hash.split('?');
    const params = new URLSearchParams(paramString);
    return { route, params };
}

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
    const hash = window.location.hash;  // "#set-password?uid=Nw&token=abc123"
    const queryString = hash.includes('?') ? hash.split('?')[1] : '';
    const params = new URLSearchParams(queryString);


    if (!csrfToken) {
        document.getElementById('response-message').innerHTML = '<div class="error">CSRF token not found. Please refresh the page.</div>';
        return;
    }

    // Save existing form values before switching
    const existingValues = {};
    [...form.elements].forEach(input => {
        if (input.name) {
            existingValues[input.name] = input.value;
        }
    });

    form.innerHTML = `<input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">`;

    let buttonText = "Submit";
    console.log("here")
    switch (action) {
        case 'signup':
            // title.textContent = 'Sign Up';
            form.action = '/sign-up/';
            buttonText = "Sign Up";
            form.innerHTML += ` 
                <h2 class="login-sub-title" id="form-title">Sign Up</h2>

                <input type="text" name="username" placeholder="Username" required>
                <div class="name-fields">
                    <input type="text" name="first_name" placeholder="First Name" required>
                    <input type="text" name="last_name" placeholder="Last Name" required>
                </div>
                <input type="email" name="email" placeholder="Email" required>
                <input type="password" name="password" placeholder="Password" required>
                <input type="password" name="confirm_password" placeholder="Confirm Password" required>
            `;
            break;

        case 'reset':
            // title.textContent = 'Reset Password';
            form.action = '/reset-password/';
            buttonText = "Reset Password";
            form.innerHTML += ` 
                <h2 class="login-sub-title" id="form-title">Reset Password</h2>
                <input type="email" name="email" placeholder="Enter your email" required>
            `;
            break;

        case 'forgot':
            // title.textContent = 'Forgot Username';
            form.action = '/forgot-username/';
            buttonText = "Recover Username";
            form.innerHTML += ` 
                <h2 class="login-sub-title" id="form-title">Forgot Username</h2>
                <input type="email" name="email" placeholder="Enter your email" required>
            `;
            break;

        case 'set_password':
            form.action = '/set-password/';
            buttonText = 'Set password'
            form.innerHTML += ` 
                <h2 class="login-sub-title" id="form-title">Reset Password</h2>
                <input type="password" name = "password" placeholder = "New Password" required>
                <input type="password" name="confirm_password" placeholder="Confirm Password" required>
                <input type="hidden" name="uid" value="${params.get('uid') || ''}">
                <input type="hidden" name="token" value="${params.get('token') || ''}">
            `;
            break;

         case 'login_otp':
            form.action = '/login-otp/'
            buttonText = 'Log in'
            form.innerHTML += ` 
                <h2 class="login-sub-title" id="form-title">6-Digit Code</h2>
                <div>Code sent to email</div>
                <input type="text" name="otp" placeholder="Code">
                <input type="hidden" name="username" value="${params.get('username') || ''}">
            `;
            break;

        default:
            // title.textContent = 'Login';
            form.action = '/login/';
            buttonText = "Log In";
            form.innerHTML += `
                <h2 class="login-sub-title" id="form-title">Login</h2>
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
            `;
    }

    form.innerHTML += `<button type="submit">${buttonText}</button>`;
    form.innerHTML += '<div id="response-message" style="color:red;"></div>';

    // Restore previous values if available
    [...form.elements].forEach(input => {
        if (existingValues[input.name]) {
            input.value = existingValues[input.name];
        }
    });
}

function renderFormFromHash() {
    const { route } = getParamsFromHash();

    switch (route) {
        case "#set-password":
            switchForm("set_password");
            break;
        case "#verify_otp":
            switchForm("login_otp");
            break;
        default:
            switchForm();
    }
}

// Handle form submission

// Function to handle form submission
async function handleFormSubmit(e, action) {
    e.preventDefault(); // Prevent default form submission

    const form = e.target;
    const formContainer = document.getElementById('form-container'); // Assuming a wrapper around the form
    const responseDiv = document.getElementById('response-message');
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.textContent;
    const relativeAction = new URL(form.action, window.location.href).pathname;


    // Disable submit button to prevent double submission
    submitButton.disabled = true;
    submitButton.textContent = 'Submitting...';

    try {
        const formData = new FormData(form);
        const csrfToken = getCookie('csrftoken');

        // Make the API call to the backend
        const response = await fetch(form.action, { // Use form.action directly
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrfToken,
                'Accept': 'application/json',
            },
        });

        const data = await response.json();


        if (data.token) {
            // Store the token (for example in localStorage or cookies)
            localStorage.setItem('auth_token', data.token);
            console.log('Token received:', data.token);

            form.innerHTML = '<div>hello</div> '
        } else {
            // Handle expected success/error message
            if (data.success) {
                let successMessage = '';
                const form_action = form.action.slice(16);
                console.log("form", form_action)
                switch (form.action.slice(21)) { // Use form.action directly
                    case '/sign-up/':
                        successMessage = 'Sign-up successful! Check your email for verification.';
                        break;
                    case '/reset-password/':
                        successMessage = 'Password reset link sent! Check your email.';
                        break;
                    case '/forgot-username/':
                        successMessage = 'Username recovery email sent! Check your inbox.';
                        break;
                    case '/login/':
                        successMessage = 'Login successful! Redirecting...';
                        break;
                    case '/set-password/':
                        successMessage = 'Password Reset Successful';
                    case '/login-otp/':
                        successMessage = 'Logging in...';

                    default:
                        console.log('Data success:', data.success); // This will show if the success property exists

                        successMessage = 'Request successful!';
                }

                // Update the form container with the success message
                form.innerHTML = `<div class="success-message">${successMessage}</div>`;

                // If there's a redirect URL, handle the redirect
               if (data.redirect_url) {
                    if (data.redirect_url === "/") {
                        window.location.href = data.redirect_url;
                    } else {
                        window.location.hash = "#" + data.redirect_url;
                        renderFormFromHash();
                    }
                }


          } else {
                const responseMessage = document.getElementById('response-message');
                if (responseMessage) {
                    responseMessage.innerHTML = `
                        <div class = 'error-message' id="response-message" role="alert">
                            <span class="icon-error">
                            </span>
                            <p>${data.message}</p>
                        </div>
                            `;
                }
                submitButton.disabled = false;
                submitButton.textContent = originalButtonText;
            }

        }
    } catch (error) {
        // Catch and display errors that occur during fetch
        form.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        submitButton.disabled = false;
        submitButton.textContent = originalButtonText;
    }
}
