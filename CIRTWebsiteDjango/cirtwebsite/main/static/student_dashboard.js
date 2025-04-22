function getCSRFToken() {
  const m = document.cookie.split('; ').find(r => r.startsWith('csrftoken='));
  return m ? m.split('=')[1] : '';
}

document.addEventListener('DOMContentLoaded', function () {
    const contentDiv = document.getElementById('dashboard-content');

    // Upload button: full page redirect
    document.getElementById('uploadBtn').addEventListener('click', () => {
        window.location.href = '/upload-journal/';
    });

    // Past Uploads
    document.getElementById('pastUploadsBtn').addEventListener('click', () => {
        contentDiv.innerHTML = `
            <h3>Past Uploads</h3>
            <ul id="uploads-list"></ul>
        `;

        fetch('/past-uploads/', {
            method: 'POST',
            headers: {'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json'},
            body: '{}'
        })
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('uploads-list');
           if (data.length === 0) {
                list.innerHTML = '<li>No uploaded journals.</li>';
            } else {
                data.forEach(doc => {
                  list.innerHTML += `
                    <li class="saved-journal">
                      <strong>${doc.title}</strong>
                      <p>${doc.description || "No description available"}</p>
                      <a href="/view_pdf/${doc.id}" class="read-more">View Journal</a>
                    </li>
                  `;

                });
            }
        })
        .catch(err => {
            contentDiv.innerHTML += `<p style="color:red;">Failed to load past uploads.</p>`;
            console.error(err);
        });
    });

    // Review Status
    document.getElementById('statusBtn').addEventListener('click', () => {
    contentDiv.innerHTML = `
        <h3>Review Status</h3>
        <ul id="status-list"></ul>
    `;

    fetch('/review-status/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json'
        },
        body: '{}'
    })
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById('status-list');
        const documents = data.data || [];

        if (documents.length === 0) {
            list.innerHTML = '<li>No statuses available.</li>';
        } else {
            documents.forEach(doc => {
                list.innerHTML += `
                    <li class="saved-journal">
                        <strong>${doc.title}</strong> 
                        <p>${doc.description || "No description available"}</p>
                        <p>Status: ${doc.status || "No status available"}</p>
                        <a href="/view_pdf/${doc.id}" class="read-more">View Status</a>
                    </li>
                `;
            });
        }
    })
    .catch(err => {
        contentDiv.innerHTML += `<p style="color:red;">Failed to load status list.</p>`;
        console.error(err);
    });
});


    // Saved Journals
    document.getElementById('savedBtn').addEventListener('click', () => {
        contentDiv.innerHTML = `
            <h3>Saved Journals</h3>
            <ul id="saved-list"></ul>
        `;

        fetch('/saved-journals/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            },
            body: '{}'
        })
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('saved-list');

            if (data.length === 0) {
                list.innerHTML = '<li>No saved journals.</li>';
            } else {
                data.forEach(doc => {
                  list.innerHTML += `
                    <li class="saved-journal">
                      <strong>${doc.title}</strong>
                      <p>${doc.description || "No description available"}</p>
                      <a href="/view_pdf/${doc.id}" class="read-more">View Journal</a>
                    </li>
                  `;

                });
            }
        })
        .catch(err => {
            console.error('Error loading saved journals:', err);
            contentDiv.innerHTML += '<p style="color: red;">Failed to load saved journals.</p>';
        });
    });

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
