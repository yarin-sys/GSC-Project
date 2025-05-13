import {} from '../../item-list/app.js';

const contentContainer = document.getElementById("content-container");


const baseEndpoint = "http://localhost:8000";

const hash = window.location.hash; // "#item/4"
const parts = hash.split('/');
const itemId = parts[1]; // "4"
console.log(itemId);

const authToken = localStorage.getItem("access");


function isTokenNotValid(jsonData) {
  if(jsonData.code && jsonData.code === 'token_not_valid'){
      refreshToken();

      alert("Please Login Again");
      window.location.href = "http://127.0.0.1:5500/signup-login/login/index.html";
      return false;
  }
  return true;
}

function showData(data) {
  console.log(data);
  const isValidData = isTokenNotValid(data);

  if (isValidData && data) {
    let htmlStr = "";
    let result = data;

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
      <div class="d-flex card" style="background-color: #ffc611; border-radius: 20px; padding: 2rem; display: flex; gap: 2rem; align-items: flex-start; flex-wrap: wrap; width: " id="kuning">
        <!-- Gambar -->
        <div class="gambar" >
          <img src="${result.picture}" alt="${result.item_name}" style=" border-radius: 37px;" />
        </div>

        <!-- Informasi Item -->
        <div class="info" style="height: 320px;>
          <h1 style="margin-bottom: 0.5rem;">${result.item_name}</h1>
          ${ownerInfo}
          <p><strong>Tingkat Kerusakan:</strong> ${rateString}</p>
          <strong>Deskripsi:</strong><p> ${result.deskripsi}</p>
          <strong>Address:</strong><p> ${result.pick_address}</p>
          <p><strong>Harga Penawaran:</strong> Rp${result.price_offered.toLocaleString("id-ID")}</p>
          ${finalPriceInfo}
        </div>

        <!-- Status Fixed dan Tombol -->
        <div style="flex: 1 1 100%; display: flex; justify-content: space-between; align-items: center; margin-top: 2rem;">
          <div id="isFixed">
            <p style="font-weight: bold;">Is your item ready to be fixed?</p>
          </div>
          <div style="display: flex; gap: 1rem;">
            <button style="padding: 0.5rem 1rem; background-color: #164058; color: white; border: none; border-radius: 5px;">Fix it!</button>
            <button style="padding: 0.5rem 1rem; background-color: white; border: 2px solid #164058; color: #164058; border-radius: 5px;">Cancel</button>
          </div>
        </div>
      </div>
                `;
    
    contentContainer.innerHTML = htmlStr;
  } else {
    contentContainer.innerHTML = "<p>Tidak ada Items </p>";
  }
}


const options = {
  method: "GET",
  headers: {
    Authorization: `Bearer ${authToken}`,
  },
};

fetch(`${baseEndpoint}/item/${itemId}`, options)
  .then((response) => {
    console.log("respon sebagai berikut: ", response);
    return response.json();
  })
  .then((data) => showData(data))
  .catch((error) => {
    console.log(error);
  });

