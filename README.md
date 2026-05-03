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
- **Request-time model status verification** for high availability
- Context-aware response caching (lru_cache) with composite key (message + language + history)

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
- Smooth expand/collapse animation with aria-expanded states
- Only one question open at a time
- Active question highlighted in accent color
- Fully keyboard accessible (Tab, Enter, Space)
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
- 150ms debounced input handler for smooth performance
- Filters in real time as user types (case insensitive)
- Shows maximum 4 matching suggestions at a time
- Matching text highlighted in accent color
- Full keyboard navigation (Arrow keys, Enter, Escape)
- Click to fill input, Escape to dismiss
- Glassmorphism styled dropdown matching app theme

### ♿ Accessibility
- Skip navigation link for keyboard users
- Full ARIA implementation: roles, labels, live regions
- `role="log"` on chat messages for screen reader announcements
- `aria-expanded` states on FAQ accordion items
- `aria-current="page"` on active navigation items
- `aria-live="polite"` on chat and status indicators
- Focus-visible styles for all interactive elements
- High contrast media query support (`prefers-contrast: high`)
- Reduced motion support (`prefers-reduced-motion: reduce`)
- Semantic HTML throughout (aside, nav, header, main, footer, region)
- Screen reader only utility class (`.sr-only`)
- All interactive elements keyboard reachable via Tab

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
  - WebGL error boundary — falls back to CSS gradient if WebGL unavailable
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

### 📲 PWA Support
- `manifest.json` included for "Add to Home Screen" support
- App name, theme color, and display mode configured
- Mobile-first experience with native app feel

### 🔍 SEO & Social
- Meta description and keywords tags
- Open Graph tags for social media sharing (og:title, og:description, og:url)
- Semantic HTML structure for search engine indexing

### ☁️ Expanded Google Cloud Integration
- **Vertex AI** — Gemini 2.5 Flash for conversational AI with dynamic status checks
- **Firestore** — Real-time session persistence and chat history analytics
- **BigQuery** — Structured data logging for long-term usage tracking and election insights
- **Cloud Translation API** — Proactive language detection and enhanced multilingual support
- **Secret Manager** — Secure configuration management pattern for sensitive environment variables
- **Google Cloud Logging** — Professional-grade observability with unique Request IDs and latency metrics per request
- **Cloud Run** — Fully managed serverless deployment with automated health checks
- **Google Application Default Credentials** — Secure, keyless authentication throughout the stack

### 🔒 Security & Performance Hardening
- **Rate Limiting** — Integrated `Flask-Limiter` with `memory://` storage to protect endpoints from abuse
- **Security Headers** — Enforced middleware for CSP, HSTS, X-Frame-Options, and XSS Protection
- **Input Sanitization** — Robust routines handling null bytes, unicode normalization, and length constraints
- **Zero Hardcoded Keys** — 100% reliance on environment variables and Google Secret Manager
- **Input Validation** — Message length limits (2000 chars), whitespace stripping, and strict JSON validation
- **Malicious Input Handling** — Protection against HTML injection, SQL injection, and JSON injection
- **Lightweight Frontend** — No heavy frameworks, optimized repo size under 1MB
- **Optimized Performance** — All JS libraries loaded via CDN (zero repo size impact)
- **Markdown Rendering** — Bot responses support rich formatting (bold, italic, lists)
- **Global Error Handling** — Professional 404 and 500 handlers ensuring zero raw data leakage

### 🧪 Comprehensive Testing Suite
- **84 professional test cases** using Python unittest and advanced mocking
- **100% feature coverage** including security, accessibility, and service fallbacks
- **Fail-safe Verification** — Tests for Google service failures (Firestore down, BigQuery unreachable, etc.)
- **Test Classes:**
  - Index & Health Routes (10 tests)
  - Chat Logic & Language Support (17 tests)
  - Conversation History (6 tests)
  - Edge Cases & Malicious Inputs (11 tests)
  - Error Handling (5 tests)
  - Security & Headers (7 tests)
  - Google Services Integration (11 tests)
  - Accessibility Compliance (7 tests)
  - Integration Flows (10 tests)
