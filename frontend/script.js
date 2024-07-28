
// Set the cookie
// document.cookie = `user_name=${response?.cookie}`;

// Function to get the value of a specific cookie
function getCookieValue(name) {
    let cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        let [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

// Use these variables in your server-side logic (e.g., Express routes)
function fetchBotResponse(userMessage) {
  let userName = getCookieValue('session_id');
  let query = "whare in the place"
 // var apiUrl = `http://127.0.0.1:3000/${userMessage}/${query}`;
 const apiUrl=`http://127.0.0.1:3000/${userMessage}/${query}`
  console.log(userName,48);
    return fetch(apiUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // "getSetCookie":cookie
    },
    body: JSON.stringify({ question: userMessage }),credentials:'include'
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    // console.log(response.json(),57);
   
    // document.cookie={userMessage:userMessage}
    document.cookie="dummy"
    return response.json();
  });
}
async function sendMessage(value) {// function for a get user input &&  send a message from a user 
   let message=value.trim()
  var userInput = document.getElementById("userInput");
  let  userMessage = userInput.value.trim();
  if (userMessage===""&&message!=='') {
    userMessage=message
  } else if(message==='') {
    userMessage=userMessage
    
  }
  //  console.log(userMessage,64,message);

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
  await fetchBotResponse(userMessage)
    .then(response => {
      // Display bot message
         // Display bot message
         console.log(response.cookie);
         //  document.cookie=`"user_name":${response?.cookie}`
          document.cookie = `session_id=${response?.cookie}; path=/; secure; samesite=strict`;
   
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



const searchInput = document.getElementById('searchInput');
let timeoutId;

// Function to be called after a 2-second delay
function delayedFunction() {
  fetchSuggestions();
}

// Function to debounce the input change event
function debounce(func, delay) {
  clearTimeout(timeoutId);
  timeoutId = setTimeout(func, delay);
}

// Function to fetch suggestions from API
async function fetchSuggestions() {
  const query = searchInput.value.trim(); // Get search query
  
  if (query === '') {
    clearSuggestions();
    return;
  }
  
  try {
    let  cookie= document.cookie
    console.log(cookie,8);
 const apiUrl=`https://en.wikipedia.org/w/api.php?action=opensearch&search=${query}&namespace=0&format=json&origin=*`
 document.cookie="dummy"
 
  
  const response = await fetch(apiUrl);
// console.log(response,204);
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
    const data = await response.json();
 
    displaySuggestions(data[1]); // Assuming results are an array of suggestions
  } catch (error) {
    console.error('Error fetching suggestions:', error);
    clearSuggestions();
  }
}

// Function to display suggestions
  function displaySuggestions(suggestions) {
  const suggestionContainer = document.getElementById('suggestionContainer');
  suggestionContainer.innerHTML = ''; // Clear previous suggestions
  
  suggestions.forEach(suggestion => {
    const suggestionElement = document.createElement('div');
    suggestionElement.classList.add('suggestion-item');
    suggestionElement.textContent = suggestion;
    suggestionElement.addEventListener('click', () => {
      // Handle suggestion selection (e.g., fill input field, perform search)
      searchInput.value = suggestion;
      sendMessage(suggestion)
      // console.log(suggestion,223);
      
      clearSuggestions();
      // Additional functionality as needed...
    });
    suggestionContainer.appendChild(suggestionElement);
  });
}

// Function to clear suggestions
function clearSuggestions() {
  const suggestionContainer = document.getElementById('suggestionContainer');
  suggestionContainer.innerHTML = '';
}

// Adding an event listener for the "input" event on the search input
searchInput.addEventListener('input', function() {
  // Call debounce function with delayedFunction and delay of 2000 milliseconds (2 seconds)
  debounce(delayedFunction, 2000);
});

