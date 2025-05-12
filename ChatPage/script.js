document.addEventListener("DOMContentLoaded", function () {
  const input = document.querySelector(".chat-input");
  const chatBox = document.querySelector(".chat-box");
  const plusButton = document.getElementById("plus-button");
  const negotiationBubble = document.getElementById("negotiation-bubble");
  const negotiationInput = document.getElementById("negotiation-input");

  // Enter message from main chat input
  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && input.value.trim() !== "") {
      const message = input.value.trim();
      const bubble = document.createElement("div");
      bubble.className = "chat-bubble-right";
      bubble.innerHTML = `
        <img src="Images/test.png" class="rounded-circle" width="35" height="35" alt="User" />
        <div class="chat-message">${message}</div>
      `;
      chatBox.insertBefore(bubble, input.parentElement);
      input.value = "";
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  });

  // Show negotiation bubble on plus button click
  plusButton.addEventListener("click", function () {
    negotiationBubble.style.display = "flex";
    negotiationInput.focus();
  });

  // Handle negotiation offer submission
  negotiationInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && negotiationInput.value.trim() !== "") {
      const price = negotiationInput.value.trim();
      const offerBubble = document.createElement("div");
      offerBubble.className = "chat-bubble-right";
      offerBubble.innerHTML = `
        <img src="Images/test.png" class="rounded-circle" width="35" height="35" alt="User" />
        <div class="chat-message">How about ${price}?</div>
      `;
      chatBox.insertBefore(offerBubble, negotiationBubble);
      negotiationInput.value = "";
      negotiationBubble.style.display = "none";
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  });
});
