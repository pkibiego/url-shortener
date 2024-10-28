document.getElementById("create-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const originalUrl = document.getElementById("original-url").value;
    const response = await fetch("http://127.0.0.1:8000/urls/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ original_url: originalUrl }),
    });

    if (response.ok) {
        M.toast({html: 'URL shortened successfully!'});
        loadUrls();
    } else {
        M.toast({html: 'Error shortening URL', classes: 'red'});
    }
});

async function loadUrls() {
    const response = await fetch("http://127.0.0.1:8000/api/urls/");
    if (response.ok) {
        const urls = await response.json();
        const urlList = document.getElementById("url-list");
        urlList.innerHTML = urls.map(url => `
            <li class="collection-item">
                <a href="${url.original_url}" target="_blank">${url.short_url}</a>
                <button onclick="editUrl('${url.short_url}')" class="btn-small secondary-content">Edit</button>
            </li>
        `).join("");
    }
}

loadUrls();
