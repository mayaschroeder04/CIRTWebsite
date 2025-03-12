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

// =============================
// 🔽 ADD THE NEW FILTER FUNCTIONS BELOW 🔽
// =============================

// Toggle the filter dropdown
function toggleFilter() {
    const filterDropdown = document.getElementById("filter-options");
    filterDropdown.style.display = filterDropdown.style.display === "block" ? "none" : "block";
}

// Get the selected filter category
function getSelectedFilter() {
    const filters = document.getElementsByName("filter");
    for (const filter of filters) {
        if (filter.checked) {
            return filter.value;
        }
    }
    return "All"; // Ensures default filter is always applied
}

// Perform the search with filter integration
function performSearch() {
    const query = document.getElementById("search-input").value.trim();
    const selectedFilter = getSelectedFilter();

    if (!query) {
        alert("Please enter a search term.");
        return;
    }

    console.log(`Searching for '${query}' in category: '${selectedFilter}'`);
    window.location.href = `search-results.html?query=${encodeURIComponent(query)}&filter=${encodeURIComponent(selectedFilter)}`;
}

// Trigger search on 'Enter' keypress
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("search-input");
    if (searchInput) {
        searchInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                console.log("Enter key pressed - Performing search");
                performSearch();
            }
        });
    } else {
        console.error("❌ ERROR: Search input field not found in DOM");
    }
});