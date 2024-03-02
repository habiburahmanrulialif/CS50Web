
// Function to initialize WebSocket connection
function initializeWebSocket(groupName) {
    var chatSocket = new WebSocket(
        'ws://' + window.location.host +
        '/ws/group/' + groupName + '/');

    chatSocket.onmessage = function (e) {
        var data = JSON.parse(e.data);
        var messageContent = data.message;
        var isCurrentUser = (data.sender === currentUser); // Assuming currentUser is defined globally
        appendMessage(messageContent, isCurrentUser);
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    return chatSocket;
}

// Function to send message
function sendMessage(chatSocket, message) {
    chatSocket.send(JSON.stringify({
        'message': message
    }));
}

// Function to append message to message-data container
function appendMessage(messageContent, isCurrentUser) {
    var messageContainer = document.getElementById('message-data');
    var messageElement = document.createElement('div');
    messageElement.textContent = messageContent;

    if (isCurrentUser) {
        messageElement.classList.add('message-list-owner');
    } else {
        messageElement.classList.add('message-list-not-owner');
    }

    messageContainer.appendChild(messageElement);
}

// Function to handle form submission
function handleFormSubmit(chatSocket, groupName) {
    document.getElementById('message-form-form').addEventListener('submit', function (e) {
        e.preventDefault();
        var messageInput = document.getElementById('message-form-text');
        var message = messageInput.value.trim();
        if (message !== '') {
            sendMessage(chatSocket, message);
            messageInput.value = '';
        }
    });
}

// Main function to initialize chat functionality
function initChat(groupName) {
    var chatSocket = initializeWebSocket(groupName);
    handleFormSubmit(chatSocket, groupName);
}

// Call initChat function with the group name
initChat(groupName);
