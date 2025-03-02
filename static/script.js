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
        // Use the Railway API endpoint
        const apiUrl = 'https://twitter-generator-api.up.railway.app/generate_thread';

        console.log('Sending request to:', apiUrl);
        console.log('Request data:', {
            topic: topicInput,
            num_threads: numThreads,
            thread_length: threadLength,
            random_mode: randomMode
        });

        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: topicInput,
                num_threads: numThreads,
                thread_length: threadLength,
                random_mode: randomMode
            }),
            // Important: Do not include credentials for cross-origin requests with '*'
            mode: 'cors'
        });

        console.log('Response status:', response.status);
        const data = await response.json();
        console.log('Response data:', data);

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
            let insightsHTML = '';
            thread.insights.forEach(insight => {
                insightsHTML += `
                    <div class="insight">
                        <p>✨ ${insight}</p>
                    </div>
                `;
            });
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
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('threadContainer').innerHTML = `
            <div class="thread">
                <p>⚠️ Network Error: ${error.message}</p>
                <p>Please check your connection and try again.</p>
                <p>Details: ${error.toString()}</p>
            </div>
        `;
    }
}

// Function to copy thread content to clipboard
function copyThread(threadIndex) {
    const threadElement = document.querySelectorAll('.thread')[threadIndex];
    const insights = threadElement.querySelectorAll('.insight p');
    
    let threadText = '';
    insights.forEach((insight, i) => {
        // Remove the ✨ emoji from the text
        const text = insight.textContent.replace('✨ ', '');
        threadText += `${i+1}/ ${text}\n\n`;
    });
    
    // Add final tweet
    threadText += `${insights.length+1}/ Thanks for reading! If you found this thread valuable, please:\n• Like\n• Retweet\n• Follow for more content like this\n\n`;
    
    navigator.clipboard.writeText(threadText)
        .then(() => {
            alert('Thread copied to clipboard!');
        })
        .catch(err => {
            console.error('Error copying text: ', err);
            alert('Failed to copy. Please try again.');
        });
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Check if there are any saved preferences
    const savedTopic = localStorage.getItem('preferredTopic');
    if (savedTopic) {
        document.getElementById('topic').value = savedTopic;
    }
    
    // Add event listeners for saving preferences
    document.getElementById('topic').addEventListener('change', function() {
        localStorage.setItem('preferredTopic', this.value);
    });
});
