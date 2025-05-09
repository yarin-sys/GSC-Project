document.addEventListener("DOMContentLoaded", function () {
  const input = document.querySelector(".chat-input");
  const chatBox = document.querySelector(".chat-box");

  input.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && input.value.trim() !== "") {
      const message = input.value.trim();
      const bubble = document.createElement("div");
      bubble.className = "chat-bubble-right";
      bubble.innerHTML = `
        <img src="Images/test.png" class="rounded-circle" width="35" height="35" alt="User" />
        <div class="chat-message">${message}</div>
      `;
      chatBox.insertBefore(bubble, chatBox.lastElementChild.previousElementSibling);
      input.value = "";
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  });
});
