const API_URL = 'http://localhost:5000/generate_thread';
let usageCount = localStorage.getItem('usageCount') || 5;

async function generateThread() {
    if (usageCount <= 0) return showProModal();
    
    const topic = document.getElementById('topic').value.trim();
    const numThreads = parseInt(document.getElementById('numThreads').value);
    const threadLength = parseInt(document.getElementById('threadLength').value);
    const randomMode = document.getElementById('randomMode').checked;

    if (!topic) {
        showError("Please enter a topic.");
        return;
    }

    showLoadingState();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-User-Tier': 'free'  // Default to free tier
            },
            body: JSON.stringify({
                topic,
                num_threads: numThreads,
                thread_length: threadLength,
                random_mode: randomMode
            })
        });

        if (response.status === 403) {
            showProModal();
            return;
        }

        const data = await response.json();
        if (data.status === 'error') {
            showError(data.error || "Unexpected server response.");
            return;
        }

        usageCount--;
        localStorage.setItem('usageCount', usageCount);
        updateUsageDisplay();
        renderThreads(data.threads);
    } catch (error) {
        showError(`Network Error: ${error.message}`);
    }
}

function showLoadingState() {
    document.getElementById('threadContainer').innerHTML = `
        <div class="loading-state">
            <div class="loader"></div>
            <p>Generating your thread...</p>
        </div>
    `;
}

function showError(message) {
    document.getElementById('threadContainer').innerHTML = `
        <div class="error-state">
            <p>⚠️ ${message}</p>
            <button onclick="generateThread()">Retry</button>
        </div>
    `;
}

function renderThreads(threads) {
    let threadsHTML = '';
    threads.forEach((thread, index) => {
        let insightsHTML = thread.insights.map(insight => `
            <div class="insight">
                <p>✨ ${insight}</p>
            </div>
        `).join('');
        threadsHTML += `
            <div class="thread">
                <h3>🔥 Thread ${index + 1}: ${thread.topic}</h3>
                ${insightsHTML}
                <div class="actions">
                    <button onclick="copyThread(${index})">Copy Thread</button>
                </div>
            </div>
        `;
    });
    document.getElementById('threadContainer').innerHTML = threadsHTML;
}

function updateUsageDisplay() {
    document.getElementById('usageCount').textContent = 
        `${usageCount}/10 free uses remaining`;
    document.querySelector('.progress-bar').style.width = 
        `${(1 - usageCount/10) * 100}%`;
}

function showProModal() {
    document.body.insertAdjacentHTML('beforeend', `
        <div class="pro-modal">
            <h2>🚀 Unlock PRO Superpowers</h2>
            <p>Get access to Twitter trends, news sources, and unlimited generations!</p>
            <button class="pro-btn" onclick="redirectToCheckout()">
                Upgrade Now - $9.99/month
            </button>
            <p class="small-text">7-day money back guarantee</p>
        </div>
    `);
}

function redirectToCheckout() {
    // Implement Stripe integration
    window.location.href = `/checkout?user=${localStorage.getItem('userId')}`;
}

// Initialize
document.getElementById('generateBtn').addEventListener('click', generateThread);
