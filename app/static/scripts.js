document.getElementById("url-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    let originalUrl = document.getElementById("original_url").value.trim();

    // Check if the URL doesn't start with 'http://' or 'https://', and prepend 'https://'
    if (!originalUrl.match(/^https?:\/\//)) {
        originalUrl = "https://" + originalUrl;
    }

    const response = await fetch("/api/shorten/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ original_url: originalUrl }),
    });

    if (response.ok) {
        const data = await response.json();
        
        // Display the original URL
        document.getElementById("original_url_display").textContent = data.original_url;
        
        // Construct the full shortened URL without '/api'
        const baseUrl = `${window.location.protocol}//${window.location.host}`;  // This gets https://yourdomain.com
        const fullShortUrl = `${baseUrl}/${data.short_url}`;  // Omit the '/api' part

        // Update the short URL display
        const shortUrl = document.getElementById("short_url_display");
        shortUrl.textContent = fullShortUrl;  // Set the displayed text to the full URL
        shortUrl.href = fullShortUrl;  // Set the actual link to the full URL

        // Show the result section
        document.getElementById("result").style.display = "block";
    } else {
        alert("Error shortening URL");
    }
});

// Dynamically update the year in the footer
document.getElementById("year").textContent = new Date().getFullYear();

// Pagination on landing.html
let currentPage = 1;
const linksPerPage = 5;
const searchBar = document.getElementById("search-bar");
const tableBody = document.getElementById("links-table").querySelector("tbody");

searchBar.addEventListener("input", filterLinks);
document.getElementById("prev-page").addEventListener("click", () => changePage(-1));
document.getElementById("next-page").addEventListener("click", () => changePage(1));

function filterLinks() {
    const searchTerm = searchBar.value.toLowerCase();
    const rows = Array.from(tableBody.querySelectorAll("tr"));

    rows.forEach(row => {
        const originalUrl = row.children[0].textContent.toLowerCase();
        const shortUrl = row.children[1].textContent.toLowerCase();
        const isVisible = originalUrl.includes(searchTerm) || shortUrl.includes(searchTerm);
        row.style.display = isVisible ? "" : "none";
    });
}

function changePage(delta) {
    currentPage += delta;
    updateTable();
}

function updateTable() {
    const rows = Array.from(tableBody.querySelectorAll("tr"));
    rows.forEach((row, index) => {
        row.style.display = (index >= (currentPage - 1) * linksPerPage && index < currentPage * linksPerPage) ? "" : "none";
    });

    document.getElementById("page-number").textContent = currentPage;
    document.getElementById("prev-page").disabled = currentPage === 1;
    document.getElementById("next-page").disabled = (currentPage * linksPerPage >= rows.length);
}

// Initial table update
updateTable();
