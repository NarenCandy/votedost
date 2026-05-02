# 🗳️ VoteDost - Your Indian Election Assistant

> *"Dost" means Friend in Hindi — VoteDost is every Indian voter's friendly guide to elections.*

VoteDost is a smart, dynamic, and interactive AI-powered election assistant designed for the **Virtual Prompt Wars Challenge 2**. It helps Indian citizens navigate the complexities of the electoral process through conversational AI, structured content panels, and a premium modern interface.

## 🌐 Live Demo
👉 [https://votedost-864461954747.us-central1.run.app](https://votedost-864461954747.us-central1.run.app)

## ✨ Complete Feature List

### 🤖 AI Chat Assistant
- Powered by **Google Vertex AI (Gemini 2.5 Flash)**
- Conversational multi-turn chat with full history context
- Custom system prompt designed specifically for Indian election knowledge
- Covers: voter registration, ECI, EVMs, VVPAT, NOTA, MCC, candidate eligibility, and more
- Gracefully rejects off-topic questions and stays focused on elections

### 🌐 Multi-Language Support
- **7 Indian languages supported:** English, Hindi (हिंदी), Tamil (தமிழ்), Telugu (తెలుగు), Kannada (ಕನ್ನಡ), Bengali (বাংলা), Marathi (मराठी)
- **Auto-language detection** — responds in the language the user types in
- Manual language selector dropdown in the topbar
- Selected language dynamically injected into Gemini system prompt for accurate responses
- Input placeholder text updates to match selected language

### 📚 Election Guide Panel
- Dedicated browsable panel with 8 information cards
- Covers: ECI overview, voter eligibility, how to get Voter ID, candidate eligibility, Model Code of Conduct, EVM explanation, VVPAT, and Right to NOTA
- 2-column card grid on desktop, 1-column on mobile
- Each card has icon, bold title, and clear description

### 🗓️ Election Timeline Panel
- Beautiful **visual vertical timeline** of the complete Indian election process
- 11 steps from Election Announcement to Results & Declaration
- Alternating left/right cards on desktop, left-aligned on mobile
- Each step has numbered gradient circle, icon, title and description
- Animated with **GSAP** slide-in effect when panel opens
- Steps covered:
  1. Election Announcement
  2. Model Code of Conduct Begins
  3. Voter List Finalization
  4. Nomination Filing
  5. Scrutiny of Nominations
  6. Withdrawal of Candidature
  7. Campaign Period
  8. Campaign Silence Period
  9. Polling Day
  10. Counting of Votes
  11. Results & Declaration

### ❓ Interactive FAQ Panel
- **10 frequently asked questions** in accordion style
- Smooth expand/collapse animation
- Only one question open at a time
- Active question highlighted in accent color
- Questions covered:
  - How to register to vote
  - Valid IDs at polling booth
  - What is NOTA
  - Voting without name on list
  - Minimum voting age
  - Booth assignment rules
  - Vote bribery reporting
  - Lok Sabha vs Vidhan Sabha difference
  - How to check voter list
  - What is Model Code of Conduct

### 🔍 Smart Autocomplete
- 12 predefined election-related suggestions
- Filters in real time as user types (case insensitive)
- Shows maximum 4 matching suggestions at a time
- Matching text highlighted in accent color
- Click to fill input, Escape to dismiss
- Glassmorphism styled dropdown matching app theme

### 🎨 Premium UI Design
- **Deep space dark theme** (#050508 near-black background)
- **Glassmorphism** chat container with frosted glass effect
- **Rich color palette:** deep violet (#7c3aed) + electric blue (#2563eb) + gold (#f59e0b) accents
- **Plus Jakarta Sans** typography throughout
- User avatar with gradient initial letter circle
- Bot avatar with gradient square and election icon
- Subtle 3px left border accent on bot messages
- Gold shimmer effect on send button hover
- Live pulsing green status indicator in topbar
- Language auto-detect badge in topbar
- "Powered by Gemini" badge with Google colors in sidebar

### ✨ Animations & Effects
- **Three.js WebGL particle background** with 300 particles
  - 70% deep violet particles, 30% gold particles
  - Varying particle sizes for depth effect
  - Constellation-style connecting lines (opacity 0.06)
  - Mouse cursor tracking and rotation
  - Optimized with custom ShaderMaterial for smooth performance
- **GSAP animations** on all chat messages (slide-in from bottom)
- GSAP timeline panel card animations
- Smooth FAQ accordion expand/collapse
- Typing indicator with 3 bouncing dots while AI responds
- Chip hover lift effect
- Send button scale animation on click

### 🧭 Navigation
- **Desktop:** Left sidebar (220px) with:
  - VoteDost logo and gradient title
  - Nav items: Chat, Election Guide, Timeline, FAQs
  - Quick Questions chips section
  - Powered by Gemini badge at bottom
- **Mobile:** Fixed bottom navigation bar with icons for all 4 sections
- Active nav item highlighted with accent color
- Smooth panel switching — only one view visible at a time

### 📱 Mobile Responsive
- Sidebar hidden on mobile, replaced with bottom nav bar
- Bottom nav uses `dvh` (dynamic viewport height) for Chrome mobile compatibility
- Safe area insets for iPhone notch and Android gesture navigation
- Chat bubbles expand to 90% width on mobile
- FAQ accordion touch-friendly
- Timeline switches to left-aligned single column on mobile
- Language selector accessible on mobile
- All content panels properly padded above bottom nav bar

### 🔒 Security & Performance
- Zero hardcoded API keys
- Google Application Default Credentials for secure Vertex AI access
- Environment variable based configuration
- Lightweight frontend — no heavy frameworks, repo size under 1MB
- All JS libraries loaded via CDN (zero repo size impact)
- Markdown rendering for bot responses (bold, italic, lists)
- Graceful error handling throughout

## 🎯 Chosen Vertical
**Civic Technology & Election Assistance**

## 🧠 Approach and Logic
The goal was to build an app that feels like a **funded product** while staying lightweight and laser-focused on the problem statement — helping users understand the Indian election process in an interactive and easy-to-follow way.

1. **Intelligent Conversational AI:** Custom Gemini system prompt tuned specifically for Indian election knowledge. The bot stays on topic, responds in the user's language, and handles multi-turn conversations naturally.

2. **Dual Mode — Chat + Browse:** Not all users want to type questions. The Election Guide, Timeline, and FAQs panels let users browse structured content without chatting, making the app accessible for all types of users.

3. **Language First:** India has 22 official languages. Supporting 7 major ones with both auto-detection and manual selection makes VoteDost genuinely useful for a diverse population.

4. **Premium but Lightweight:** Deep space theme, WebGL particles, GSAP animations — all achieved with pure HTML/CSS/JS and CDN libraries. No React, no bundlers, no bloat.

## ⚙️ How the Solution Works

| Layer | Details |
|-------|---------|
| Frontend | Pure HTML, CSS, Vanilla JavaScript |
| Backend | Python Flask |
| AI Model | Google Vertex AI — Gemini 2.5 Flash |
| 3D Background | Three.js (WebGL) |
| Animations | GSAP 3 |
| Fonts | Plus Jakarta Sans (Google Fonts) |
| Deployment | Google Cloud Run |
| Auth | Google Application Default Credentials |

## 📌 Assumptions Made
1. **Google Cloud Environment:** User running locally has authenticated via `gcloud auth application-default login` and has Vertex AI API enabled on their GCP project.
2. **Connectivity:** Active internet connection required for CDN resources and Vertex AI API calls.
3. **Stateless Sessions:** Conversation history stored in frontend JS state. Refreshing the page clears chat history.
4. **Browser Support:** Web Speech API features (if added) require a modern browser. Core chat functionality works on all browsers.

## 🚀 Running Locally
1. Ensure Python 3.9+ is installed
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Set your Google Cloud Project:
```bash
   # Windows (PowerShell)
   $env:GOOGLE_CLOUD_PROJECT="votedost"

   # Mac/Linux
   export GOOGLE_CLOUD_PROJECT="votedost"
```
4. Authenticate with Google Cloud:
```bash
   gcloud auth application-default login
```
5. Run the server:
```bash
   python app.py
```
6. Open [http://localhost:8080](http://localhost:8080)

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
3. Access your live URL from Cloud Run dashboard

## 📁 Project Structure
votedost/
├── app.py              # Flask backend + Vertex AI integration
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container configuration
├── .dockerignore       # Docker ignore rules
├── static/
│   ├── style.css       # All styling + animations
│   └── script.js       # Frontend logic + Three.js + GSAP
└── templates/
└── index.html      # Main app layout

## 🏆 Built For
**PromptWars: Virtual — Challenge 2**
Hack2Skill × Google Cloud