
function getCSRFToken() {
  const m = document.cookie.split('; ')
              .find(r => r.startsWith('csrftoken='));
  return m ? m.split('=')[1] : '';
}
function setActiveTab(id) {
  document.querySelectorAll('.dashboard-navbar span')
          .forEach(s => s.classList.remove('active-tab'));
  document.getElementById(id).classList.add('active-tab');
}

function sendDecision(journalId, status, comment) {
  /* calls:  /past-reviews/<journalId>/<status>/  */
  return fetch(`/past-reviews/${journalId}/${status}/${comment}/`, {
    method: 'POST',
    credentials: 'same-origin',
    headers: {
      'X-CSRFToken': getCSRFToken(),
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ comment })
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const contentDiv = document.getElementById('dashboard-content');
  document.getElementById('profileBtn').addEventListener('click', () => {
    setActiveTab('profileBtn');
    contentDiv.innerHTML =
      '<div class="profile-box"><h3>Your Profile</h3></div>';

    fetch('/user-profile/', {
      method: 'POST',
      credentials: 'same-origin',
      headers: { 'X-CSRFToken': getCSRFToken(),
                 'Content-Type': 'application/json' },
      body: '{}'
    })
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(d => {
      contentDiv.querySelector('.profile-box').innerHTML = `
        <h3>Your Profile</h3>
        <p><strong>Name:</strong>  ${d.name}</p>
        <p><strong>Email:</strong> ${d.email}</p>
        <p><strong>Role:</strong>  ${d.role}</p>`;
    })
    .catch(() =>
      contentDiv.innerHTML +=
        '<p style="color:red;">Failed to load profile.</p>');
  });

  document.getElementById('pendingBtn').addEventListener('click', () => {
    setActiveTab('pendingBtn');
    contentDiv.innerHTML = '<p>Loading…</p>';

    fetch('/assigned-journals/', { credentials: 'same-origin' })
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(data => {
      const pending = data.filter(j =>
                     j.status === 'pending' || j.status === 'reviewing');
      let html = `
        <div class="pending-journals-box">
          <h3>Pending Journals for Review</h3>`;
      if (!pending.length) {
        contentDiv.innerHTML = html +
          '<p>No pending journals right now.</p></div>';
        return;
      }

      pending.forEach((j, i) => {
        html += `
          <div class="journal-entry" id="journal-${j.id}">
            <p><strong>Title:</strong> ${j.title}</p>
            <p><strong>Author:</strong> ${j.author}</p>
            <a href="${j.file_url}" target="_blank">View File</a><br>
            <label for="c${i}"><strong>Reviewer Comment:</strong></label><br>
            <textarea id="c${i}" class="review-comment"
                      placeholder="Write your comment here…"></textarea><br>
            <button class="review-btn approve">Approve</button>
            <button class="review-btn reject">Reject</button>
          </div>`;
      });
      html += '</div>';
      contentDiv.innerHTML = html;

      /* wire buttons */
      contentDiv.querySelectorAll('.journal-entry').forEach(entry => {
        const jid = entry.id.split('-')[1];
        const comment = entry.querySelector('.review-comment');

        entry.querySelector('.approve')
             .addEventListener('click', () =>
               sendDecision(jid,'approved',comment.value)
               .then(r => { if (r.ok) entry.remove(); }));

        entry.querySelector('.reject')
             .addEventListener('click', () =>
               sendDecision(jid,'rejected',comment.value)
               .then(r => { if (r.ok) entry.remove(); }));
      });
    })
    .catch(() =>
      contentDiv.innerHTML =
        '<p style="color:red;">Failed to load pending journals.</p>');
  });

  document.getElementById('feedbackBtn').addEventListener('click', () => {
    setActiveTab('feedbackBtn');
    contentDiv.innerHTML = '<p>Loading…</p>';

    fetch('/assigned-journals/', { credentials: 'same-origin' })
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(data => {
      const reviewed = data.filter(j =>
                       j.status === 'approved' || j.status === 'rejected');
      let html = `
        <div class="reviewed-journals-box">
          <h3>Reviewed Journals</h3>`;
      if (!reviewed.length) {
        contentDiv.innerHTML = html +
          '<p>You have not reviewed any journals yet.</p></div>';
        return;
      }

      reviewed.forEach(j => {
        html += `
          <div class="journal-entry">
            <p><strong>Title:</strong> ${j.title}</p>
            <p><strong>Author:</strong> ${j.author}</p>
            <a href="${j.file_url}" target="_blank">View File</a>
            <p><strong>Status:</strong> ${j.status}</p>
          </div>`;
      });
      contentDiv.innerHTML = html + '</div>';
    })
    .catch(() =>
      contentDiv.innerHTML =
        '<p style="color:red;">Failed to load reviewed journals.</p>');
  });
});
