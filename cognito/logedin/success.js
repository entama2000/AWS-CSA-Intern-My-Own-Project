const chatBody = document.getElementById('chat-body');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const loadingAnimation = document.getElementById('loadingAnimation');

let conversationHistory = [];

sendButton.addEventListener('click', sendMessage);

function sendMessage() {
  const message = messageInput.value.trim();
  if (message) {
    addMessageToChat('You', message);
    conversationHistory.push({ role: 'user', content: message });
    messageInput.value = '';
    getResponse(message);
  }
}

function addMessageToChat(sender, message) {
  const messageElement = document.createElement('div');
  messageElement.classList.add('message');
  messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
  chatBody.appendChild(messageElement);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
}

function getResponse(message) {
  const token = getCookie('token');
  if (token) {
    const thinkingAnimation = document.createElement('div');
    thinkingAnimation.classList.add('message', 'ai', 'thinking-animation');
    thinkingAnimation.innerHTML = `
      <div class="loader"></div>
      <span>entama is thinking...</span>
    `;
    chatBody.appendChild(thinkingAnimation);
    chatBody.scrollTop = chatBody.scrollHeight;

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://rqe0g3nujg.execute-api.us-east-1.amazonaws.com/dev/bedrock', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    const data = { IdToken: token, prompt: JSON.stringify(conversationHistory) };

    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        const response = JSON.parse(xhr.responseText);
        const statusCode = response.statusCode;

        if (statusCode === 200) {
          const body = JSON.parse(response.body);
          const answer = body.answer;
          chatBody.removeChild(thinkingAnimation);
          addMessageToChat('ENTAMA AI', answer);
          conversationHistory.push({ role: 'assistant', content: answer });
        } else {
          const body = JSON.parse(response.body);
          addMessageToChat('Error', body.message);
          chatBody.removeChild(thinkingAnimation);
        }
      }
    };

    xhr.send(JSON.stringify(data));
  } else {
    window.location.href = '../index.html';
  }
}

// reset chat
const resetButton = document.getElementById('reset-button');

resetButton.addEventListener('click', resetChat);

function resetChat() {
  chatBody.innerHTML = '';
  conversationHistory = [];
}