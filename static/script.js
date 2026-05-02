/**
 * VoteDost - Frontend Logic
 * ------------------------
 * Handles Three.js background, chat interactions, language selection,
 * tab switching, and accessibility updates.
 */

// --- Constants & State ---
const SUPPORTED_LANGUAGES = ["English", "Hindi", "Tamil", "Telugu", "Kannada", "Bengali", "Marathi"];
const PLACEHOLDERS = {
    "English": "Ask about elections...",
    "Hindi": "चुनाव के बारे में पूछें...",
    "Tamil": "தேர்தல் பற்றி கேளுங்கள்...",
    "Telugu": "ఎన్నికల గురించి అడగండి...",
    "Kannada": "ಚುನಾವಣೆಯ ಬಗ್ಗೆ ಕೇಳಿ...",
    "Bengali": "নির্বাচন সম্পর্কে জিজ্ঞাসা করুন...",
    "Marathi": "निवडणुकीबद्दल विचारा..."
};

let history = [];
let selectedLanguage = "English";
let autocompleteIndex = -1;

// --- Utility Functions ---

/**
 * Debounce function to limit excessive function calls.
 */
const debounce = (func, wait) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
};

/**
 * Basic Markdown Parser for bold and newlines.
 */
const parseMarkdown = (text) => {
    if (!text) return "";
    let parsed = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    parsed = parsed.replace(/\*(.*?)\*/g, '<em>$1</em>');
    parsed = parsed.replace(/\n/g, '<br>');
    return parsed;
};

// --- Three.js Particle Background ---

/**
 * Initializes the Three.js particle background with an error boundary.
 */
