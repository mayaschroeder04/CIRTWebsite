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

function assignReviewer(journalId) {
    const reviewerSelect = document.getElementById(`reviewer-${journalId}`);
    const reviewerId     = reviewerSelect.value;               // chosen reviewer

    fetch(`/assign-reviewer/${journalId}/${reviewerId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: '{}'
    })
    .then(response => {
        if (!response.ok) throw new Error('Assignment failed');

        // Remove the journal from the page
        document.getElementById(`journal-${journalId}`).remove();

        // Success message
        const container = document.getElementById('dashboard-content');
        const message   = document.createElement('p');
        message.textContent = 'Journal successfully assigned!';
        message.style.color = 'green';
        container.insertBefore(message, container.firstChild);

        // If no journals remain, say so
        if (!container.querySelector('.journal-entry')) {
            container.innerHTML += '<p>No unassigned journals!</p>';
        }
    })
    .catch(error => {
        console.error('Error assigning reviewer:', error);
        alert('Failed to assign reviewer.');
    });
}

document.addEventListener('DOMContentLoaded', function () {
    const contentDiv = document.getElementById('dashboard-content');

    // Profile Info
    document.getElementById('profileBtn').addEventListener('click', () => {
        setActiveTab('profileBtn');
        contentDiv.innerHTML = `
            <div class="profile-box">
                <h3>Your Profile</h3>
                <p><strong>Name:</strong> John Doe</p>
                <p><strong>Email:</strong> johndoe@example.com</p>
                <p><strong>Role:</strong> Student</p>
            </div>
        `;

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
            contentDiv.querySelector('.profile-box').innerHTML = `
                <h3>Your Profile</h3>
                <p><strong>Name:</strong>  ${data.name}</p>
                <p><strong>Email:</strong> ${data.email}</p>
                <p><strong>Role:</strong>  ${data.role}</p>`;
        })
        .catch(err => {
            console.error('Error loading profile:', err);
            contentDiv.innerHTML +=
                '<p style="color:red;">Failed to load profile.</p>';
        });
    });

    // Needs-Review tab
    document.getElementById('needsReviewBtn').addEventListener('click', () => {
        setActiveTab('needsReviewBtn');
        const container = document.getElementById('dashboard-content');
        container.innerHTML = '';

        fetch('/get-reviewers/')
        .then(r => r.json())
        .then(reviewers => {
            fetch('/get-pending-journals/')
            .then(r => r.json())
            .then(data => {
                if (data.length === 0) {
                    container.innerHTML = '<p>No unassigned journals!</p>';
                    return;
                }

                data.forEach(journal => {
                    const div = document.createElement('div');
                    div.className = 'journal-entry';
                    div.id        = `journal-${journal.id}`;

                    div.innerHTML = `
                        <p><strong>Title:</strong> ${journal.title}</p>
                        <p><strong>Author:</strong> ${journal.author}</p>
                        <a href="${journal.fileUrl}" target="_blank">View File</a>
                        <div style="margin-top:10px;">
                          <label for="reviewer-${journal.id}">Assign Reviewer:</label>
                          <select id="reviewer-${journal.id}">
                            ${reviewers.map(r =>
                               `<option value="${r.id}">${r.name}</option>`).join('')}
                          </select>
                          <button onclick="assignReviewer(${journal.id})">Assign</button>
                        </div>`;
                    container.appendChild(div);
                });
            })
            .catch(err => {
                console.error('Failed to load pending journals:', err);
                container.innerHTML =
                    '<p style="color:red;">Error loading journals.</p>';
            });
        })
        .catch(err => {
            console.error('Failed to load reviewers:', err);
            container.innerHTML =
                '<p style="color:red;">Error loading reviewers.</p>';
        });
    });

    // Feedback tab (skeleton)
    document.getElementById('feedbackBtn').addEventListener('click', () => {
        setActiveTab('feedbackBtn');
        document.getElementById('dashboard-content').innerHTML = '';
        fetch('/feedback/');
    });
});
