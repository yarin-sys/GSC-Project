document.addEventListener("DOMContentLoaded", function () {
  const chatBox = document.getElementById("chat-box");
  const textInput = document.getElementById("text-input");
  const plusButton = document.getElementById("plus-button");

  // Function to create chat bubble
  function addChatBubble(message, isOffer = false) {
    const bubble = document.createElement("div");
    bubble.className = "chat-bubble-right";
    bubble.innerHTML = `
      <img src="Images/test.png" class="rounded-circle" width="35" height="35" alt="User" />
      <div class="chat-message">${message}</div>
    `;
    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Function to create negotiation input field
  function addNegotiationInput() {
    const bubble = document.createElement("div");
    bubble.className = "chat-bubble-right negotiation-container";
    bubble.innerHTML = `
      <img src="Images/test.png" class="rounded-circle" width="35" height="35" alt="User" />
      <input type="text" class="form-control negotiation-input" placeholder="Enter your price offer..." style="max-width: 70%; border-radius: 15px;"/>
    `;
    chatBox.appendChild(bubble);
    const input = bubble.querySelector(".negotiation-input");
    input.focus();

    input.addEventListener("keypress", function (e) {
      if (e.key === "Enter" && input.value.trim() !== "") {
        const price = input.value.trim();
        bubble.remove();
        addChatBubble(`How about ${price}?`, true);
        addOfferBox(price);
      }
    });

    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Function to create an offer box
  function addOfferBox(price) {
    const offerBox = document.createElement("div");
    offerBox.className = "offer-box";
    offerBox.innerHTML = `
      <h6 class="mb-1">Black Chair</h6>
      <p class="mb-2">${price}</p>
      <button>Confirm</button>
      <button>Deny</button>
    `;
    chatBox.appendChild(offerBox);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Handle main text input
  textInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && textInput.value.trim() !== "") {
      const message = textInput.value.trim();
      addChatBubble(message);
      textInput.value = "";
    }
  });

  // Handle plus button for negotiation
  plusButton.addEventListener("click", function () {
    addNegotiationInput();
  });
});
