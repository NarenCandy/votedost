# VoteDost - Your Indian Election Assistant

VoteDost is a smart, dynamic, and interactive election assistant designed for the **Virtual Prompt Wars Challenge 2**. It helps Indian citizens navigate the complexities of the electoral process by providing reliable information on voter registration, candidate eligibility, EVMs, timelines, and more.

## 🌐 Live Demo
👉 [https://votedost-864461954747.us-central1.run.app](https://votedost-864461954747.us-central1.run.app)

## ✨ Features
- 🤖 AI-powered election Q&A via Google Vertex AI (Gemini 2.5 Flash)
- 🌐 7 Indian language support (English, Hindi, Tamil, Telugu, Kannada, Bengali, Marathi) with auto-detection
- 📚 Election Guide with key laws, voter rights and ECI info
- 🗓️ Visual step-by-step Indian election process timeline
- ❓ Interactive FAQ accordion with 10 common questions
- 🔍 Smart autocomplete suggestions as you type
- 📱 Fully mobile responsive with bottom navigation
- ✨ Premium glassmorphism UI with Three.js WebGL particle background
- 🎨 Smooth GSAP animations throughout

## 🎯 Chosen Vertical
**Civic Technology & Election Assistance**

## 🧠 Approach and Logic
The goal was to create an interface that feels highly premium and modern (a "billion-dollar look") while ensuring the application remains lightweight, fast, and accessible.

1. **Intelligent Conversational AI:** The core of the assistant is powered by Google's **Vertex AI (Gemini 2.5 Flash)**. We designed a custom system prompt that instructs the model to act as a friendly, knowledgeable guide for Indian elections.
2. **Context-Aware Multi-Language Support:** To cater to the diverse linguistic landscape of India, VoteDost supports Auto-Language Detection and allows manual language selection (English, Hindi, Tamil, Telugu, Kannada, Bengali, Marathi). The selected language is dynamically injected into the Gemini prompt via the backend, ensuring accurate localized responses.
3. **Interactive UI/UX:** Built with a modern glassmorphism aesthetic, integrating a dynamic WebGL particle background using **Three.js** and smooth UI transitions using **GSAP**.
4. **Structured Content Panels:** Recognizing that users sometimes prefer browsing over chatting, we implemented dedicated content panels (Election Guide Grid, Vertical Timeline, Interactive FAQs) that exist alongside the AI chat.

## ⚙️ How the Solution Works
- **Frontend:** Pure HTML, CSS, and vanilla JavaScript. We avoided heavy frontend frameworks to keep the repository size incredibly small (< 1 MB). It utilizes responsive CSS Grid/Flexbox and dynamic DOM manipulation for tab switching, FAQ accordions, and autocomplete suggestions.
- **Backend:** A lightweight Python **Flask** server handles routing and secure API communication.
- **Google Services Integration:** The backend seamlessly communicates with **Google Cloud Vertex AI (`gemini-2.5-flash`)** using the official Python SDK. It maintains conversation history to provide contextual, multi-turn responses.
- **Security:** No hardcoded API keys. The application relies entirely on secure environment variables (`GOOGLE_CLOUD_PROJECT`) and Google Application Default Credentials, ensuring safe and responsible implementation.
- **Efficiency:** The Three.js particle system uses an optimized custom `ShaderMaterial` to handle 300 varied particles without lagging the browser. External libraries are loaded via CDNs to minimize the repository footprint.

## 📌 Assumptions Made
1. **Google Cloud Environment:** It is assumed the user running this app locally has authenticated via `gcloud auth application-default login` and has the Vertex AI API enabled on their specified Google Cloud Project.
2. **Connectivity:** The app assumes an active internet connection to load CDN resources (Three.js, GSAP, Google Fonts) and communicate with the Vertex AI endpoint.
3. **Stateless Sessions:** For this MVP, conversation history is stored in the frontend client state (`history` array in JS) rather than a persistent backend database. Refreshing the page clears the chat history.

## 🚀 Running Locally
1. Ensure Python 3.9+ is installed.
2. Install dependencies: `pip install -r requirements.txt`
3. Set your Google Cloud Project:
   - Windows (PowerShell): `$env:GOOGLE_CLOUD_PROJECT="your-project-id"`
   - Mac/Linux: `export GOOGLE_CLOUD_PROJECT="your-project-id"`
4. Authenticate with Google Cloud: `gcloud auth application-default login`
5. Run the server: `python app.py`
6. Open `http://localhost:8080` in your browser.

## ☁️ Deployment (Google Cloud Run)
1. Build and submit Docker image:
```bash
   gcloud builds submit --tag gcr.io/votedost/votedost
```
2. Deploy to Cloud Run:
```bash
   gcloud run deploy votedost \
     --image gcr.io/votedost/votedost \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GOOGLE_CLOUD_PROJECT=votedost
```

## 🛠️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, Vanilla JavaScript |
| Backend | Python, Flask |
| AI Model | Google Vertex AI (Gemini 2.5 Flash) |
| Animations | Three.js, GSAP |
| Fonts | Plus Jakarta Sans |
| Deployment | Google Cloud Run |
| Auth | Google Application Default Credentials |