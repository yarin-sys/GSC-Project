
const warningPrice = document.getElementById('warning-price');

function refreshToken() {
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

// get access token from local(cache data)
const authToken = localStorage.getItem('access');

window.addEventListener("load", (event) => {
    event.preventDefault();
    const itemsForm = document.getElementById('itemsForm');
    // let fileInput = document.querySelector('input[type="file"]');


    itemsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let itemsFormData = new FormData(itemsForm);

        // mandatory if you input file (in this case image)
        // let fileInput = document.querySelector('input[type="file"]');
        // itemsFormData.append('file', fileInput.files[0]);
    
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


