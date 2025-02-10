function openModal() {
    document.getElementById("modal").style.display = "block";
    document.getElementById("modal-content").innerHTML = `
            <div class="modal-content">
                <h2>Login</h2>
                <p onclick="showRegister()">New here? Sign up now!</p>
                <button onclick="continueAsGuest()">Continue as Guest</button>
            </div>
        `;
}

function showRegister() {
    document.getElementById("modal-content").innerHTML = `
            <div class="modal-content">
                <h2>Register</h2>
                <p onclick="openModal()">Already have an account? Login</p>
                <button onclick="continueAsGuest()">Continue as Guest</button>
            </div>
        `;
}

function closeModal() {
    document.getElementById("modal").style.display = "none";
}

function continueAsGuest() {
    window.location.href = "fake_journal.html";
}

function switchTab(clickedTab) {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    clickedTab.classList.add('active');
}