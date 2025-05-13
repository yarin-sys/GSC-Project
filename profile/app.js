import { jwtDecode } from "https://cdn.jsdelivr.net/npm/jwt-decode@4.0.0/build/esm/index.js";
import { refreshToken } from "../item-list/app.js";

function isTokenNotValid(jsonData) {
    if(jsonData.code && jsonData.code === 'token_not_valid'){
        refreshToken();

        alert("Please Login Again");
        window.location.href = "http://127.0.0.1:5500/signup-login/login/index.html";
        return false;
    }
    return true;
}

const profileContainer = document.getElementById('profile-container');

const authToken = localStorage.getItem("access");
if (authToken) {
  const decoded = jwtDecode(authToken);
  const userId = decoded.user_id; // ini kuncinya
  const userId_int = parseInt(userId)
  console.log("User ID:", userId_int);

  // Contoh fetch ke endpoint user
  fetch(`http://127.0.0.1:8000/user/${userId_int}`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${authToken}`,
    }
  })
  .then(res => res.json())
  .then(data => {
    console.log("User detail:", data);
    const isValidData = isTokenNotValid(data);
    if (isValidData && data){
        let htmlStr = "";
        htmlStr +=  `
          <div  class="mt-4">
            <img src="${data.profile_pict}" alt="${data.username}" style="width: 468px; height: 468px; object-fit: cover; border-radius: 1000px" />
          </div>
          <div class="profile-desc">
            <h1 align="center">${data.username}</h1>
            <label for="phone"><strong>No Telepon:</strong> <br /></label>
            <p id="phone">${data.phone}</p>
            <label for="email"><strong>Email:</strong></label>
            <p id="email">${data.email}</p>
            <label for="address"><strong>Alamat:</strong></label>
            <p id="address">${data.address}</p>
          </div>

        `;
        profileContainer.innerHTML = htmlStr;

    }

  })
  .catch(err => {
    console.error("Gagal mengambil data user:", err);
  });
} else {
  console.error("Token tidak ditemukan di localStorage");
}

