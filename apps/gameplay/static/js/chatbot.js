// CHATBOT FUNCTIONALITY
const chatbotInput = document.getElementById('chatbotInput');
const chatbotSend = document.getElementById('chatbotSend');
const chatbotMessages = document.getElementById('chatbotMessages');

// Send message
function sendMessage() {
    const message = chatbotInput.value.trim();
    if (!message) return;

    // Mostrar mensaje del usuario
    addMessage(message, 'user');
    chatbotInput.value = '';

    // Mostrar "escribiendo..."
    showTypingIndicator();

    fetch('/gameplay/chatbot/api/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        credentials: 'same-origin',  // 🔥 ESTO ES LO IMPORTANTE
        body: JSON.stringify({
            mensaje: message
        })
    })

    .then(response => response.json())
    .then(data => {
    hideTypingIndicator();
    addMessage(data.respuesta || data.error || '⚠️ Respuesta inválida', 'bot');
    })
    .catch(error => {
        hideTypingIndicator();
        addMessage('❌ Error al comunicar con el servidor', 'bot');
        console.error(error);
    });
}


chatbotSend.addEventListener('click', sendMessage);
chatbotInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Suggestion chips
document.querySelectorAll('.suggestion-chip').forEach(chip => {
    chip.addEventListener('click', () => {
        const message = chip.getAttribute('data-message');
        chatbotInput.value = message;
        sendMessage();
    });
});

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const now = new Date();
    const time = now.toLocaleTimeString('es-EC', { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.innerHTML = `
        <div class="message-content">
            ${text}
            <div class="message-time">${time}</div>
        </div>
    `;
    
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

// Typing indicator
let typingIndicator = null;

function showTypingIndicator() {
    typingIndicator = document.createElement('div');
    typingIndicator.className = 'message bot';
    typingIndicator.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    chatbotMessages.appendChild(typingIndicator);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
}

function hideTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.remove();
        typingIndicator = null;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ==========================================
// VOICE RECOGNITION IMPLEMENTATION
// ==========================================

const micBtn = document.getElementById('chatbotMic');

// Verificar soporte del navegador
if ('webkitSpeechRecognition' in window) {
    const recognition = new webkitSpeechRecognition();
    
    recognition.continuous = false; // Se detiene al dejar de hablar
    recognition.lang = 'es-ES';     // Idioma Español
    recognition.interimResults = false;

    // Click en el micrófono
    micBtn.addEventListener('click', function() {
        if (micBtn.classList.contains('listening')) {
            recognition.stop();
        } else {
            recognition.start();
        }
    });

    // Inicio de la escucha
    recognition.onstart = function() {
        micBtn.classList.add('listening');
        chatbotInput.placeholder = "Escuchando...";
        micBtn.title = "Escuchando... clic para detener";
    };

    // Fin de la escucha (por silencio o manual)
    recognition.onend = function() {
        micBtn.classList.remove('listening');
        chatbotInput.placeholder = "Escribe tu mensaje...";
        micBtn.title = "Hablar";
        chatbotInput.focus();
    };

    // Resultado obtenido
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        
        // 1. Insertamos el texto en el input
        chatbotInput.value = transcript;
        
        // 2. Opcional: Auto-envío (actualmente desactivado para que el usuario verifique)
        // sendMessage(); 
    };

    recognition.onerror = function(event) {
        console.error("Error de reconocimiento de voz:", event.error);
        micBtn.classList.remove('listening');
        chatbotInput.placeholder = "Error al escuchar. Intenta escribir.";
    };

} else {
    // Si el navegador no soporta la API (ej. Firefox desktop sin flags), ocultamos el botón
    console.warn("Web Speech API no soportada en este navegador.");
    micBtn.style.display = 'none';
}