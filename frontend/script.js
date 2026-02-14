document.getElementById("scheme-form").addEventListener("submit", async function(e) {
    e.preventDefault();

    const data = {
        age: parseInt(document.getElementById("age").value),
        income: parseInt(document.getElementById("income").value),
        state: document.getElementById("state").value,
        occupation: document.getElementById("occupation").value
    };

    const response = await fetch("http://127.0.0.1:8000/check-schemes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    displayResults(result);
});

function displayResults(data) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (data.eligible_schemes.length === 0) {
        resultsDiv.innerHTML = "<p>No schemes found.</p>";
        return;
    }

    data.eligible_schemes.forEach(scheme => {
        const card = document.createElement("div");
        card.className = "scheme-card";

        card.innerHTML = `
            <h3>${scheme.name}</h3>
            <p><strong>Benefit:</strong> ${scheme.benefit}</p>
            <p>${scheme.simple_explanation}</p>
            <p><strong>Why you qualify:</strong> ${scheme.why_you_qualify}</p>
            <hr/>
        `;

        resultsDiv.appendChild(card);
    });

    if (data.comparison_summary) {
        const summary = document.createElement("div");
        summary.innerHTML = `<h3>Best Match Summary</h3><p>${data.comparison_summary}</p>`;
        resultsDiv.appendChild(summary);
    }
}