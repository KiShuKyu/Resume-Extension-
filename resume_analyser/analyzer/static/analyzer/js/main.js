console.log("✅ main.js loaded");

document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ DOM fully loaded");

    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const analyzeBtn = document.getElementById("analyze-btn");
    const resultBox = document.getElementById("result");
    const jdInput = document.getElementById("jdInput");
    const themeToggle = document.getElementById("theme-toggle"); // Ensure this ID exists in layout.html

    let selectedFile = null;

    // --- DARK MODE LOGIC ---
    if (themeToggle) {
        const currentTheme = localStorage.getItem("theme") || "light";
        document.documentElement.setAttribute("data-theme", currentTheme);
        themeToggle.textContent = currentTheme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";

        themeToggle.addEventListener("click", () => {
            let theme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
            document.documentElement.setAttribute("data-theme", theme);
            localStorage.setItem("theme", theme);
            themeToggle.textContent = theme === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
        });
    }

    if (!dropZone || !fileInput || !analyzeBtn || !resultBox) {
        console.error("❌ One or more IDs not found! Check your index.html");
        return;
    }

    const createSection = (title, items, cssClass) => {
        if (!items || items.length === 0) return "";
        let html = `<div class="card ${cssClass}"><h3>${title}</h3><ul>`;
        items.forEach(item => { html += `<li>${item}</li>`; });
        html += `</ul></div>`;
        return html;
    };

    
    dropZone.addEventListener("click", (e) => {
        if (e.target !== dropZone) return;
        fileInput.click();
    });


    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("drag-over");
    });
    dropZone.addEventListener("dragleave", () => dropZone.classList.remove("drag-over"));

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("drag-over");
        selectedFile = e.dataTransfer.files[0];
        if (selectedFile) dropZone.textContent = `Selected: ${selectedFile.name}`;
    });

    fileInput.addEventListener("change", () => {
        selectedFile = fileInput.files[0];
        if (selectedFile) dropZone.textContent = `Selected: ${selectedFile.name}`;
    });

    analyzeBtn.addEventListener("click", async () => {
        if (!selectedFile) {
            alert("Please upload a resume first!");
            return;
        }

        const formData = new FormData();
        formData.append("resume", selectedFile);
        
        if (jdInput) {
            formData.append("job_description", jdInput.value);
        }

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Centered Loading UI with Adaptive Color
        resultBox.innerHTML = `
            <div class="text-center mt-4">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-2" style="color: var(--main-text-color) !important; font-weight: bold;">
                    ⌛ <b>Analyzing resume with Gemini AI... please wait.</b>
                </p>
            </div>`;

        try {
            const response = await fetch("/analyze/", {
                method: "POST",
                headers: { "X-CSRFToken": csrfToken },
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `Server error: ${response.status}`);
            }

            const data = await response.json();
            resultBox.innerHTML = "";

            resultBox.innerHTML += `
                <div class="score-card mb-4 text-center">
                    <h2 class="fw-bold" style="color: var(--main-text-color)">Overall Score: ${data.jdMatch.score}/100</h2>
                    <div class="score-bar mx-auto" style="max-width: 500px;">
                        <div id="scoreFill" style="width: ${data.jdMatch.score}%; height: 100%; border-radius: 10px;"></div>
                    </div>
                </div>
            `;

            resultBox.innerHTML += createSection("✅ Key Strengths", data.goodPoints, "good");
            resultBox.innerHTML += createSection("❌ Areas for Improvement", data.badPoints, "bad");
            resultBox.innerHTML += createSection("💡 Actionable Tips", data.improvements, "improve");
            
            if (data.jdMatch.missingSkills && data.jdMatch.missingSkills.length > 0) {
                resultBox.innerHTML += createSection("🎯 Missing Keywords (ATS)", data.jdMatch.missingSkills, "jd");
            }

        } catch (error) {
            console.error("Fetch error:", error);
            const isRateLimit = error.message.includes("429") || error.message.includes("RESOURCE_EXHAUSTED");
            const isOverloaded = error.message.includes("503") || error.message.includes("overloaded");

            resultBox.innerHTML = `
                <div class="text-center mt-4">
                    <div class="fs-1">${isRateLimit || isOverloaded ? '⏳' : '⚠️'}</div>
                    <h3 class="mt-2" style="color: var(--main-text-color);">
                        ${isRateLimit ? 'Rate Limit Reached' : (isOverloaded ? 'AI Server Busy' : 'Analysis Error')}
                    </h3>
                    <p style="color: var(--main-text-color); opacity: 0.8; max-width: 400px; margin: 0 auto;">
                        ${isRateLimit 
                            ? "Google's free AI tier needs a break. Please wait 60 seconds." 
                            : "Something went wrong with the server connection."}
                    </p>
                    <p class="mt-3" style="color: #f44336; font-size: 0.85rem; font-family: monospace;">
                        Details: ${error.message}
                    </p>
                    <button class="btn btn-primary mt-3" onclick="location.reload()">Refresh & Retry</button>
                </div>`;
        }
    });
});