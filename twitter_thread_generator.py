from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import random
import os

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": ["https://kyle4814.github.io", "*"]}}, supports_credentials=True)

# Significantly expanded topic database with diverse subjects
TOPIC_DATABASE = {
    "AI": [
        "AI-powered automation saves businesses millions annually.",
        "Neural networks can now predict consumer behavior with 87% accuracy.",
        "GPT-4 has revolutionized content creation for businesses worldwide.",
        "The ethical implications of AI decision-making in healthcare settings.",
        "AI-driven personalization increases conversion rates by 35% on average.",
        "Reinforcement learning models are transforming robotics manufacturing.",
        "AI chatbots now resolve 78% of customer inquiries without human intervention.",
        "The computational limitations holding back artificial general intelligence."
    ],
    "Digital Marketing": [
        "SEO is still the #1 driver of free organic traffic for 76% of businesses.",
        "Email marketing generates $42 for every $1 spent on average.",
        "YouTube automation channels can generate 5-figure monthly incomes.",
        "TikTok ads are delivering 30% higher CTR compared to Facebook ads.",
        "Content repurposing strategies can triple your content output efficiency.",
        "Voice search optimization is becoming essential for local businesses.",
        "First-party data collection strategies that comply with privacy regulations.",
        "Omnichannel marketing increases customer retention by 90%."
    ],
    "Sports": [
        "Michael Jordan's mindset: How psychological preparation creates champions.",
        "Recovery science is revolutionizing athletic performance standards.",
        "Why periodized training programs outperform traditional training methods.",
        "The role of nutrition timing in optimizing athletic performance.",
        "How sports analytics is changing game strategies across major leagues.",
        "The physiological impact of altitude training for endurance athletes.",
        "Mental visualization techniques used by Olympic gold medalists.",
        "The science behind injury prevention in high-impact sports."
    ],
    "History": [
        "The economic factors that contributed to the fall of the Roman Empire.",
        "Archaeological evidence suggests ancient Egyptians used electricity.",
        "How the Silk Road shaped modern global trade relationships.",
        "The forgotten women mathematicians who changed scientific history.",
        "How the Black Death transformed European social structures.",
        "Ancient Mayan astronomical calculations that still amaze modern scientists.",
        "The historical origins of banking systems and their evolution.",
        "How colonial policies continue to impact modern global economics."
    ],
    "Business": [
        "Problem-solution fit: Why the best businesses solve painful problems.",
        "Recession-proof business models thriving in economic downturns.",
        "The cashflow management strategies of billion-dollar companies.",
        "How storytelling creates emotional connections with brand consumers.",
        "Risk mitigation strategies for scaling businesses beyond $10M revenue.",
        "The psychology behind premium pricing strategies that increase profits.",
        "How vertical integration is changing competitive landscapes.",
        "Customer retention strategies that outperform acquisition in ROI."
    ],
    "Psychology": [
        "The neuroscience of habit formation and behavior change.",
        "How cognitive biases influence consumer purchasing decisions.",
        "The impact of sleep quality on cognitive performance and decision-making.",
        "Flow state psychology: How to achieve optimal performance conditions.",
        "The psychological factors behind successful negotiation outcomes.",
        "How social proof mechanisms influence group behavior.",
        "The relationship between mindfulness practice and stress reduction.",
        "Psychological pricing strategies that increase perceived value."
    ],
    "Technology": [
        "Quantum computing applications that will transform cybersecurity.",
        "How edge computing is revolutionizing IoT implementations.",
        "The technical challenges of scaling blockchain for mass adoption.",
        "Neuromorphic computing designs mimicking human brain architecture.",
        "How 6G will transform connectivity beyond current imagination.",
        "The environmental impact of data centers and sustainable solutions.",
        "Biometric authentication technologies and their security implications.",
        "How API-first development is changing software architecture."
    ],
    "Health": [
        "The gut-brain connection: How nutrition affects cognitive function.",
        "Intermittent fasting protocols backed by research studies.",
        "Genetic testing applications for personalized healthcare approaches.",
        "How telemedicine is transforming healthcare delivery in rural areas.",
        "Evidence-based stress management techniques for professionals.",
        "The impact of environmental toxins on hormonal balance.",
        "Sleep optimization strategies based on chronobiology research.",
        "The science of longevity: Interventions supported by research."
    ],
    "Science": [
        "CRISPR gene editing applications beyond medical treatments.",
        "Dark matter theories that could revolutionize our understanding of physics.",
        "Biomimicry innovations solving complex engineering challenges.",
        "The latest findings on exoplanet atmospheric composition.",
        "How materials science is enabling next-generation battery technology.",
        "Ocean acidification impacts on marine ecosystems and food chains.",
        "Neuroplasticity research challenging traditional brain development theories.",
        "Climate modeling improvements that enhance prediction accuracy."
    ],
    "Finance": [
        "Algorithmic trading strategies used by quantitative hedge funds.",
        "Decentralized finance protocols disrupting traditional banking.",
        "Tax optimization structures for digital entrepreneurs.",
        "The psychological factors affecting investment decision-making.",
        "Real estate investment trends in emerging markets.",
        "How central bank policies impact different asset classes.",
        "Portfolio diversification strategies during inflationary periods.",
        "Wealth preservation techniques during economic uncertainty."
    ],
    "Creativity": [
        "The neuroscience of creativity and innovative thinking.",
        "Divergent thinking exercises that enhance problem-solving abilities.",
        "How constraints paradoxically increase creative output quality.",
        "The connection between travel experiences and creative breakthroughs.",
        "Cross-disciplinary approaches that drive innovation.",
        "How ambient noise levels affect creative thinking processes.",
        "The relationship between solitude and creative production.",
        "Creativity enhancement techniques used by renowned artists."
    ],
    "Environment": [
        "Regenerative agriculture practices that sequester carbon.",
        "Ocean plastic cleanup technologies showing promising results.",
        "The economic case for renewable energy infrastructure.",
        "Urban planning designs that reduce carbon footprints.",
        "The impact of rewilding projects on biodiversity restoration.",
        "Sustainable material innovations replacing plastics.",
        "Water conservation technologies for agricultural applications.",
        "How circular economy models reduce waste and increase profits."
    ]
}

