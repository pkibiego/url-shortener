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
