function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;

    // Add user message to UI
    appendMessage(message, 'user');
    input.value = '';

    // Show loading indicator
    const loadingId = addLoadingIndicator();

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        removeLoadingIndicator(loadingId);
        appendMessage(data.response, 'bot');
    })
    .catch(error => {
        console.error('Error:', error);
        removeLoadingIndicator(loadingId);
        appendMessage("I'm sorry, I'm having trouble connecting to the server. Please check if the backend is running.", 'bot');
    });
}

function appendMessage(text, sender) {
    const chatWindow = document.getElementById('chat-window');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-message`;
    
    // Convert text to markdown HTML if bot, otherwise simple newline replace
    let formattedText = text;
    if (sender === 'bot') {
        formattedText = marked.parse(text);
    } else {
        formattedText = text.replace(/\n/g, '<br>');
    }
                             
    msgDiv.innerHTML = formattedText;
    chatWindow.appendChild(msgDiv);
    
    // Auto scroll to bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function addLoadingIndicator() {
    const chatWindow = document.getElementById('chat-window');
    const loadingDiv = document.createElement('div');
    const id = 'loading-' + Date.now();
    loadingDiv.id = id;
    loadingDiv.className = 'message bot-message loading';
    loadingDiv.innerText = 'Typing...';
    chatWindow.appendChild(loadingDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return id;
}

function removeLoadingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) indicator.remove();
}
