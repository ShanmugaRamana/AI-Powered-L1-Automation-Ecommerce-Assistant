// /frontend/public/js/main.js
const form = document.getElementById('input-form');
const input = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const messageContainer = document.getElementById('message-container');
const chatContainer = document.getElementById('chat-container'); // Get the main container

// Get buttons for both modes
const textMicButton = document.getElementById('mic-btn'); 
const voiceMicButton = document.getElementById('voice-mic-btn');

const API_URL = 'http://localhost:8000/chat';

let conversationHistory = [];
let taskIsComplete = true;
let currentLanguage = null;

// --- Speech Recognition Setup ---
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;

if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'en-US'; // Change to 'ta-IN' for Tamil, 'hi-IN' for Hindi
    recognition.interimResults = false;

    // A single function to start voice recognition
    const startVoiceRecognition = () => {
        chatContainer.classList.add('voice-mode-active'); // Switch to voice UI
        voiceMicButton.classList.add('recording');
        recognition.start();
    };

    // Attach the event to both mic buttons
    textMicButton.addEventListener('click', startVoiceRecognition);
    voiceMicButton.addEventListener('click', startVoiceRecognition);

    recognition.onresult = (event) => {
        const spokenText = event.results[0][0].transcript;
        input.value = spokenText;
        form.requestSubmit(sendButton); // Auto-submit
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        // Switch back to text mode on error
        chatContainer.classList.remove('voice-mode-active');
        voiceMicButton.classList.remove('recording');
    };
    
    recognition.onend = () => {
        // Switch back to text mode when listening ends
        chatContainer.classList.remove('voice-mode-active');
        voiceMicButton.classList.remove('recording');
    };

} else {
    console.log("Speech Recognition not supported.");
    textMicButton.style.display = 'none';
}


function speak(text) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}

function addMessage(sender, text) {
    // This function remains the same
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    const textElement = document.createElement('span');
    textElement.classList.add('message-text');
    if (sender === 'bot') {
        textElement.innerHTML = marked.parse(text);
        const copyButton = document.createElement('button');
        copyButton.classList.add('copy-btn');
        const copyIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;
        const checkIcon = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
        copyButton.innerHTML = copyIcon;
        copyButton.addEventListener('click', () => {
            navigator.clipboard.writeText(text);
            copyButton.innerHTML = checkIcon;
            setTimeout(() => { copyButton.innerHTML = copyIcon; }, 1500);
        });
        messageElement.appendChild(copyButton);
    } else {
        textElement.textContent = text;
    }
    const timeElement = document.createElement('span');
    timeElement.classList.add('timestamp');
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    timeElement.textContent = time;
    messageElement.appendChild(textElement);
    messageElement.appendChild(timeElement);
    messageContainer.appendChild(messageElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}


form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = input.value.trim();
    if (!userMessage) return;

    // Logic for resetting history remains the same
    if (taskIsComplete) {
        conversationHistory = [];
        currentLanguage = null;
    }

    addMessage('user', userMessage);
    conversationHistory.push({ role: 'user', content: userMessage });
    
    input.value = '';
    input.disabled = true;
    
    showTypingIndicator();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', },
            body: JSON.stringify({
                message: userMessage,
                history: conversationHistory.slice(0, -1),
                language: currentLanguage
            }),
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        
        taskIsComplete = data.task_complete;
        currentLanguage = data.language;

        hideTypingIndicator();
        addMessage('bot', data.response); // Always add text reply
        conversationHistory.push({ role: 'assistant', content: data.response });
        
        // Always speak the response now
        speak(data.response);

    } catch (error) {
        hideTypingIndicator();
        const errorMsg = 'Sorry, something went wrong. Please try again.';
        addMessage('bot', errorMsg);
        speak(errorMsg); // Also speak errors
        console.error('Fetch error:', error);
    } finally {
        input.disabled = false;
        input.focus();
    }
});

// Helper functions show/hide typing indicator remain the same
function showTypingIndicator() {
    const indicatorElement = document.createElement('div');
    indicatorElement.classList.add('typing-indicator');
    indicatorElement.innerHTML = '<span></span><span></span><span></span>';
    messageContainer.appendChild(indicatorElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

function hideTypingIndicator() {
    const indicatorElement = document.querySelector('.typing-indicator');
    if (indicatorElement) {
        messageContainer.removeChild(indicatorElement);
    }
}