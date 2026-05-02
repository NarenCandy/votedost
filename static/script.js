// --- Three.js Particle Background ---
const initThreeJS = () => {
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    // Particles
    const particlesGeometry = new THREE.BufferGeometry();
    const particlesCount = 150;
    
    const posArray = new Float32Array(particlesCount * 3);
    
    for(let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 10;
    }
    
    particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    
    const material = new THREE.PointsMaterial({
        size: 0.02,
        color: 0x8b5cf6,
        transparent: true,
        opacity: 0.8
    });
    
    const particlesMesh = new THREE.Points(particlesGeometry, material);
    scene.add(particlesMesh);

    // Lines connecting particles
    const linesMaterial = new THREE.LineBasicMaterial({
        color: 0x3b82f6,
        transparent: true,
        opacity: 0.1
    });

    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
    const lineMesh = new THREE.Line(lineGeometry, linesMaterial);
    scene.add(lineMesh);

    camera.position.z = 3;

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

        particlesMesh.rotation.y += 0.002;
        particlesMesh.rotation.x += 0.001;
        
        lineMesh.rotation.y += 0.002;
        lineMesh.rotation.x += 0.001;

        // Smooth mouse movement
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
    avatar.className = 'avatar';
    avatar.textContent = role === 'user' ? '👤' : '🤖';
    
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

const sendMessageToBackend = async (message) => {
    showTypingIndicator();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message, history })
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
    
    sendMessageToBackend(text);
};

window.sendSuggested = (text) => {
    userInput.value = text;
    handleSend();
};

chatForm.addEventListener('submit', handleSend);
