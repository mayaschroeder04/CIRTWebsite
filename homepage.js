function openModal() {
    document.getElementById("modal").style.display = "block";
    document.getElementById("modal-content").innerHTML = `
        <div class="modal-content">
            <h2>Log In</h2>
            <p class="switch-link" onclick="showRegister()">New here? Sign up now!</p>
            <div class="button-container">
                <button class="primary-btn" onclick="redirectToLogin()">Log In</button>
                <button class="secondary-btn" onclick="continueAsGuest()">Continue as Guest</button>
            </div>
            <button class="close-btn" onclick="closeModal()">X</button>
        </div>
    `;
}

function showRegister() {
    document.getElementById("modal-content").innerHTML = `
        <div class="modal-content">
            <h2>Register</h2>
            <p class="switch-link" onclick="openModal()">Already have an account? Log in</p>
            <div class="button-container">
                <button class="primary-btn" onclick="redirectToRegister()">Sign Up</button>
                <button class="secondary-btn" onclick="continueAsGuest()">Continue as Guest</button>
            </div>
            <button class="close-btn" onclick="closeModal()">X</button>
        </div>
    `;
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}


function continueAsGuest() {
    window.location.href = "fake_journal.html";
}