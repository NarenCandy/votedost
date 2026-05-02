// --- Three.js Particle Background ---
const initThreeJS = () => {
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
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
        // Position
        posArray[i * 3] = (Math.random() - 0.5) * 12;
        posArray[i * 3 + 1] = (Math.random() - 0.5) * 12;
        posArray[i * 3 + 2] = (Math.random() - 0.5) * 8;
        
        // Color mix: 70% purple, 30% gold
        const isGold = Math.random() > 0.7;
        const color = isGold ? colorGold : colorPurple;
        
        colorsArray[i * 3] = color.r;
        colorsArray[i * 3 + 1] = color.g;
        colorsArray[i * 3 + 2] = color.b;
        
        // Size: vary between 0.01 and 0.04
        sizesArray[i] = Math.random() * 0.03 + 0.01;
    }
    
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    particlesGeometry.setAttribute('customColor', new THREE.BufferAttribute(colorsArray, 3));
    particlesGeometry.setAttribute('size', new THREE.BufferAttribute(sizesArray, 1));
    
    // Custom Shader for Particles to support variable sizes and colors
    const vertexShader = `
        attribute float size;
        attribute vec3 customColor;
        varying vec3 vColor;
        void main() {
            vColor = customColor;
            vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
            // Scale size based on distance
            gl_PointSize = size * (300.0 / -mvPosition.z);
            gl_Position = projectionMatrix * mvPosition;
        }
    `;
    
    const fragmentShader = `
        varying vec3 vColor;
        void main() {
            // Make particles circular
            float r = distance(gl_PointCoord, vec2(0.5));
            if (r > 0.5) discard;
            gl_FragColor = vec4(vColor, 0.8);
        }
    `;

    const material = new THREE.ShaderMaterial({
        uniforms: {},
        vertexShader: vertexShader,
        fragmentShader: fragmentShader,
        transparent: true,
        depthWrite: false
    });
    
    const particlesMesh = new THREE.Points(particlesGeometry, material);
    scene.add(particlesMesh);

    // Lines connecting particles
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

    // Mouse interaction
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const windowHalfX = window.innerWidth / 2;
    const windowHalfY = window.innerHeight / 2;

    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX - windowHalfX);
        mouseY = (event.clientY - windowHalfY);
    });

    // Animation Loop
    const clock = new THREE.Clock();

    const animate = () => {
        requestAnimationFrame(animate);
        const elapsedTime = clock.getElapsedTime();

        targetX = mouseX * 0.001;
        targetY = mouseY * 0.001;

        // Faster subtle rotation as requested
        particlesMesh.rotation.y += 0.003;
        particlesMesh.rotation.x += 0.0015;
        
        lineMesh.rotation.y += 0.003;
        lineMesh.rotation.x += 0.0015;

        // Smooth mouse movement parallax
        particlesMesh.rotation.y += 0.05 * (targetX - particlesMesh.rotation.y);
        particlesMesh.rotation.x += 0.05 * (targetY - particlesMesh.rotation.x);
        
        lineMesh.rotation.y += 0.05 * (targetX - lineMesh.rotation.y);
        lineMesh.rotation.x += 0.05 * (targetY - lineMesh.rotation.x);

        // Make points bob slightly
        const positions = particlesMesh.geometry.attributes.position.array;
        for(let i = 0; i < particlesCount; i++) {
            const i3 = i * 3;
            positions[i3 + 1] += Math.sin(elapsedTime + positions[i3]) * 0.002;
        }
        particlesMesh.geometry.attributes.position.needsUpdate = true;

        renderer.render(scene, camera);
    };

    animate();

    // Handle Resize
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
};

initThreeJS();

// --- Chat Functionality ---
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatMessages = document.getElementById('chat-messages');
const typingIndicator = document.getElementById('typing-indicator');
const chatContainer = document.querySelector('.chat-container');

// Chat history to send to backend
let history = [];

// Animate initial bot message
gsap.to('.bot-message', {
    y: 0,
    opacity: 1,
    duration: 0.5,
    ease: "back.out(1.7)"
});

// Basic Markdown Parser (handles bold and newlines)
const parseMarkdown = (text) => {
    let parsed = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    parsed = parsed.replace(/\*(.*?)\*/g, '<em>$1</em>');
    parsed = parsed.replace(/\n/g, '<br>');
    return parsed;
};

