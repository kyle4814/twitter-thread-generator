// Fixed API endpoint URL
const apiUrl = 'https://twitter-generator-api.up.railway.app/generate_thread';

// Add premium loading animation
function showLoadingState() {
    document.getElementById('threadContainer').innerHTML = `
        <div class="premium-loader">
            <div class="loader-spinner"></div>
            <p>✨ Crafting viral content...</p>
        </div>
    `;
}

// Add error handling with retry
function showError(error) {
    document.getElementById('threadContainer').innerHTML = `
        <div class="premium-error">
            <p>⚠️ ${error}</p>
            <button class="retry-btn" onclick="generateThread()">Retry</button>
        </div>
    `;
}
