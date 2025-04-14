// JavaScript File for Homepage Only // 

// Function to handle the click event on Register and Log in buttons
function openModal(title) {
    let modal = document.getElementById("modal");
    let modalContent = document.getElementById("modal-content");

    console.log("Opening modal with title:", title); // Check if this gets logged

    // Ensure modal elements exist before modifying them
    if (modal && modalContent) {
        modal.style.display = "block";
        modalContent.innerHTML = `
                    <div class="modal-content">
                        <h2><strong>Log in to continue reading</strong></h2>
                        <p>${title}</p>
                        <a href="/login/">
                            <button>Sign Up / Log In</button>
                        </a>
                        <a href="/student-dashboard/">
                            <button>Student Dashboard</button>
                        </a>
                        <a href="/">
                            <button>Continue As Guest</button>
                        </a>
                        <button onclick="closeModal()">Close</button>
                    </div>
                `;
    }
}

function closeModal() {
    let modal = document.getElementById("modal");
    if (modal) {
        modal.style.display = "none";
    }
}

// Toggle the filter dropdown
function toggleFilter() {
  const filterDropdown = document.getElementById("filter-options");
  filterDropdown.style.display =
    filterDropdown.style.display === "block" ? "none" : "block";
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
  window.location.href = `search-results?query=${encodeURIComponent(
    query
  )}&filter=${encodeURIComponent(selectedFilter)}`;
}

// Trigger search on 'Enter' keypress
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
        console.log("Enter key pressed - Performing search");
        performSearch();
      }
    });
  } else {
    console.error("ERROR: Search input field not found in DOM");
  }
});

console.log("Display Latest Posts Function is Loaded");

function displayLatestPosts() {
    const rawJson = document.getElementById("documents-data").textContent;
//   const rawDocumentsJson = "{{ documents_json|escapejs }}";

    const documents = JSON.parse(rawJson);
    console.log(documents);

    let resultHTML = "";

    documents.forEach((document) => {
        // Use encodeURIComponent to safely pass data into JavaScript function
        const title = encodeURIComponent(document.title);
        const description = encodeURIComponent(document.description);

        resultHTML += `
                        <div class="featured-post">
                            <h2>${document.title}</h2>
                            <p><strong>Author:</strong> ${document.author}</p>
                            <p><strong>Category:</strong> ${document.category_name}</p>
                            <p>${document.description}</p>
                            <a class="read-more" onclick="window.location.href='${document.file_url}'">Continue Reading</a>
                        </div>
                    `;
    });
    document.getElementById("latest-posts").innerHTML = resultHTML;
}
document.addEventListener("DOMContentLoaded", displayLatestPosts);
console.log("DOM content loaded, calling displayLatestPosts...");
displayLatestPosts();
console.log("Documents JSON:", "{{ documents_json|escapejs }}");


