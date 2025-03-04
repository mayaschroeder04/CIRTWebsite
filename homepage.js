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

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector(".input");

    if (searchInput) {
        searchInput.addEventListener("keypress", function (event) {
            if (event.key === "Enter") {
                const query = searchInput.value.trim();
                if (query) {
                    // Instead of opening in a new tab, it will navigate in the same tab
                    window.location.href = `search-results.html?query=${encodeURIComponent(query)}`;
                }
            }
        });
    }

    // Load search results dynamically on search-results.html
    const resultsContainer = document.getElementById("search-results-container");

    if (resultsContainer) {
        const urlParams = new URLSearchParams(window.location.search);
        const query = urlParams.get("query");

        if (query) {
            resultsContainer.innerHTML = `<h3>Results for: "${query}"</h3>`;

            // Example: Fetching data from different sections
            const allData = [
                { title: "AI in Criminal Justice", author: "John Doe", category: "Journals" },
                { title: "Crime Pattern Studies", author: "Jack Brown", category: "Journals" },
                { title: "Random Title 3", author:"Andy Miller", category: "Journals" },
                { title: "Random Forensic Image", category: "Images" }
            ];

            // Filter based on the search term
            const filteredResults = allData.filter(item =>
                item.title.toLowerCase().includes(query.toLowerCase()) ||
                (item.author && item.author.toLowerCase().includes(query.toLowerCase()))
            );

            if (filteredResults.length > 0) {
                filteredResults.forEach(item => {
                    const resultElement = document.createElement("div");
                    resultElement.classList.add("featured-post");
                    resultElement.innerHTML = `
                        <h2>${item.title}</h2>
                        <p class="author">${item.author ? item.author : "Unknown"}</p>
                        <p>Category: ${item.category}</p>
                    `;
                    resultsContainer.appendChild(resultElement);
                });
            } else {
                resultsContainer.innerHTML += `<p>No results found.</p>`;
            }
        } else {
            resultsContainer.innerHTML = "<p>No search query provided.</p>";
        }
    }
});