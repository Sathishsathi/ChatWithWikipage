// function sendMessage() {
//     var userInput = document.getElementById("userInput");
//     var userMessage = userInput.value;
  
//     if (userMessage.trim() === "") {
//       return;
//     }
  
//     var chatBox = document.getElementById("chatBox");
  
//     // Display user message
//     var userDiv = document.createElement("div");
//     userDiv.textContent = userMessage;
//     userDiv.classList.add("chat-message", "user-message");
//     chatBox.appendChild(userDiv);
  
//     // Clear user input
//     userInput.value = "";
  
//     // Simulate bot response after a short delay (could be an actual API call)
//     setTimeout(function() {
//       var botMessage = getBotResponse(userMessage);
  
//       // Display bot message
//       var botDiv = document.createElement("div");
//       botDiv.textContent = botMessage;
//       botDiv.classList.add("chat-message", "bot-message");
//       chatBox.appendChild(botDiv);
  
//       // Scroll to bottom of chat box
//       chatBox.scrollTop = chatBox.scrollHeight;
//     }, 500); // Simulate delay for bot typing effect
//   }
  
//   function getBotResponse(message) {
//     // Simple example: Echo the user message
//     return "You said: " + message;
//   }
  

// Use these variables in your server-side logic (e.g., Express routes)
function fetchBotResponse(userMessage) {
  // Replace this URL with your backend endpoint or a chatbot API
  var apiUrl = 'http://127.0.0.1:3000/post';

  return fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question: userMessage }),
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  });
}
function sendMessage() {// function for a get user input &&  send a message from a user 
  var userInput = document.getElementById("userInput");
  var userMessage = userInput.value.trim();

  if (userMessage === "") {
    return;
  }

  var chatBox = document.getElementById("chatBox");

  // Display user message
  var userDiv = document.createElement("div");
  userDiv.textContent = userMessage;
  userDiv.classList.add("chat-message", "user-message", "text-right");
  chatBox.appendChild(userDiv);

  // Clear user input
  userInput.value = "";

  // Fetch API to send user message and get bot response
  fetchBotResponse(userMessage)
    .then(response => {
      // Display bot message
      var botMessage = response.message;
      var botDiv = document.createElement("div");
      botDiv.textContent = botMessage;
      botDiv.classList.add("chat-message", "bot-message");
      chatBox.appendChild(botDiv);

      // Scroll to bottom of chat box
      chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
      console.error('Error fetching bot response:', error);
    });
}