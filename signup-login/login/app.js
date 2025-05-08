const loginForm = document.getElementById("login-form");
const baseEndpoint = "http://localhost:8000/";

if (loginForm) {
  loginForm.addEventListener("submit", handleLogin);
}

function handleLogin(event) {
  console.log(event);
  event.preventDefault();
  const loginEndpoint = `${baseEndpoint}api/token/`;

  let loginFormData = new FormData(loginForm);
  let loginObjectData = Object.fromEntries(loginFormData);
  let bodyStr = JSON.stringify(loginObjectData);
  // console.log("bodystr : ",bodyStr);

  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: bodyStr,
  };

  fetch(loginEndpoint, options)
    .then((response) => {
      console.log("respon e: ", response);
      if (response.ok) {
        alert(`Login successful`);
      } else {
        alert("login gagal");
      }
      return response.json();
    })
    .then((data) => {
      handleAuthData(data);

      if (data) {
        window.location.href = "http://127.0.0.1:5500/item-list/index.html";
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

// storing access and refresh token in local storage
function handleAuthData(authData) {
  localStorage.setItem("access", authData.access);
  localStorage.setItem("refresh", authData.refresh);
}

function tombol() {
  document.getElementById("tombol").addEventListener("click", function () {
    window.location.href = "https://github.com/yarin-sys/GSC-Project/tree/main";
  });
}
