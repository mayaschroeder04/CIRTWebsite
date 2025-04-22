function getCSRFToken() {
    const m = document.cookie.split('; ').find(r => r.startsWith('csrftoken='));
    return m ? m.split('=')[1] : '';
}

document.addEventListener('DOMContentLoaded', function () {
    const contentDiv = document.getElementById('dashboard-content');

    // Profile Info
    document.getElementById('profileBtn').addEventListener('click', () => {
        contentDiv.innerHTML = `
            <div class="profile-box">
                <h3>Your Profile</h3>
                <p><strong>Name:</strong> John Doe</p>
                <p><strong>Email:</strong> johndoe@example.com</p>
                <p><strong>Role:</strong> Student</p>
            </div>
        `;

        // Fetch actual user profile info
        fetch('/user-profile/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            body: '{}'
        })
            .then(res => res.json())
            .then(data => {
                // Dynamically update profile box with actual data
                contentDiv.querySelector('.profile-box').innerHTML = `
                <h3>Your Profile</h3>
                <p><strong>Name:</strong> ${data.name}</p>
                <p><strong>Email:</strong> ${data.email}</p>
                <p><strong>Role:</strong> ${data.role}</p>
            `;
            })
            .catch(err => {
                console.error('Error loading profile:', err);
                contentDiv.innerHTML += '<p style="color: red;">Failed to load profile.</p>';
            });
    });
});