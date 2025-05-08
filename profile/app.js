import { jwtDecode } from "https://cdn.jsdelivr.net/npm/jwt-decode@4.0.0/build/esm/index.js";

function isTokenNotValid(jsonData) {
    if(jsonData.code && jsonData.code === 'token_not_valid'){
        // run a refresh token query

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

                <img src="${data.profile_pict}" class="card-img-top img-fluid mx-auto d-block mt-3" 
                alt="${data.username}" style="width: 100px; height:100px; object-fit: cover;">
                <h5 class="card-title">${data.username}</h5>
                 <p class="card-text"><strong>Alamat:</strong> ${data.address} </p>
                <p class="card-text"><strong>No Telepon:</strong> ${data.phone} </p>

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