# Create static directory for CSS/JS if it doesn't exist
os.makedirs(os.path.join(app.static_folder), exist_ok=True)

# Create CSS file with galaxy background
with open(os.path.join(app.static_folder, 'style.css'), 'w') as f:
    f.write('''
    body {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?q=80&w=1200');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
        font-family: 'Arial', sans-serif;
        margin: 0;
        padding: 0;
        min-height: 100vh;
    }
    
    .container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
    }
    
    .card {
        background-color: rgba(13, 17, 43, 0.8);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        width: 100%;
        box-shadow: 0 0 20px rgba(103, 128, 255, 0.5);
        text-align: center;
    }
    
    h1 {
        color: #7B68EE;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 30px;
        text-shadow: 0 0 10px rgba(123, 104, 238, 0.5);
    }
    
    label {
        display: block;
        margin-bottom: 8px;
        font-weight: bold;
        color: #9DB4FF;
    }
    
    input, select {
        width: 100%;
        padding: 12px;
        margin-bottom: 20px;
        border-radius: 8px;
        border: 2px solid #3D5AFE;
        background-color: rgba(30, 40, 70, 0.8);
        color: white;
        font-size: 16px;
    }
    
    button {
        background: linear-gradient(45deg, #3D5AFE, #7B68EE);
        color: white;
        border: none;
        padding: 12px 25px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
        margin-top: 10px;
        transition: all 0.3s ease;
    }
    
    button:hover {
        background: linear-gradient(45deg, #7B68EE, #3D5AFE);
        transform: translateY(-2px);
        box-shadow: 0 7px 14px rgba(59, 43, 91, 0.3);
    }
    
    .thread-container {
        margin-top: 30px;
        width: 100%;
    }
    
    .thread {
        background-color: rgba(25, 32, 71, 0.7);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        border-left: 4px solid #7B68EE;
    }
    
    .insight {
        background-color: rgba(41, 53, 116, 0.5);
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        text-align: left;
        border-left: 3px solid #3D5AFE;
    }
    
    .checkbox-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .checkbox-container input {
        width: auto;
        margin-right: 10px;
    }
    
    .sparkle {
        color: #FFD700;
        margin-right: 5px;
    }
    
    @media (max-width: 600px) {
        .container {
            padding: 15px;
        }
        
        .card {
            padding: 15px;
        }
    }
    ''')

