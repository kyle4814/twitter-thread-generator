const apiUrl = 'https://twitter-generator-api.up.railway.app/generate_thread';

async function generateThread() {
    if (!validateInputs()) return;

    showLoadingState();

    try {
        const topic = document.getElementById('topic').value.trim();
        const numThreads = parseInt(document.getElementById('numThreads').value) || 1;
        const threadLength = parseInt(document.getElementById('threadLength').value) || 5;
        const randomMode = document.getElementById('randomMode').checked;

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic,
                num_threads: numThreads,
                thread_length: threadLength,
                random_mode: randomMode
            })
        });

        const data = await response.json();
        if (data.status === 'error') {
            showError(data.error || "Unexpected server response.");
            return;
        }

        renderThreads(data.threads);
    } catch (error) {
        showError(`Network Error: ${error.message}`);
    }
}

if (response.status === 403) {
    showError("Upgrade to PRO for more threads");
    return;
}

function validateInputs() {
    const topic = document.getElementById('topic').value.trim();
    if (!topic) {
        showError("Please enter a topic.");
        return false;
    }
    return true;
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

function copyThread(index) {
    const thread = document.querySelectorAll('.thread')[index];
    const insights = Array.from(thread.querySelectorAll('.insight p'))
                         .map(p => p.innerText.replace('✨ ', '')).join('\n\n');
    navigator.clipboard.writeText(insights)
        .then(() => alert('Thread copied to clipboard!'))
        .catch(err => console.error('Copy failed:', err));
}
// For local testing
// const apiUrl = 'http://localhost:5000/generate_thread';
const apiUrl = 'https://twitter-generator-api.up.railway.app/generate_thread';

// Initialize button click handler
document.getElementById('generateBtn').addEventListener('click', generateThread);
