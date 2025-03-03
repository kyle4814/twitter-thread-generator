// script.js
const FREE_SOURCES = ['gnews', 'innews'];
const PRO_SOURCES = ['bingnews', 'nytimes', 'guardian'];

function renderSourceSelector() {
    const container = document.getElementById('sourceSelector');
    container.innerHTML = Object.keys(NEWS_SOURCES).map(source => `
        <label class="source-chip ${FREE_SOURCES.includes(source) ? 'free' : 'pro-locked'}">
            <input type="checkbox" name="source" value="${source}" 
                   ${FREE_SOURCES.includes(source) ? '' : 'disabled'}>
            ${source.toUpperCase()}
            ${FREE_SOURCES.includes(source) ? '' : '<span class="pro-badge">PRO</span>'}
        </label>
    `).join('');
}

function showProBenefits() {
    const modal = document.createElement('div');
    modal.className = 'pro-benefits-modal';
    modal.innerHTML = `
        <h3>🔓 PRO Features Unlock:</h3>
        <ul>
            <li>10x More Sources (${PRO_SOURCES.join(', ')})</li>
            <li>AI-Powered Insights</li>
            <li>Unlimited Generations</li>
        </ul>
        <button onclick="showPricing()">Upgrade Now</button>
    `;
    document.body.appendChild(modal);
}