# Create HTML template
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/generate_thread', methods=['POST'])
def generate_thread():
    try:
        data = request.json
        topic = data.get("topic", "AI").strip()  # Default to AI if no topic is entered
        num_threads = min(int(data.get("num_threads", 1)), 10)  # Limit to 10 threads max
        thread_length = min(int(data.get("thread_length", 5)), 8)  # Limit to 8 insights per thread
        random_mode = data.get("random_mode", False)  # Enable random topic selection
        
        # Input validation
        if num_threads < 1:
            num_threads = 1
        if thread_length < 1:
            thread_length = 1
            
        print(f"Request Received: Topic={topic}, Threads={num_threads}, Length={thread_length}, Random={random_mode}")
        
        threads = []
        used_insights = set()  # Track used insights to avoid duplicates
        
        for i in range(num_threads):
            thread = []
            
            if random_mode:
                # True randomness - completely different topics for each thread
                available_topics = list(TOPIC_DATABASE.keys())
                random.shuffle(available_topics)
                selected_topic = available_topics[i % len(available_topics)]
                
                # Get available insights that haven't been used yet
                available_insights = [insight for insight in TOPIC_DATABASE[selected_topic] 
                                      if insight not in used_insights]
                
                # If we've used all insights, reset the used_insights set
                if len(available_insights) < thread_length:
                    available_insights = TOPIC_DATABASE[selected_topic]
                    
                # Select random insights
                selected_insights = random.sample(
                    available_insights, 
                    min(thread_length, len(available_insights))
                )
                
                # Add topic prefix to each insight
                thread = [f"✨ {selected_topic}: {insight}" for insight in selected_insights]
                
                # Track used insights
                used_insights.update(selected_insights)
                
            else:
                # Topic-specific mode - use requested topic if available
                if topic in TOPIC_DATABASE:
                    available_insights = [insight for insight in TOPIC_DATABASE[topic] 
                                         if insight not in used_insights]
                    
                    # If we've used all insights, reset the used_insights set
                    if len(available_insights) < thread_length:
                        available_insights = TOPIC_DATABASE[topic]
                    
                    selected_insights = random.sample(
                        available_insights, 
                        min(thread_length, len(available_insights))
                    )
                    
                    thread = [f"✨ {topic}: {insight}" for insight in selected_insights]
                    used_insights.update(selected_insights)
                    
                else:
                    # If topic doesn't exist, provide better placeholder content
                    fallback_topics = list(TOPIC_DATABASE.keys())
                    random.shuffle(fallback_topics)
                    fallback_topic = fallback_topics[0]
                    
                    thread = [
                        f"✨ Topic '{topic}' not found in database. Here's an insight on {fallback_topic}:",
                        *random.sample(TOPIC_DATABASE[fallback_topic], min(thread_length-1, len(TOPIC_DATABASE[fallback_topic])))
                    ]
            
            threads.append(thread)
            
        print(f"Generated {len(threads)} threads successfully")
        return jsonify({
            "threads": threads,
            "status": "success"
        })
        
    except Exception as e:
        print(f"Error generating thread: {e}")
        return jsonify({
            "error": f"Internal Server Error: {str(e)}",
            "status": "error"
        }), 500

# Create HTML template file
os.makedirs('templates', exist_ok=True)
with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Insight Generator</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>✨ Insight Generator ✨</h1>
        
        <div class="card">
            <label for="topic">Topic:</label>
            <input type="text" id="topic" placeholder="Enter a topic (e.g., AI, Business, Sports)">
            
            <label for="numThreads">Number of Threads:</label>
            <input type="number" id="numThreads" min="1" max="10" value="1">
            
            <label for="threadLength">Insights per Thread:</label>
            <input type="number" id="threadLength" min="1" max="8" value="5">
            
            <div class="checkbox-container">
                <input type="checkbox" id="randomMode">
                <label for="randomMode">Enable Random Topic Mode</label>
            </div>
            
            <button onclick="generateThread()">Generate Insights</button>
        </div>
        
        <div id="threadContainer" class="thread-container"></div>
    </div>

    <script>
        async function generateThread() {
            const topic = document.getElementById('topic').value || 'AI';
            const numThreads = parseInt(document.getElementById('numThreads').value) || 1;
            const threadLength = parseInt(document.getElementById('threadLength').value) || 5;
            const randomMode = document.getElementById('randomMode').checked;
            
            // Show loading state
            document.getElementById('threadContainer').innerHTML = '<div class="thread"><p>Generating insights...</p></div>';
            
            try {
                const response = await fetch('/generate_thread', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        topic,
                        num_threads: numThreads,
                        thread_length: threadLength,
                        random_mode: randomMode
                    }),
                });
                
                const data = await response.json();
                
                if (data.status === 'error') {
                    document.getElementById('threadContainer').innerHTML = `
                        <div class="thread">
                            <p>Error: ${data.error}</p>
                        </div>
                    `;
                    return;
                }
                
                let threadsHTML = '';
                
                data.threads.forEach((thread, index) => {
                    let insightsHTML = '';
                    
                    thread.forEach((insight, i) => {
                        insightsHTML += `
                            <div class="insight">
                                <p>${insight}</p>
                            </div>
                        `;
                    });
                    
                    threadsHTML += `
                        <div class="thread">
                            <h3>Thread ${index + 1}</h3>
                            ${insightsHTML}
                        </div>
                    `;
                });
                
                document.getElementById('threadContainer').innerHTML = threadsHTML;
                
            } catch (error) {
                document.getElementById('threadContainer').innerHTML = `
                    <div class="thread">
                        <p>Error: ${error.message}</p>
                    </div>
                `;
            }
        }
    </script>
</body>
</html>
''')

if __name__ == '__main__':
    print("✨ Insight Generator server is running!")
    print("✨ Access the application at http://127.0.0.1:5000")
    app.run(debug=True)
