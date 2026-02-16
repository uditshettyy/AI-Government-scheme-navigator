document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("scheme-form");
    const resultsDiv = document.getElementById("results");
    const stateDropdown = document.getElementById("state");
    const occupationDropdown = document.getElementById("occupation");

    /* ---------------- SUBMIT HANDLER ---------------- */

    form.addEventListener("submit", async function (e) {
        e.preventDefault();

        resultsDiv.innerHTML = "<p>Checking eligibility...</p>";

        const data = {
            age: parseInt(document.getElementById("age").value),
            income: parseInt(document.getElementById("income").value),
            state: stateDropdown.value,
            occupation: occupationDropdown.value
        };

        try {
            const response = await fetch("http://127.0.0.1:8000/check-schemes", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error("Failed to fetch schemes");
            }

            const result = await response.json();
            displayResults(result);

        } catch (error) {
            resultsDiv.innerHTML =
                "<p style='color:red;'>Server connection error. Make sure backend is running.</p>";
            console.error(error);
        }
    });

    /* ---------------- LOAD STATES ---------------- */

    async function loadStates() {
        try {
            const response = await fetch("http://127.0.0.1:8000/states");
            const data = await response.json();

            stateDropdown.innerHTML = '<option value="">Select State</option>';

            data.states.forEach(state => {
                if (state.toLowerCase() !== "all") {
                    const option = document.createElement("option");
                    option.value = state;
                    option.textContent = state;
                    stateDropdown.appendChild(option);
                }
            });

        } catch (error) {
            console.error("Failed to load states:", error);
        }
    }

    /* ---------------- LOAD OCCUPATIONS ---------------- */

    async function loadOccupations() {
        try {
            const response = await fetch("http://127.0.0.1:8000/occupations");
            const data = await response.json();

            occupationDropdown.innerHTML = '<option value="">Select Occupation</option>';

            data.occupations.forEach(occupation => {
                const option = document.createElement("option");
                option.value = occupation;
                option.textContent = occupation;
                occupationDropdown.appendChild(option);
            });

        } catch (error) {
            console.error("Failed to load occupations:", error);
        }
    }

    /* ---------------- DISPLAY RESULTS ---------------- */

    function displayResults(data) {
        resultsDiv.innerHTML = "";

        if (!data.eligible_schemes || data.eligible_schemes.length === 0) {
            resultsDiv.innerHTML = "<p>No schemes found.</p>";
            return;
        }

        data.eligible_schemes.forEach((scheme, index) => {

            const card = document.createElement("div");
            card.className = "scheme-card";

            const recommendedBadge =
                scheme.recommended ? `<span class="badge">Recommended</span>` : "";

            const documentsList = scheme.required_documents
                ? scheme.required_documents.map(doc => `<li>${doc}</li>`).join("")
                : "";

            card.innerHTML = `
                <div class="card-header">
                    <h3>${scheme.name}</h3>
                    ${recommendedBadge}
                </div>

                <p><strong>Benefit:</strong> ${scheme.benefit}</p>
                <p>${scheme.simple_explanation || ""}</p>
                <p><strong>Why you qualify:</strong> ${scheme.why_you_qualify || ""}</p>

                ${scheme.score ? `<p><strong>Score:</strong> ${scheme.score}</p>` : ""}

                ${documentsList ? `
                    <div class="docs">
                        <strong>Required Documents:</strong>
                        <ul>${documentsList}</ul>
                    </div>
                ` : ""}

                ${scheme.application_url ? `
                    <a href="${scheme.application_url}" target="_blank" class="apply-btn">
                        Apply Now
                    </a>
                ` : ""}
            `;

            resultsDiv.appendChild(card);
        });

        if (data.comparison_summary) {
            const summary = document.createElement("div");
            summary.className = "summary-card";
            summary.innerHTML = `
                <h3>Best Match Summary</h3>
                <p>${data.comparison_summary}</p>
            `;
            resultsDiv.appendChild(summary);
        }
    }

    loadStates();
    loadOccupations();
});