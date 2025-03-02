### **Master Prompt for AI to Fix the Twitter Thread Generator**

**Objective:**  
You are a highly advanced AI developer tasked with **fixing, optimizing, and enhancing** an AI-powered **Twitter Thread Generator**. The system fetches trending topics and insights from **Reddit, Twitter, NewsAPI**, and an internal database, generating **high-quality Twitter threads** in a structured format.

**Current Issues to Fix & Improvements Needed:**
---

### **1️⃣ CORS Error (Critical)**
- **Issue:** The backend API `https://twitter-generator-api.up.railway.app/generate_thread` is **blocked by CORS policy** when requested from `https://kyle4814.github.io`.
- **Fix:**  
  - Ensure the backend **Flask API includes the correct CORS headers** to allow cross-origin requests.
  - Use `Flask-CORS` properly and **set the correct origins**:
    ```python
    from flask_cors import CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    ```
  - Verify that **preflight OPTIONS requests** receive a proper response.

---

### **2️⃣ API Endpoint Not Handling Requests Properly**
- **Issue:** The frontend is making a **POST request to `/generate_thread`**, but the backend is **returning a 405 (Method Not Allowed)**.
- **Fix:**  
  - Ensure the Flask route is correctly defined:
    ```python
    @app.route('/generate_thread', methods=['POST'])
    ```
  - Confirm **the deployed backend matches the latest GitHub version**.
  - Verify the `requirements.txt` file includes **all necessary dependencies**.

---

### **3️⃣ Fetching & Processing External Data Sources**
- **Issue:** The generator is **not pulling diverse insights** and is **biased towards AI topics**.
- **Fix:**  
  - Ensure **proper API calls to Reddit, Twitter, and NewsAPI** for dynamic content.
  - Implement **Redis caching** for efficiency.
  - Example fix for **Reddit fetching**:
    ```python
    def fetch_reddit_insights(topic):
        headers = {"User-Agent": "TwitterThreadGenerator/1.0"}
        url = f"https://www.reddit.com/r/{topic}/top.json?limit=5"
        response = requests.get(url, headers=headers)
        return [post["data"]["title"] for post in response.json().get("data", {}).get("children", [])]
    ```

---

### **4️⃣ Improved UI & Frontend Fixes**
- **Issue:** The frontend **looks broken** and **missing styles**.
- **Fix:**  
  - **Ensure `style.css` is correctly linked** (`404 Not Found` issue).
  - Fix `script.js` **missing or broken function calls**.
  - Verify **HTML input elements work properly**.

---

### **5️⃣ GitHub Push Issues**
- **Issue:** User **cannot push new commits** due to a **remote branch conflict**.
- **Fix:**  
  - Use the following **Git commands**:
    ```bash
    git pull origin main --rebase
    git add .
    git commit -m "Fix CORS, API issues, UI improvements"
    git push origin main
    ```

---

### **Final Deliverables**
- ✅ **Fixed Backend API** (CORS, API handling, external data fetching)
- ✅ **Optimized Frontend** (CSS fixes, working JS, correct API calls)
- ✅ **Fully Functional Deployment** (GitHub & Railway working perfectly)

---

**GOAL:**  
This AI-powered **Twitter Thread Generator** should be **flawless, seamless, and generate viral threads** in **seconds**. Fix **every single issue** and **maximize performance**. 🚀
