const contentContainer = document.getElementById("content-container");
const searchForm = document.getElementById("searchForm");

const baseEndpoint = "http://localhost:8000";

if (searchForm) {
  searchForm.addEventListener("submit", handleSearch);
}

const authToken = localStorage.getItem("access");

function isTokenNotValid(jsonData) {
  if (jsonData.code && jsonData.code === "token_not_valid") {
    // run a refresh token query
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

  if (isValidData && data) {
    let htmlStr = "";
    let result_data = data;

    for (result of result_data) {
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
        case 4:
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
    }
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


const options = {
  method: "GET",
  headers: {
    Authorization: `Bearer ${authToken}`,
  },
};

fetch(endpoint, options)
  .then((response) => {
    console.log("respon sebagai berikut: ", response);
    return response.json();
  })
  .then((data) => showData(data))
  .catch((error) => {
    console.log(error);
  });

// const searchIcon = document.getElementById("search-icon");

// const input = searchForm.querySelector('input[type="text"]');
// const button = searchForm.querySelector('input[type="submit"]');

// searchIcon.addEventListener("click", function () {
//   const isHidden = input.style.display === "none";
//   input.style.display = isHidden ? "inline-block" : "none";
//   button.style.display = isHidden ? "inline-block" : "none";

//   if (isHidden) {
//     input.focus();
//   }
// });
