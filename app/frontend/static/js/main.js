// app/static/js/main.js
let sessionId = null;
let chatMode = 'both';

// Read mode from URL
function getModeFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('mode') || 'both';
}

function setHeaderForMode(mode) {
    const header = document.getElementById('chat-header-title');
    if (!header) return;
    if (mode === 'diet') header.innerHTML = '🥗 FitForge Diet Coach';
    else if (mode === 'exercise') header.innerHTML = '🏋️ FitForge Exercise Coach';
    else header.innerHTML = '🤖 FitForge AI Coach';
}

const MOTIVATION_TIPS = [
    "💪 Every rep gets you closer to your goal!",
    "🥦 Fuel your body, fuel your dreams!",
    "🏃‍♂️ Progress, not perfection!",
    "🔥 Consistency beats intensity!",
    "🌟 You are stronger than you think!",
    "🎯 Small steps every day lead to big results!",
    "😎 Believe in yourself and all that you are!",
    "🏆 Celebrate every victory, no matter how small!"
];

function showRandomMotivation() {
    const banner = document.getElementById('motivation-banner');
    if (banner) {
        const tip = MOTIVATION_TIPS[Math.floor(Math.random() * MOTIVATION_TIPS.length)];
        banner.textContent = tip;
    }
}

function appendMessage(text, sender) {
    const chatWindow = document.getElementById('chat-window');
    const row = document.createElement('div');
    row.className = 'chat-bubble-row ' + (sender === 'user' ? 'user-row' : 'bot-row');
    row.style.opacity = 0;
    setTimeout(() => { row.style.opacity = 1; }, 10);

    // Avatar
    const avatar = document.createElement('div');
    avatar.className = 'avatar ' + (sender === 'user' ? 'user-avatar' : 'bot-avatar');
    avatar.innerHTML = sender === 'user' ? '🧑' : (chatMode === 'diet' ? '🥗' : (chatMode === 'exercise' ? '🏋️' : '🤖'));

    // Bubble
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble ' + (sender === 'user' ? 'user-bubble' : 'bot-bubble');
    if (sender === 'bot') {
        bubble.innerHTML = `<div class="markdown-content">${marked.parse(text)}</div>`;
    } else {
        bubble.textContent = text;
    }

    if (sender === 'user') {
        row.appendChild(bubble);
        row.appendChild(avatar);
    } else {
        row.appendChild(avatar);
        row.appendChild(bubble);
    }
    chatWindow.appendChild(row);
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Confetti if plan generated
    if (sender === 'bot' && (text.includes('Workout Plan') || text.includes('Diet Plan'))) {
        launchConfetti();
    }
}

function setBotLoading(isLoading) {
    let loadingRow = document.getElementById('bot-loading-row');
    if (isLoading) {
        if (!loadingRow) {
            loadingRow = document.createElement('div');
            loadingRow.className = 'chat-bubble-row bot-row';
            loadingRow.id = 'bot-loading-row';
            const avatar = document.createElement('div');
            avatar.className = 'avatar bot-avatar';
            avatar.innerHTML = (chatMode === 'diet' ? '🥗' : (chatMode === 'exercise' ? '🏋️' : '🤖'));
            const bubble = document.createElement('div');
            bubble.className = 'chat-bubble bot-bubble';
            bubble.innerHTML = '<span class="bot-loading-dot"></span><span class="bot-loading-dot"></span><span class="bot-loading-dot"></span>';
            loadingRow.appendChild(avatar);
            loadingRow.appendChild(bubble);
            document.getElementById('chat-window').appendChild(loadingRow);
            document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;
        }
    } else {
        if (loadingRow) loadingRow.remove();
    }
}

// Confetti animation
function launchConfetti() {
    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = window.innerWidth;
    const H = window.innerHeight;
    canvas.width = W;
    canvas.height = H;
    let particles = [];
    for (let i = 0; i < 120; i++) {
        particles.push({
            x: Math.random() * W,
            y: Math.random() * -H,
            r: Math.random() * 6 + 4,
            d: Math.random() * 100 + 10,
            color: `hsl(${Math.random()*360},70%,60%)`,
            tilt: Math.random() * 10 - 10
        });
    }
    let angle = 0;
    let frame = 0;
    function draw() {
        ctx.clearRect(0, 0, W, H);
        angle += 0.01;
        for (let i = 0; i < particles.length; i++) {
            let p = particles[i];
            p.y += (Math.cos(angle + p.d) + 3 + p.r/2) / 2;
            p.x += Math.sin(angle) * 2;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI*2, false);
            ctx.fillStyle = p.color;
            ctx.fill();
        }
        frame++;
        if (frame < 90) {
            requestAnimationFrame(draw);
        } else {
            ctx.clearRect(0, 0, W, H);
        }
    }
    draw();
}

document.addEventListener('DOMContentLoaded', () => {
    chatMode = getModeFromURL();
    setHeaderForMode(chatMode);
    sessionId = null; // Reset session on mode change
    showRandomMotivation();
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');

    chatForm && chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;
        appendMessage(message, 'user');
        chatInput.value = '';
        setBotLoading(true);
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, session_id: sessionId, mode: chatMode }),
            });
            if (!response.ok) {
                throw new Error('Server error');
            }
            const data = await response.json();
            sessionId = data.session_id;
            setBotLoading(false);
            appendMessage(data.response, 'bot');
        } catch (err) {
            setBotLoading(false);
            appendMessage('Sorry, there was an error. Please try again.', 'bot');
        }
    });

    // Greet the user on load
    if (chatMode === 'diet') {
        appendMessage('Hi! I am your FitForge Diet Coach. Ask me anything about nutrition, meal plans, calories, or healthy eating!', 'bot');
    } else if (chatMode === 'exercise') {
        appendMessage('Hi! I am your FitForge Exercise Coach. Ask me anything about workouts, routines, sets, reps, or exercise form!', 'bot');
    } else {
        appendMessage('Hi! I am your FitForge AI coach. Ask me anything about fitness, nutrition, workouts, or logging your progress!', 'bot');
    }
}); 