const appendMessage = (content, role) => {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}-message`;
    
    const avatar = document.createElement('div');
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
    
    // Insert message before typing indicator
    chatMessages.appendChild(msgDiv);
    
    // Animate new message
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

const showTypingIndicator = () => {
    typingIndicator.classList.remove('hidden');
    scrollToBottom();
};

const hideTypingIndicator = () => {
    typingIndicator.classList.add('hidden');
};

let selectedLanguage = "English";

const sendMessageToBackend = async (message) => {
    showTypingIndicator();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message, history, language: selectedLanguage })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        
        if (response.ok) {
            appendMessage(data.response, 'bot');
            // update history
            history.push({ role: 'user', content: message });
            history.push({ role: 'assistant', content: data.response });
        } else {
            appendMessage(`Error: ${data.error}`, 'bot');
        }
    } catch (error) {
        hideTypingIndicator();
        appendMessage('Sorry, I am having trouble connecting to the server right now.', 'bot');
        console.error('Error:', error);
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

window.sendSuggested = (text) => {
    userInput.value = text;
    handleSend();
    // Switch to chat panel if triggered from sidebar quick questions
    const chatNavItem = document.querySelector('.nav-item[data-target="panel-chat"]');
    if (chatNavItem) chatNavItem.click();
};

chatForm.addEventListener('submit', handleSend);

// --- Language Selector ---
const languageSelector = document.getElementById('language-selector');
const placeholders = {
    "English": "Ask about elections...",
    "Hindi": "चुनाव के बारे में पूछें...",
    "Tamil": "தேர்தல் பற்றி கேளுங்கள்...",
    "Telugu": "ఎన్నికల గురించి అడగండి...",
    "Kannada": "ಚುನಾವಣೆಯ ಬಗ್ಗೆ ಕೇಳಿ...",
    "Bengali": "নির্বাচন সম্পর্কে জিজ্ঞাসা করুন...",
    "Marathi": "निवडणुकीबद्दल विचारा..."
};

languageSelector.addEventListener('change', (e) => {
    selectedLanguage = e.target.value;
    userInput.placeholder = placeholders[selectedLanguage] || placeholders["English"];
});

// --- Tab Switching Logic ---
const navItems = document.querySelectorAll('.nav-item');
const panels = document.querySelectorAll('.panel');

navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Remove active from all nav items and add to matched ones
        navItems.forEach(nav => {
            if(nav.dataset.target === item.dataset.target) {
                nav.classList.add('active');
            } else {
                nav.classList.remove('active');
            }
        });
        
        // Hide all panels
        panels.forEach(panel => {
            panel.classList.remove('active');
            panel.classList.add('hidden');
        });
        
        // Show target panel
        const targetId = item.dataset.target;
        const targetPanel = document.getElementById(targetId);
        targetPanel.classList.remove('hidden');
        targetPanel.classList.add('active');
        
        // Animate incoming content
        if (targetId === 'panel-guide') {
            gsap.fromTo('.guide-card', 
                { y: 30, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: "power2.out" }
            );
        } else if (targetId === 'panel-timeline') {
            gsap.fromTo('.timeline-step', 
                { x: 50, opacity: 0 },
                { x: 0, opacity: 1, duration: 0.5, stagger: 0.15, ease: "power2.out" }
            );
        } else if (targetId === 'panel-faqs') {
            gsap.fromTo('.faq-item', 
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.4, stagger: 0.1, ease: "power2.out" }
            );
        } else if (targetId === 'panel-chat') {
            scrollToBottom();
        }
    });
});

// --- FAQ Accordion Logic ---
const faqItems = document.querySelectorAll('.faq-item');
faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        // Close all
        faqItems.forEach(faq => faq.classList.remove('active'));
        faqItems.forEach(faq => faq.querySelector('.faq-icon').textContent = '+');
        
        // Open clicked if it wasn't active
        if (!isActive) {
            item.classList.add('active');
            item.querySelector('.faq-icon').textContent = '-';
        }
    });
});

// --- Autocomplete Suggestions ---
const autocompleteDropdown = document.getElementById('autocomplete-dropdown');
const predefinedSuggestions = [
    "How do I register to vote?",
    "What is EVM and how does it work?",
    "What is Model Code of Conduct?",
    "Who can contest in elections?",
    "What is NOTA?",
    "How to check my name in voter list?",
    "What ID do I need for voting?",
    "What is the difference between Lok Sabha and Vidhan Sabha?",
    "What happens if someone bribes me for vote?",
    "What is VVPAT?",
    "How to report election violation?",
    "What is the minimum age to vote?"
];

userInput.addEventListener('input', (e) => {
    const value = e.target.value.toLowerCase();
    autocompleteDropdown.innerHTML = '';
    
    if (!value) {
        autocompleteDropdown.classList.add('hidden');
        return;
    }
    
    const matches = predefinedSuggestions.filter(s => s.toLowerCase().includes(value)).slice(0, 4);
    
    if (matches.length === 0) {
        autocompleteDropdown.classList.add('hidden');
        return;
    }
    
    matches.forEach(match => {
        const div = document.createElement('div');
        div.className = 'autocomplete-item';
        
        // Highlight match
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
});

// Hide autocomplete on Escape or click outside
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        autocompleteDropdown.classList.add('hidden');
    }
});
document.addEventListener('click', (e) => {
    if (!e.target.closest('.input-area')) {
        autocompleteDropdown.classList.add('hidden');
    }
});
