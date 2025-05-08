function getCSRFToken() {
    const m = document.cookie.split('; ').find(r => r.startsWith('csrftoken='));
    return m ? m.split('=')[1] : '';
}

function setActiveTab(tabId) {
    document.querySelectorAll('.dashboard-navbar span').forEach(span => {
        span.classList.remove('active-tab');
    });
    document.getElementById(tabId).classList.add('active-tab');
}

document.addEventListener('DOMContentLoaded', function () {
    const contentDiv = document.getElementById('dashboard-content');

    // Profile Info
    document.getElementById('profileBtn').addEventListener('click', () => {
        setActiveTab('profileBtn')
        contentDiv.innerHTML = `
            <div class="profile-box">
                <h3>Your Profile</h3>
                <p><strong>Name:</strong> John Doe</p>
                <p><strong>Email:</strong> johndoe@example.com</p>
                <p><strong>Role:</strong> Student</p>
            </div>
        `;

        // Fetch actual user profile info
        fetch(`/user-profile/`, {
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
    // Pending Journals
    document.getElementById('pendingBtn').addEventListener('click', () => {
        setActiveTab('pendingBtn');
        contentDiv.innerHTML = `
        <div class="pending-journals-box">
            <h3>Pending Journals for Review</h3>
            <div class="journal-entry">
                <p><strong>Title:</strong> Crime Trends in 2024</p>
                <p><strong>Author:</strong> Alice Martin</p>
                <a href="#" target="_blank">View File</a><br>
                <button class="review-btn approve">Approve</button>
                <button class="review-btn reject">Reject</button>
            </div>
            <div class="journal-entry">
                <p><strong>Title:</strong> AI and Law Enforcement</p>
                <p><strong>Author:</strong> Brian Lee</p>
                <a href="#" target="_blank">View File</a><br>
                <button class="review-btn approve">Approve</button>
                <button class="review-btn reject">Reject</button>
            </div>
        </div>
    `;
    });
    // Reviewed Journals
    document.getElementById('feedbackBtn').addEventListener('click', () => {
        setActiveTab('feedbackBtn');
        contentDiv.innerHTML = `
        <div class="reviewed-journals-box">
            <h3>Reviewed Journals</h3>
            <div class="journal-entry">
                <p><strong>Title:</strong> Cybersecurity Policies</p>
                <p><strong>Author:</strong> Dana Smith</p>
                <a href="#" target="_blank">View File</a>
                <p><strong>Reviewer Comment:</strong> Well-researched and clearly written. Approved.</p>
            </div>
            <div class="journal-entry">
                <p><strong>Title:</strong> Facial Recognition & Privacy</p>
                <p><strong>Author:</strong> Kevin Tran</p>
                <a href="#" target="_blank">View File</a>
                <p><strong>Reviewer Comment:</strong> Needs stronger citations. Rejected for now.</p>
            </div>
        </div>
    `;
    });
})