const initThreeJS = () => {
    try {
        const container = document.getElementById('canvas-container');
        if (!container) return;

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        
        // Use antialias only if supported/performant
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        // Particles Configuration
        const particlesCount = 300;
        const particlesGeometry = new THREE.BufferGeometry();
        
        const posArray = new Float32Array(particlesCount * 3);
        const colorsArray = new Float32Array(particlesCount * 3);
        const sizesArray = new Float32Array(particlesCount);
        
        const colorPurple = new THREE.Color('#7c3aed');
        const colorGold = new THREE.Color('#f59e0b');
        
        for(let i = 0; i < particlesCount; i++) {
            posArray[i * 3] = (Math.random() - 0.5) * 12;
            posArray[i * 3 + 1] = (Math.random() - 0.5) * 12;
            posArray[i * 3 + 2] = (Math.random() - 0.5) * 8;
            
            const isGold = Math.random() > 0.7;
            const color = isGold ? colorGold : colorPurple;
            
            colorsArray[i * 3] = color.r;
            colorsArray[i * 3 + 1] = color.g;
            colorsArray[i * 3 + 2] = color.b;
            
            sizesArray[i] = Math.random() * 0.03 + 0.01;
        }
        
        particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        particlesGeometry.setAttribute('customColor', new THREE.BufferAttribute(colorsArray, 3));
        particlesGeometry.setAttribute('size', new THREE.BufferAttribute(sizesArray, 1));
        
        const vertexShader = `
            attribute float size;
            attribute vec3 customColor;
            varying vec3 vColor;
            void main() {
                vColor = customColor;
                vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
                gl_PointSize = size * (300.0 / -mvPosition.z);
                gl_Position = projectionMatrix * mvPosition;
            }
        `;
        
        const fragmentShader = `
            varying vec3 vColor;
            void main() {
                float r = distance(gl_PointCoord, vec2(0.5));
                if (r > 0.5) discard;
                gl_FragColor = vec4(vColor, 0.8);
            }
        `;

        const material = new THREE.ShaderMaterial({
            vertexShader,
            fragmentShader,
            transparent: true,
            depthWrite: false
        });
        
        const particlesMesh = new THREE.Points(particlesGeometry, material);
        scene.add(particlesMesh);

        // Subtle connecting lines
        const linesMaterial = new THREE.LineBasicMaterial({
            color: 0x7c3aed,
            transparent: true,
            opacity: 0.06
        });

        const lineGeometry = new THREE.BufferGeometry();
        lineGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const lineMesh = new THREE.Line(lineGeometry, linesMaterial);
        scene.add(lineMesh);

        camera.position.z = 4;

        // Interaction state
        let mouseX = 0, mouseY = 0;
        const windowHalfX = window.innerWidth / 2;
        const windowHalfY = window.innerHeight / 2;

        const onMouseMove = (event) => {
            mouseX = (event.clientX - windowHalfX);
            mouseY = (event.clientY - windowHalfY);
        };
        document.addEventListener('mousemove', onMouseMove);

        const clock = new THREE.Clock();

        const animate = () => {
            requestAnimationFrame(animate);
            const elapsedTime = clock.getElapsedTime();

            const targetX = mouseX * 0.001;
            const targetY = mouseY * 0.001;

            particlesMesh.rotation.y += 0.002;
            particlesMesh.rotation.x += 0.001;
            lineMesh.rotation.y += 0.002;
            lineMesh.rotation.x += 0.001;

            particlesMesh.rotation.y += 0.05 * (targetX - particlesMesh.rotation.y);
            particlesMesh.rotation.x += 0.05 * (targetY - particlesMesh.rotation.x);
            lineMesh.rotation.y += 0.05 * (targetX - lineMesh.rotation.y);
            lineMesh.rotation.x += 0.05 * (targetY - lineMesh.rotation.x);

            const positions = particlesMesh.geometry.attributes.position.array;
            for(let i = 0; i < particlesCount; i++) {
                const i3 = i * 3;
                positions[i3 + 1] += Math.sin(elapsedTime + positions[i3]) * 0.002;
            }
            particlesMesh.geometry.attributes.position.needsUpdate = true;

            renderer.render(scene, camera);
        };

        animate();

        window.addEventListener('resize', () => {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

    } catch (error) {
        console.error("WebGL Initialization failed:", error);
        // Fallback: Hide canvas and show a CSS gradient
        const container = document.getElementById('canvas-container');
        if (container) {
            container.style.display = 'none';
            document.body.style.background = "linear-gradient(135deg, #050508 0%, #1a1a2e 100%)";
        }
    }
};

// --- Chat Logic ---

const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');
const typingIndicator = document.getElementById('typing-indicator');
const chatContainer = document.querySelector('.chat-container');

/**
 * Appends a message to the chat UI with appropriate accessibility roles.
 */
const appendMessage = (content, role) => {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}-message`;
    msgDiv.setAttribute('role', 'article');
    msgDiv.setAttribute('aria-label', role === 'user' ? 'Your message' : 'VoteDost response');
    
    const avatar = document.createElement('div');
    avatar.setAttribute('aria-hidden', 'true');
    if (role === 'user') {
        avatar.className = 'avatar user-avatar';
        avatar.textContent = 'V';
    } else {
        avatar.className = 'avatar bot-avatar';
        avatar.textContent = '🗳️';
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'content';
    contentDiv.innerHTML = parseMarkdown(content);
    
    msgDiv.appendChild(avatar);
    msgDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(msgDiv);
    
    // Smooth entrance animation
    gsap.fromTo(msgDiv, 
        { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.4, ease: "power2.out" }
    );
    
    scrollToBottom();
};

const scrollToBottom = () => {
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 50);
};

/**
 * Sends a message to the Flask backend.
 */
const sendMessageToBackend = async (message) => {
    typingIndicator.classList.remove('hidden');
    scrollToBottom();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, history, language: selectedLanguage })
        });
        
        const data = await response.json();
        typingIndicator.classList.add('hidden');
        
        if (response.ok) {
            appendMessage(data.response, 'bot');
            history.push({ role: 'user', content: message });
            history.push({ role: 'assistant', content: data.response });
            
            // Limit history to last 10 turns to keep requests efficient
            if (history.length > 20) history = history.slice(-20);
        } else {
            appendMessage(`Error: ${data.error}`, 'bot');
        }
    } catch (error) {
        typingIndicator.classList.add('hidden');
        appendMessage('I am having trouble connecting to the server. Please try again later.', 'bot');
        console.error('Fetch error:', error);
    }
};

const handleSend = (e) => {
    if (e) e.preventDefault();
    
    const text = userInput.value.trim();
    if (!text) return;
    
    appendMessage(text, 'user');
    userInput.value = '';
    autocompleteDropdown.classList.add('hidden');
    
    sendMessageToBackend(text);
};

// Global function for suggested questions
window.sendSuggested = (text) => {
    userInput.value = text;
    handleSend();
    const chatNavItem = document.querySelector('.nav-item[data-target="panel-chat"]');
    if (chatNavItem) chatNavItem.click();
};

if (chatForm) chatForm.addEventListener('submit', handleSend);

// --- UI Controls ---

// Language Selection
const languageSelector = document.getElementById('language-selector');
if (languageSelector) {
    languageSelector.addEventListener('change', (e) => {
        selectedLanguage = e.target.value;
        userInput.placeholder = PLACEHOLDERS[selectedLanguage] || PLACEHOLDERS["English"];
    });
}

// Tab Switching
const navItems = document.querySelectorAll('.nav-item');
const panels = document.querySelectorAll('.panel');

navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = item.dataset.target;
        
        // Update navigation states
        navItems.forEach(nav => {
            const isActive = nav.dataset.target === targetId;
            nav.classList.toggle('active', isActive);
            if (isActive) {
                nav.setAttribute('aria-current', 'page');
            } else {
                nav.removeAttribute('aria-current');
            }
        });
        
        // Update panel visibility
        panels.forEach(panel => {
            const isActive = panel.id === targetId;
            panel.classList.toggle('active', isActive);
            panel.classList.toggle('hidden', !isActive);
        });
        
        // Scroll or Animate content
        if (targetId === 'panel-chat') {
            scrollToBottom();
        } else if (targetId === 'panel-guide') {
            gsap.fromTo('.guide-card', 
                { y: 30, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: "power2.out" }
            );
        } else if (targetId === 'panel-timeline') {
            gsap.fromTo('.timeline-step', 
                { x: 50, opacity: 0 },
                { x: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: "power2.out" }
            );
        } else if (targetId === 'panel-faqs') {
            gsap.fromTo('.faq-item', 
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.4, stagger: 0.05, ease: "power2.out" }
            );
        }
    });
});

// FAQ Accordion
const faqItems = document.querySelectorAll('.faq-item');
faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    if (!questionBtn) return;

    questionBtn.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        // Close others
        faqItems.forEach(faq => {
            faq.classList.remove('active');
            const btn = faq.querySelector('.faq-question');
            btn.setAttribute('aria-expanded', 'false');
            faq.querySelector('.faq-icon').textContent = '+';
        });
        
        // Open current if it was closed
        if (!isActive) {
            item.classList.add('active');
            questionBtn.setAttribute('aria-expanded', 'true');
            item.querySelector('.faq-icon').textContent = '-';
        }
    });
});

// --- Autocomplete Suggestions ---

const autocompleteDropdown = document.getElementById('autocomplete-dropdown');
const PREDEFINED_SUGGESTIONS = [
    "How do I register to vote?",
    "What is EVM and how does it work?",
    "What is Model Code of Conduct?",
    "Who can contest in elections?",
    "What is NOTA?",
    "How to check my name in voter list?",
    "What ID do I need for voting?",
    "What is the difference between Lok Sabha and Vidhan Sabha?",
    "What is the minimum age to vote?",
    "What is VVPAT?",
    "How to report election violation?",
    "Can NRI vote in Indian elections?"
];

/**
 * Renders autocomplete options based on current input.
 */
const updateAutocomplete = debounce((value) => {
    autocompleteDropdown.innerHTML = '';
    autocompleteIndex = -1;
    
    if (!value) {
        autocompleteDropdown.classList.add('hidden');
        return;
    }
    
    const matches = PREDEFINED_SUGGESTIONS
        .filter(s => s.toLowerCase().includes(value.toLowerCase()))
        .slice(0, 5);
    
    if (matches.length === 0) {
        autocompleteDropdown.classList.add('hidden');
        return;
    }
    
    matches.forEach((match, index) => {
        const div = document.createElement('div');
        div.className = 'autocomplete-item';
        div.setAttribute('role', 'option');
        div.id = `autocomplete-opt-${index}`;
        
        // Highlight matching text
        const regex = new RegExp(`(${value})`, "gi");
        div.innerHTML = match.replace(regex, `<span class="autocomplete-match">$1</span>`);
        
        div.addEventListener('click', () => {
            userInput.value = match;
            autocompleteDropdown.classList.add('hidden');
            userInput.focus();
        });
        
        autocompleteDropdown.appendChild(div);
    });
    
    autocompleteDropdown.classList.remove('hidden');
}, 150);

userInput.addEventListener('input', (e) => updateAutocomplete(e.target.value));

/**
 * Handles keyboard navigation for autocomplete and global shortcuts.
 */
userInput.addEventListener('keydown', (e) => {
    const items = autocompleteDropdown.querySelectorAll('.autocomplete-item');
    
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (items.length > 0) {
            autocompleteIndex = (autocompleteIndex + 1) % items.length;
            highlightAutocomplete(items);
        }
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (items.length > 0) {
            autocompleteIndex = (autocompleteIndex - 1 + items.length) % items.length;
            highlightAutocomplete(items);
        }
    } else if (e.key === 'Enter') {
        if (autocompleteIndex > -1 && items[autocompleteIndex]) {
            e.preventDefault();
            userInput.value = items[autocompleteIndex].textContent;
            autocompleteDropdown.classList.add('hidden');
            handleSend();
        }
    } else if (e.key === 'Escape') {
        autocompleteDropdown.classList.add('hidden');
    }
});

const highlightAutocomplete = (items) => {
    items.forEach((item, index) => {
        const isSelected = index === autocompleteIndex;
        item.classList.toggle('selected', isSelected);
        if (isSelected) {
            item.scrollIntoView({ block: 'nearest' });
            userInput.setAttribute('aria-activedescendant', item.id);
        }
    });
};

// Close dropdown on click outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.input-area')) {
        autocompleteDropdown.classList.add('hidden');
    }
});

// --- Initialization ---

window.addEventListener('DOMContentLoaded', () => {
    initThreeJS();
    
    // Initial animation for welcome message
    gsap.to('.bot-message', {
        y: 0,
        opacity: 1,
        duration: 0.6,
        ease: "back.out(1.7)"
    });
});
