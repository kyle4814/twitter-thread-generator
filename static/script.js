async function generateThread() {
    const topicInput = document.getElementById('topic').value.trim();
    const numThreads = parseInt(document.getElementById('numThreads').value) || 1;
    const threadLength = parseInt(document.getElementById('threadLength').value) || 5;
    const randomMode = document.getElementById('randomMode').checked;

    document.getElementById('threadContainer').innerHTML = `
        <div class="thread">
            <p>🚀 Generating insights...</p>
        </div>
    `;

    try {
        const response = await fetch('https://web-production-d52f.up.railway.app/generate_thread', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: topicInput,
                num_threads: numThreads,
                thread_length: threadLength,
                random_mode: randomMode
            }),
        });

        const data = await response.json();

        if (data.status === 'error' || !data.threads) {
            document.getElementById('threadContainer').innerHTML = `
                <div class="thread">
                    <p>⚠️ Error: ${data.error || "Unexpected server response."}</p>
                </div>
            `;
            return;
        }

        let threadsHTML = '';
        data.threads.forEach((thread, index) => {
            let insightsHTML = thread.map(insight => `
                <div class="insight">
                    <p>✨ ${insight}</p>
                </div>
            `).join('');

            threadsHTML += `
                <div class="thread">
                    <h3>🔥 Thread ${index + 1}</h3>
                    ${insightsHTML}
                </div>
            `;
        });

        document.getElementById('threadContainer').innerHTML = threadsHTML;

    } catch (error) {
        document.getElementById('threadContainer').innerHTML = `
            <div class="thread">
                <p>⚠️ Network Error: ${error.message}</p>
            </div>
        `;
    }
}
