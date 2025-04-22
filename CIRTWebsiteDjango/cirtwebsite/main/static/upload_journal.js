document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('uploadForm');
    if (!form) return;  // extra safe

    form.addEventListener('submit', async function(event) {
        event.preventDefault();

        const submitButton = form.querySelector('button[type="submit"]');
        const statusMessage = document.getElementById('statusMessage');

        submitButton.disabled = true;
        submitButton.textContent = 'Submitting...';

        const formData = new FormData(form);
        const csrfToken = getCookie('csrftoken');

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Accept': 'application/json',
                }
            });

            const data = await response.json();
            console.log(data)

            if (data.status === 'success') {
                statusMessage.innerHTML = `<div class="success-message"><h2>${data.message}</h2></div>`;
                form.reset();
            } else {
                statusMessage.innerHTML = `<div class="error-message"><h2>Upload Failed</h2><p>${data.message}</p></div>`;
            }

        } catch (error) {
            console.error("Error during upload:", error);
            statusMessage.innerHTML = `<div class="error-message"><h2>Error occurred during upload</h2><p>${error.message}</p></div>`;
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'Upload';
        }
    });

    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                return cookie.substring(name.length + 1);
            }
        }
        return null;
    }
});
