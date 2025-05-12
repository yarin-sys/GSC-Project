const contentContainer = document.getElementById("content-container");
const searchForm = document.getElementById("searchForm");

const baseEndpoint = "http://localhost:8000";

if (searchForm) {
  searchForm.addEventListener("submit", handleSearch);
}

const authToken = localStorage.getItem("access");

export function refreshToken() {
  const refresh = localStorage.getItem('refresh'); // Ambil refresh token dari localStorage

  if (!refresh) {
      alert("No refresh token found. Please login again.");
      window.location.href = "http://127.0.0.1:5500/signup-login/login/index.html";
      return;
  }

  fetch('http://localhost:8000/api/token/refresh/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ refresh: localStorage.getItem('refresh') })
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Refresh token invalid');
      }
      return response.json();
  })
  .then(data => {
      // Simpan access token baru
      localStorage.setItem('access', data.access);
      console.log('Token refreshed');
  })
  .catch(error => {
      console.error('Error refreshing token:', error);
      alert("Session expired. Please login again.");
      window.location.href = "http://127.0.0.1:5500/signup-login/login/index.html";
  });
}

function isTokenNotValid(jsonData) {
  if(jsonData.code && jsonData.code === 'token_not_valid'){
      refreshToken();

      alert("Please Login Again");
      window.location.href = "http://127.0.0.1:5500/signup-login/login/index.html";
      return false;
  }
  return true;
}

const endpoint = `${baseEndpoint}/items/`;

function showData(data) {
  console.log(data);
  const isValidData = isTokenNotValid(data);

  if (isValidData && data[0]) {
    let htmlStr = "";
    let result = data[0];


      let rateString;

      switch (result.rate) {
        case 1:
          rateString = "Low";
          break;
        case 2:
          rateString = "Moderate";
          break;
        case 3:
          rateString = "Considerable";
          break;
        case 4:
          rateString = "Dangerous";
          break;
        case 5:
          rateString = "Considerable";
          break;
        default:
        // code block
      }

      //   .toLocaleString("id-ID")

      // Owner & Harga akhir
      let ownerInfo = result.owner ? `<p class="card-text"><strong>Owner:</strong> ${result.owner.username}</p>` : "";
      let finalPriceInfo = result.price_final ? `<p class="card-text"><strong>Harga akhir:</strong> Rp${result.price_final.toLocaleString("id-ID")}</p>` : "";
      let fixedText = result.fixed ? '<button style="background-color : green;">FIXED ! !</button>' : '<button style="background-color: #164058;">On Progress</button>';

      htmlStr += `
            <div class="card p-5" style="background-color: #ffc611; border-radius:34.74px; margin-bottom: 10rem">
                <div class="gambar">
                <img src="${result.picture}" class="card-img-top img-fluid mx-auto d-block mt-3" alt="${result.item_name}" />
                </div>

                <div class="info">
                <h2 class="card-title" align="center">${result.item_name}</h2>
                ${ownerInfo}
                <p class="card-text"><strong>Tingkat kerusakan:</strong> <br />${rateString}</p>
                <p class="card-text">
                    <strong>Deskripsi Kerusakan:</strong><br />
                    ${result.deskripsi}
                </p>
                <p class="card-text"><strong>Alamat:</strong> <br />${result.pick_address}</p>
                <p class="card-text"><strong>Harga penawaran :</strong> <br />Rp${result.price_offered.toLocaleString("id-ID")}</p>
                ${finalPriceInfo}
                </div>
                <div class="fixed">
                <p class="card-text" style="font-size: 25px; font-family: inter; font-weight: 700; text-wrap: nowrap"><strong>Is Ur item Fixed?:</strong><br /></p>
                ${fixedText}
                </div>
            </div>
                `;
    
    contentContainer.innerHTML = htmlStr;
    if (!data[0]) {
      contentContainer.innerHTML = "<p> Tidak ada Items </p>";
    }
  } else {
    contentContainer.innerHTML = "<p>Tidak ada Items </p>";
  }
}

function handleSearch(e) {
  e.preventDefault();

  let formData = new FormData(searchForm);
  let data = Object.fromEntries(formData);
  let searchParams = new URLSearchParams(data);
  const searchItems = `${baseEndpoint}/search/item/?${searchParams}`;

  // const authToken = localStorage.getItem("access");

  const options = {
    method: "GET",
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  };

  fetch(searchItems, options)
    .then((response) => {
      console.log("respon sebagai berikut: ", response);
      return response.json();
    })
    .then((data) => showData(data))
    .catch((error) => {
      console.log(error);
    });
}

