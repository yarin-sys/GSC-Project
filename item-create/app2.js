
import { refreshToken } from "../item-list/app.js";

const warningPrice = document.getElementById('warning-price');

function isTokenNotValid(jsonData) {
    if(jsonData.code && jsonData.code === 'token_not_valid'){
        refreshToken();

        alert("Please Login Again");
        window.location.href = "http://127.0.0.1:5500/signup-login/login/index.html";
        return false;
    }
    return true;
}

// get access token from local(cache data)
const authToken = localStorage.getItem('access');

window.addEventListener("load", (event) => {
    event.preventDefault();
    const itemsForm = document.getElementById('itemsForm');


    itemsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let itemsFormData = new FormData(itemsForm);
    
        fetch('http://localhost:8000/items/', {
            method: 'POST',
            headers: {
                "Authorization" : `Bearer ${authToken}`
            },
            body: itemsFormData
        })
        .then(response => {
        
            if (!response.ok) {
                // contoh error handling spesifik
                if (data.price_offered && data.price_offered[0]) {
                    warningPrice.innerHTML = `<p>${data.price_offered[0]}</p>`;
                }
                throw new Error(`Server Error: ${response.status}`);
            }
            
            return response.json();

        })
        .then(data => {
            const isValid = isTokenNotValid(data);
            if (isValid) {
                console.log('Response:', data);
                alert("Data berhasil dikirim");
                // itemsForm.reset();
                window.location.href = "http://localhost:5500/menu/menu.html";
                itemsForm.reset();
            }
        })
        .catch(error => {
            console.log('Terjadi kesalahan: ' + error);
            alert("Data gagal terkirim");
            
        });
    });
    
})

// Toggle search bar visibility
document.addEventListener("DOMContentLoaded", () => {
    const searchIcon = document.getElementById("search-icon");
    const searchForm = document.getElementById("search-form");
  
    if (searchIcon && searchForm) {
      searchIcon.addEventListener("click", () => {
        searchForm.style.display = searchForm.style.display === "none" ? "flex" : "none";
      });
    }
  });


