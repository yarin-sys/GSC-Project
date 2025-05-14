import { refreshToken } from "../item-list/app.js";

// Toggle search bar
document.addEventListener("DOMContentLoaded", function () {
  const searchIcon = document.getElementById("search-icon");
  const searchForm = document.getElementById("search-form");

  if (searchIcon && searchForm) {
    searchIcon.addEventListener("click", function () {
      searchForm.classList.toggle("d-none");
    });
  }

  const scrollWrapper = document.querySelector(".scrolling-wrapper");

  if (scrollWrapper) {
    scrollWrapper.addEventListener(
      "wheel",
      function (e) {
        if (e.deltaY !== 0) {
          e.preventDefault();
          scrollWrapper.scrollBy({
            left: e.deltaY < 0 ? -100 : 100,
            behavior: "smooth",
          });
        }
      },
      { passive: false }
    ); // Important to allow preventDefault()
  }
});

//Fetch API

const itemMenu = document.getElementById("itemMenu");
const houseItem = document.getElementById("houseItem");
const electronicItem = document.getElementById("electronicItem");
const otherItem = document.getElementById("otherItem");

const baseEndpoint = "http://localhost:8000";

const authToken = localStorage.getItem("access");

function isTokenNotValid(jsonData) {
  if (jsonData.code && jsonData.code === "token_not_valid") {
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

  if (isValidData && data) {
    let htmlStr = "";
    let electStr = "";
    let houStr = "";
    let othStr = "";

    let result_data = data;

    for (let result of result_data) {
      htmlStr += `
                <div class="card custom-card me-3">
                  <img src="${result.picture}" class="card-img-top" alt="${result.item_name}">
                  <div class="card-body text-center">
                    <p class="card-title fw-bold mb-0"><a href="item-detail/index.html#item/${result.id}" ">${result.item_name}</a></p>
                  </div>
                </div>
          `;

      switch (result.category) {
        case "ELECTRONIC":
          electStr += `                
                  <div class="card custom-card me-3">
                    <img src="${result.picture}" class="card-img-top" alt="${result.item_name}">
                    <div class="card-body text-center">
                      <p class="card-title fw-bold mb-0"><a href="item-detail/index.html#item/${result.id}" ">${result.item_name}</a></p>
                    </div>
                  </div>
                `;
          break;

        case "HOUSE_APPLIANCES":
          houStr += `                
              <div class="card custom-card me-3">
                <img src="${result.picture}" class="card-img-top" alt="${result.item_name}">
                <div class="card-body text-center">
                  <p class="card-title fw-bold mb-0"><a href="item-detail/index.html#item/${result.id}" ">${result.item_name}</a></p>
                </div>
              </div>
            `;
          break;

        case "OTHER":
          othStr += `
            <div class="card custom-card">
              <img src="${result.picture}" class="card-img-top" alt="${result.item_name}">
              <div class="card-body text-center">
                <p class="card-title fw-bold mb-0"><a href="item-detail/index.html#item/${result.id}" ">${result.item_name}</a></p>
              </div>
            </div>
          `;
          break;

        default:
          break;
      }
    }
    itemMenu.innerHTML = htmlStr;
    houseItem.innerHTML = houStr;
    electronicItem.innerHTML = electStr;
    otherItem.innerHTML = othStr;

    if (!data[0]) {
      itemMenu.innerHTML = "<p> Tidak ada Items </p>";
    }
  } else {
    itemMenu.innerHTML = "<p>Tidak ada Items </p>";
  }
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

const chatbotPopup = document.getElementById("chatbot-container-standalone");
const popupIcon = document.getElementById("pop-up");

document.getElementById("pop-up").addEventListener("click", function () {
  if (chatbotPopup.style.display === "none" || chatbotPopup.style.display === "") {
    chatbotPopup.style.display = "flex";
  } else {
    chatbotPopup.style.display = "none";
  }
});

document.addEventListener("click", (event) => {
  const isClickInside = chatbotPopup.contains(event.target) || popupIcon.contains(event.target);
  if (!isClickInside) {
    chatbotPopup.style.display = "none";
  }
});
