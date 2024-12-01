document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("input");

  inputField.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      let input = inputField.value.trim();
      if (input) {
        fetchResponse(input);
        inputField.value = "";  // Clear the input field after sending the message
      }
    }
  });
});

function fetchResponse(input) {
  addChat(input, "");  // Temporarily display typing animation

  fetch("/get_response", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: input }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        addChat(input, "Sorry, something went wrong.");
      } else {
        addChat(input, data.response);  // Display the bot's response
      }
    })
    .catch(error => {
      console.error("Error:", error);
      addChat(input, "Error occurred while fetching response.");
    });
}

function addChat(input, product) {
  const messagesContainer = document.getElementById("messages");

  let userDiv = document.createElement("div");
  userDiv.id = "user";
  userDiv.className = "user response";
  userDiv.innerHTML = `<img src="static/user.png" class="avatar"><span>${input}</span>`;
  messagesContainer.appendChild(userDiv);

  let botDiv = document.createElement("div");
  let botImg = document.createElement("img");
  let botText = document.createElement("span");
  botDiv.id = "bot";
  botImg.src = "static/bot-mini.png";
  botImg.className = "avatar";
  botDiv.className = "bot response";
  botText.innerText = "Typing...";
  botDiv.appendChild(botText);
  botDiv.appendChild(botImg);
  messagesContainer.appendChild(botDiv);

  // Scroll to the most recent message
  messagesContainer.scrollTop = messagesContainer.scrollHeight - messagesContainer.clientHeight;

  // Fake delay to simulate "typing"
  setTimeout(() => {
    botText.innerText = `${product}`;
    textToSpeech(product);  // Use the speech synthesis
  }, 2000);
}
