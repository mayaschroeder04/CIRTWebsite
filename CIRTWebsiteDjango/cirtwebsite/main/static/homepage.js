// homepage.js

// Utility to read CSRF token
function getCSRFToken() {
  const m = document.cookie.split('; ').find(r => r.startsWith('csrftoken='));
  return m ? m.split('=')[1] : '';
}

// Modal controls
function openModal(title) {
  const modal = document.getElementById('modal'),
        content = document.getElementById('modal-content');
  if (!modal || !content) return;
  content.innerHTML = `
    <div class="modal-content">
      <h2>Log in to continue reading</h2>
      <p>${title}</p>
      <a href="{% url 'login' %}"><button>Sign Up / Log In</button></a>
      <a href="{% url 'student_dashboard' %}"><button>Continue as Guest</button></a>
      <button onclick="closeModal()">Close</button>
    </div>`;
  modal.style.display = 'block';
}
function closeModal() {
  const m = document.getElementById('modal');
  if (m) m.style.display = 'none';
}

// Filter & Search
function toggleFilter() {
  const dd = document.getElementById('filter-options');
  dd.style.display = dd.style.display === 'block' ? 'none' : 'block';
}
function getSelectedFilter() {
  return Array.from(document.getElementsByName('filter'))
    .find(r => r.checked)?.value || 'All';
}
function performSearch() {
  const q = document.getElementById('search-input').value.trim();
  if (!q) return alert('Please enter a search term.');
  const f = getSelectedFilter();
  window.location.href = `search-results?query=${encodeURIComponent(q)}&filter=${encodeURIComponent(f)}`;
}

// Download
function fetchPresignedUrl(id) {
  fetch(`/generate_presigned_url/${id}/`)
    .then(r => r.json())
    .then(d => d.url ? window.open(d.url, '_blank') : alert('Download link failed.'))
    .catch(() => alert('Error fetching document.'));
}

// Save
function saveUserDocument(id, btn) {
  fetch(`/save-document/${id}/`, {
    method: 'POST',
    headers: {'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json'},
    body: '{}'
  })
  .then(r => r.json())
  .then(d => {
    if (d.success) {
      btn.classList.replace('save-btn', 'unsave-btn');
      btn.textContent = 'Saved';
    }else{
      alert("Create an account to save!")
    }
  });
}
function unsaveUserDocument(id, btn) {
  fetch(`/unsave-document/${id}/`, {
    method: 'POST',
    headers: {'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json'},
    body: '{}'
  })
  .then(r => r.json())
  .then(d => {
    if (d.success) {
      btn.classList.replace('unsave-btn', 'save-btn');
      btn.textContent = 'Save';
    }
  });
}

function downloadDocument(id) {
  fetch(`/download-document/${id}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCSRFToken(),
      'Content-Type': 'application/json'    // <-- fix this
    },
    body: JSON.stringify({})
  })
  .then(res => res.json())                 // this is JSON: { success, url }
  .then(data => {
    if (data.success && data.url) {
      // This will trigger a download (because of your ResponseContentDisposition)
      window.location.href = data.url;
    } else {
      alert('Download failed');
    }
  })
  .catch(err => {
    console.error('Error downloading:', err);
    alert('Download error occurred');
  });
}


function citeDocument(id){
  fetch(`/cite-document/${id}/`, {
    method: 'POST',
    headers: {'X-CSRFToken': getCSRFToken(), 'Content-Type': 'application/json'},
    body: '{}'
  })
  .then(r => r.json())
  .then(d => {
        if (d.success) {
          const citationText = d.citation;

          navigator.clipboard.writeText(citationText)
              .then(() => {
                alert("Citation copied to clipboard");
              })
              .catch(err => {
                console.error("failed to cite, ", err);
                alert("citation failed");
              })

        } else {
          alert("failed fetching document");
        }
      }
    )
      .catch(err => {
        console.error("error w fetch: ", err);
        alert("error");
      });
}

// Render posts
function displayLatestPosts() {
  const docs = JSON.parse(document.getElementById('documents-data').textContent);
  const savedRaw = JSON.parse(document.getElementById('saved-documents').textContent);
  const saved = savedRaw.map(x => Number(x));
  let html = '<ul class="results-list">';
  docs.forEach(doc => {
    const url = encodeURIComponent(doc.file_url),
          isSaved = saved.includes(doc.id),
          btn = isSaved
            ? `<button class="unsave-btn" data-id="${doc.id}">Saved</button>`
            : `<button class="save-btn"   data-id="${doc.id}">Save</button>`;
    html += `
      <li class="search-result-item">
        <div class="result-meta">
          <p class="result-type">RESEARCH REPORT</p>
          <h3 class="result-title" onclick="fetchPresignedUrl('${url}')">${doc.title}</h3>
          <p class="result-author">${doc.author}</p>
          <p class="result-org">${doc.category_name}</p>
          <p>${doc.description}</p>
        </div>
        <div class="result-actions">
          <button class="download-btn" data-id="${doc.id}">Download</button>
          ${btn}
          <button class="cite-btn" data-id="${doc.id}">Cite</button>
        </div>
      </li>`;
  });
  html += '</ul>';
  document.getElementById('latest-posts').innerHTML = html;
}

// Init
document.addEventListener('DOMContentLoaded', () => {
  // Search on Enter
  const input = document.getElementById('search-input');
  if (input) input.addEventListener('keypress', e => { if (e.key==='Enter') performSearch(); });

  document.addEventListener('click', e => {
  const target = e.target;

  if (target.classList.contains('save-btn')) {
    console.log('Save clicked:', target.dataset.id);
    saveUserDocument(target.dataset.id, target);
  }

  if (target.classList.contains('unsave-btn')) {
    console.log('Unsave clicked:', target.dataset.id);
    unsaveUserDocument(target.dataset.id, target);
  }

  if (target.classList.contains('cite-btn')) {
    console.log('Cite clicked:', target.dataset.id);
    citeDocument(target.dataset.id);
  }

  if (target.classList.contains('download-btn')) {
    console.log('Download clicked:', target.dataset.id);
    downloadDocument(target.dataset.id);
  }
});



  displayLatestPosts();
});
