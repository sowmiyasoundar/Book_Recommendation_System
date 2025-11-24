document.getElementById("search-btn").addEventListener("click", async () => {
    const query = document.getElementById("search-input").value.trim();
    const resultsDiv = document.getElementById("results");

    if (!query) {
        resultsDiv.innerHTML = "<p>Please enter a book name.</p>";
        return;
    }

    resultsDiv.innerHTML = "<p>Loading...</p>";

    try {
        const response = await fetch(`http://127.0.0.1:5000/recommend?book=${encodeURIComponent(query)}`);
        
        if (!response.ok) throw new Error("Backend error");

        const data = await response.json();

        if (!data.recommendations || data.recommendations.length === 0) {
            resultsDiv.innerHTML = "<p>No recommendations found.</p>";
            return;
        }

        resultsDiv.innerHTML = "";

        data.recommendations.forEach(book => {
            // Create star rating visually (out of 5 stars)
            const stars = Math.round(book.rating / 2);
            let starHTML = "";
            for (let i = 0; i < 5; i++) {
                starHTML += i < stars ? "★" : "☆";
            }

            resultsDiv.innerHTML += `
                <div class="book-card" onclick="window.open('${book.link}', '_blank')">
                    <img src="${book.image}" alt="${book.title}" class="book-image"/>
                    <h3>${book.title}</h3>
                    <p class="star-rating">${starHTML} (${book.rating}/10)</p>
                </div>
            `;
        });

    } catch (error) {
        resultsDiv.innerHTML = "<p style='color:red;'>Error contacting backend</p>";
        console.error(error);
    }
});
