// /frontend/public/js/main.js
const form = document.getElementById('input-form');
const input = document.getElementById('message-input');
const messageContainer = document.getElementById('message-container');

const API_URL = 'http://localhost:8000/chat';

let conversationHistory = [];
let taskIsComplete = true; // Start with true to clear history for the very first message
let currentLanguage = null; // <-- Add a variable for the language state

// The initial welcome message is rendered by EJS, so we don't need JS to add it.

function addMessage(sender, text) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);
    messageElement.textContent = text;
    messageContainer.appendChild(messageElement);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = input.value.trim();
    if (!userMessage) return;

    if (taskIsComplete) {
        conversationHistory = [];
        currentLanguage = null; // Clear language on new topic
        taskIsComplete = false;
    }

    addMessage('user', userMessage);
    conversationHistory.push({ role: 'user', content: userMessage });
    
    input.value = '';
    input.disabled = true;
    
    addMessage('bot', 'Orion is typing...');

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: userMessage,
                history: conversationHistory.slice(0, -1),
                language: currentLanguage // <-- Send the current language
            }),
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const data = await response.json();
        const botResponse = data.response;
        
        // --- Remember the state for the next turn ---
        taskIsComplete = data.task_complete;
        currentLanguage = data.language; // <-- Store the language from the response

        messageContainer.removeChild(messageContainer.lastChild);
        addMessage('bot', botResponse);
        conversationHistory.push({ role: 'assistant', content: botResponse });

    } catch (error) {
        messageContainer.removeChild(messageContainer.lastChild);
        addMessage('bot', 'Sorry, something went wrong. Please try again.');
        console.error('Fetch error:', error);
    } finally {
        input.disabled = false;
        input.focus();
    }
});