document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const selectedFilter = getSelectedFilter();
    searchInput.addEventListener("input", function () {
        const query = this.value.trim();
        if (!query) {
            closeAllLists();
            return;
        }
        fetch(`/autocomplete/?query=${encodeURIComponent(query)}&filter=${encodeURIComponent(selectedFilter)}`)
            .then(response => response.json())
            .then(data => {
                showSuggestions(this, data);
            })
            .catch(err => {
                console.error("Autocomplete fetch error:", err);
            });
    });
});

function showSuggestions(inputElement, suggestions) {
    if (inputElement) {
        closeAllLists();

        const bgSection = document.querySelector(".background-section");

        // Check if suggestion container exists
        let container = document.getElementById("autocomplete_wrapper");
        if (!container) {
            container = document.createElement("div");
            container.id = "autocomplete_wrapper";
            container.className = "autocomplete_wrapper"; // Keep this class on the new div only
            bgSection.appendChild(container);
        } else {
            container.innerHTML = ""; // Clear previous suggestions
        }

        positionAutocompleteWrapper()
        container.style.display = "block"; // Show the box (overrides display: none)

        suggestions.forEach(title => {
            const item = document.createElement("div");
            const index = title.toLowerCase().indexOf(inputElement.value.toLowerCase());

            if (index !== -1) {
                const before = title.substring(0, index);
                const match = title.substring(index, index + inputElement.value.length);
                const after = title.substring(index + inputElement.value.length);

                item.innerHTML = `${before}<strong>${match}</strong>${after}`;
            } else {
                item.innerHTML = title;
            }
            item.addEventListener("click", function () {
                inputElement.value = title;
                closeAllLists();
            });
            container.appendChild(item);
        });
    } else {
        const container = document.getElementById("autocomplete_wrapper");
        if (container) container.style.display = "none"; // Hide if no input
    }
}

function closeAllLists(elmnt) {
    const items = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < items.length; i++) {
        if (elmnt !== items[i] && elmnt !== document.getElementById("autocomplete_wrapper")) {
            items[i].parentNode.removeChild(items[i]);
        }
    }
}

function positionAutocompleteWrapper() {
    const input = document.getElementById("search-input");
    const wrapper = document.getElementById("autocomplete_wrapper");

    if (!input || !wrapper) return;

    const rect = input.getBoundingClientRect();
    wrapper.style.position = "absolute";
    wrapper.style.top = `${rect.bottom + window.scrollY}px`;
    wrapper.style.left = `${rect.left + window.scrollX}px`;
}
