let usageCount = localStorage.getItem('usageCount') || 5;

async function generate() {
    if (usageCount <= 0) return showProModal();
    
    const topic = document.getElementById('topic').value;
    const platform = document.getElementById('platform').value;
    
    const response = await fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ topic, platform })
    });
    
    usageCount--;
    localStorage.setItem('usageCount', usageCount);
    updateUsageDisplay();
    
    renderResults(await response.json());
}

function setTopic(topic) {
    document.getElementById('topic').value = topic;
}

function updateUsageDisplay() {
    document.getElementById('usageCount').textContent = 
        `${usageCount}/10 free uses remaining`;
    document.querySelector('.progress-bar').style.width = 
        `${(1 - usageCount/10) * 100}%`;
}

function renderResults(threads) {
    document.getElementById('results').innerHTML = threads
        .map(thread => `
            <div class="thread">
                <p>${thread.content}</p>
                <div class="hashtags">${thread.hashtags}</div>
                <div class="actions">
                    <button onclick="copyToClipboard(this)">📋 Copy</button>
                </div>
            </div>
        `).join('');
}

function showProModal() {
    // Implement Stripe checkout integration
    alert('Upgrade to PRO for unlimited generations!');
}
