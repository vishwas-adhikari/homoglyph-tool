document.addEventListener('DOMContentLoaded', () => {

    // Helper function to get the Django CSRF token for secure POST requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const CSRF_TOKEN = getCookie('csrftoken');

    // --- Tab Switching Logic ---
    const detectorTab = document.getElementById('tab-detector');
    const generatorTab = document.getElementById('tab-generator');
    const detectorSection = document.getElementById('detector');
    const generatorSection = document.getElementById('generator');

    detectorTab.addEventListener('click', () => {
        detectorTab.classList.add('active');
        generatorTab.classList.remove('active');
        detectorSection.classList.remove('hidden');
        generatorSection.classList.add('hidden');
    });
    generatorTab.addEventListener('click', () => {
        generatorTab.classList.add('active');
        detectorTab.classList.remove('active');
        generatorSection.classList.remove('hidden');
        detectorSection.classList.add('hidden');
    });


    // --- Backend API Call Function ---
    async function postData(url = '', data = {}) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    }

    // --- Detector Logic ---
    const detectorBtn = document.getElementById('detector-btn');
    const detectorInput = document.getElementById('detector-input');
    const detectorResults = document.getElementById('detector-results');

    async function analyzeDomain() {
        const domain = detectorInput.value.trim();
        if (!domain) return;
        detectorResults.innerHTML = `<p>Analyzing...</p>`;
        detectorResults.classList.add('visible');

        try {
            const data = await postData('/api/detect/', { domain });
            let detailsHtml = `
                <div class="result-item">
                    <div class="result-label">Input Domain</div>
                    <div class="result-value">${data.input_domain}</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Normalized (Looks Like)</div>
                    <div class="result-value">${data.normalized_domain}</div>
                </div>
                 <div class="result-item">
                    <div class="result-label">Similarity Score</div>
                    <div class="result-value">${data.similarity_score}</div>
                </div>
            `;

            if (data.is_suspicious) {
                detectorResults.innerHTML = `<div class="result-title warning">⚠️ Suspicious Domain Detected</div>`;
                data.suspicious_chars.forEach(char => {
                    detailsHtml += `
                    <div class="result-item">
                        <div class="result-label">Suspicious Character</div>
                        <div class="result-value">
                            '<span class="suspicious-char">${char.original}</span>' (${char.codepoint}) found, which looks like '<span class="canonical-char">${char.canonical}</span>'
                        </div>
                    </div>`;
                });
            } else {
                detectorResults.innerHTML = `<div class="result-title success">✅ Domain Appears Safe</div>`;
            }
            detectorResults.innerHTML += detailsHtml;
        } catch (error) {
            detectorResults.innerHTML = `<div class="result-title warning">Error connecting to server.</div>`;
            console.error('Error:', error);
        }
    }
    detectorBtn.addEventListener('click', analyzeDomain);
    detectorInput.addEventListener('keypress', e => e.key === 'Enter' && analyzeDomain());


    // --- Generator & Shortener Logic ---
    const generatorBtn = document.getElementById('generator-btn');
    const generatorInput = document.getElementById('generator-input');
    const generatorResults = document.getElementById('generator-results');
    const variantList = document.createElement('div');
    variantList.className = 'domain-list';
    generatorResults.appendChild(variantList);
    
    const shortenerSection = document.getElementById('shortener-section');
    const shortenerBtn = document.getElementById('shortener-btn');
    const shortenInput = document.getElementById('shorten-input');
    const shortenerResults = document.getElementById('shortener-results');

    async function generateVariants() {
        const domain = generatorInput.value.trim();
        if (!domain) return;
        variantList.innerHTML = `<p>Generating...</p>`;
        generatorResults.classList.add('visible');
        shortenerSection.style.display = 'none';
        shortenerBtn.style.display = 'none';
        shortenerResults.classList.remove('visible');

        try {
            const data = await postData('/api/generate/', { domain });
            if (data.generated_domains && data.generated_domains.length > 0) {
                generatorResults.innerHTML = `<div class="result-title">Generated Homoglyph Variants</div>`;
                variantList.innerHTML = data.generated_domains.map(variant => `
                    <div class="domain-item" data-domain="${variant}">
                        <span class="domain-text">${variant}</span>
                        <div>
                            <button class="btn-small action-btn shorten-btn">Shorten</button>
                            <button class="btn-small action-btn copy-btn">Copy</button>
                        </div>
                    </div>
                `).join('');
                generatorResults.appendChild(variantList);
            } else {
                variantList.innerHTML = `<p>No confusable characters found to generate variants.</p>`;
            }
        } catch (error) {
            variantList.innerHTML = `<p style="color: #f59e0b;">Error connecting to server.</p>`;
            console.error('Error:', error);
        }
    }
    generatorBtn.addEventListener('click', generateVariants);
    generatorInput.addEventListener('keypress', e => e.key === 'Enter' && generateVariants());

    async function shortenUrl() {
        const url = shortenInput.value.trim();
        if (!url) return;
        shortenerResults.innerHTML = `<p>Shortening...</p>`;
        shortenerResults.classList.add('visible');
        
        try {
            const data = await postData('/api/shorten/', { url });
            let detailsHtml = `
                <div class="result-item">
                    <div class="result-label">Original URL:</div>
                    <div class="result-value">${data.original_url}</div>
                </div>
                <div class="result-item">
                    <div class="result-label">Shortened URL:</div>
                    <div class="result-value" style="display: flex; justify-content: space-between; align-items: center;">
                        <span>${data.shortened_url}</span>
                        <button class="btn-small action-btn copy-btn" data-domain="${data.shortened_url}">Copy</button>
                    </div>
                </div>
            `;
            shortenerResults.innerHTML = `<div class="result-title success">Shortened URL</div>` + detailsHtml;

        } catch(error) {
            shortenerResults.innerHTML = `<div class="result-title warning">Error shortening URL.</div>`;
            console.error('Error:', error);
        }
    }
    shortenerBtn.addEventListener('click', shortenUrl);
    shortenInput.addEventListener('keypress', e => e.key === 'Enter' && shortenUrl());


    // --- Event Delegation for generated buttons ---
    document.body.addEventListener('click', (e) => {
        const domain = e.target.closest('.domain-item')?.dataset.domain || e.target.dataset.domain;
        if (!domain) return;

        // Handle Copy Button clicks
        if (e.target.classList.contains('copy-btn')) {
            navigator.clipboard.writeText(domain).then(() => {
                e.target.textContent = 'Copied!';
                e.target.classList.add('copied');
                setTimeout(() => {
                    e.target.textContent = 'Copy';
                    e.target.classList.remove('copied');
                }, 2000);
            });
        }

        // Handle Shorten Button clicks
        if (e.target.classList.contains('shorten-btn')) {
            shortenInput.value = domain;
            shortenerSection.style.display = 'block';
            shortenerBtn.style.display = 'block';
            shortenInput.focus();
            shortenerSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    });
});