- **Execution:** `python -m pytest tests/ -v --cov=app`

## 🎯 Chosen Vertical
**Civic Technology & Election Assistance**

## 🧠 Approach and Logic

1. **Intelligent Conversational AI:** Custom Gemini system prompt tuned specifically for Indian election knowledge. The bot stays on topic, responds in the user's language, and handles multi-turn conversations naturally.

2. **Dual Mode — Chat + Browse:** Not all users want to type questions. The Election Guide, Timeline, and FAQs panels let users browse structured content without chatting, making the app accessible for all types of users.

3. **Language First:** India has 22 official languages. Supporting 7 major ones with both auto-detection and manual selection makes VoteDost genuinely useful for a diverse population.

4. **Premium but Lightweight:** Deep space theme, WebGL particles, GSAP animations — all achieved with pure HTML/CSS/JS and CDN libraries. No React, no bundlers, no bloat.

5. **Enterprise-grade Observability:** Google Cloud Logging integration ensures every request is tracked with unique IDs and latency metrics — production-ready from day one.

## ⚙️ How the Solution Works

| Layer | Details |
|-------|---------|
| Frontend | Pure HTML, CSS, Vanilla JavaScript |
| Backend | Python Flask |
| AI Model | Google Vertex AI — Gemini 2.5 Flash |
| 3D Background | Three.js (WebGL) |
| Animations | GSAP 3 |
| Fonts | Plus Jakarta Sans (Google Fonts) |
| Logging | Google Cloud Logging |
| Deployment | Google Cloud Run |
| Auth | Google Application Default Credentials |
| Testing | Python unittest + pytest |

## 📌 Assumptions Made
1. **Google Cloud Environment:** User running locally has authenticated via `gcloud auth application-default login` and has Vertex AI API enabled on their GCP project.
2. **Connectivity:** Active internet connection required for CDN resources and Vertex AI API calls.
3. **Stateless Sessions:** Conversation history stored in frontend JS state. Refreshing the page clears chat history.
4. **Browser Support:** Core chat functionality works on all modern browsers. WebGL required for particle background (CSS gradient fallback provided).

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
7. Run tests:
```bash
python -m pytest tests/ -v --cov=app
```

## ☁️ Deployment (Google Cloud Run)
```bash
gcloud run deploy votedost \
  --source . \
  --project votedost \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=votedost
```

## 📁 Project Structure (Modular v1.1)
```
votedost/
├── app.py                  # Proxy entry point for backward compatibility
├── requirements.txt        # Python dependencies (flask-limiter, google-cloud-*)
├── Dockerfile              # Production container configuration
├── .flake8                 # Linting configuration
├── pyproject.toml          # Tooling configuration
├── app/                    # Main application package
│   ├── __init__.py         # App factory + rate limiter + middleware
│   ├── config.py           # Dataclass-based configuration
│   ├── routes/             # Modular blueprints
│   │   └── chat.py         # Main chat and health routes
│   ├── services/           # Decoupled Google Cloud service integrations
│   │   ├── ai_service.py   # Vertex AI (Gemini)
│   │   ├── firestore.py    # Firestore analytics
│   │   ├── bigquery.py     # BigQuery logging
│   │   └── translation.py  # Language detection
│   ├── models/             # Shared data models
│   └── utils/              # Validators and exception handlers
├── tests/                  # 84 comprehensive test cases
│   ├── test_app.py         # Legacy and core logic tests
│   ├── test_security.py    # Security and header validation
│   ├── test_google_services.py # Service fallback tests
│   └── test_accessibility.py # WCAG compliance tests
├── static/                 # Frontend assets (style.css, script.js, manifest.json)
└── templates/              # HTML templates (index.html)
```

## 🏆 Built For
**PromptWars: Virtual — Challenge 2**
Hack2Skill × Google Cloud