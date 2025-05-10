
const warningPrice = document.getElementById('warning-price');

function isTokenNotValid(jsonData) {
    if(jsonData.code && jsonData.code === 'token_not_valid'){
        // run a refresh token query

        alert("Please Login Again");
        window.location.href = "http://127.0.0.1:5500/signup-login/login/index.html";
        return false;
    }
    return true;
}

// get access token from local(cache data)
const authToken = localStorage.getItem('access');

window.addEventListener("load", (event) => {
    const itemsForm = document.getElementById('itemsForm');
    let fileInput = document.querySelector('input[type="file"]');


    itemsForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let itemsFormData = new FormData(itemsForm);

        // mandatory if you input file (in this case image)
        let fileInput = document.querySelector('input[type="file"]');
        itemsFormData.append('file', fileInput.files[0]);
    
        fetch('http://localhost:8000/items/', {
            method: 'POST',
            headers: {
                "Authorization" : `Bearer ${authToken}`
            },
            body: itemsFormData
        })
        .then(async response => {
            const data = await response.json();  // tetap ambil JSON untuk tahu pesan error
        
            if (!response.ok) {
                // contoh error handling spesifik
                if (data.price_offered && data.price_offered[0]) {
                    warningPrice.innerHTML = `<p>${data.price_offered[0]}</p>`;
                }
                throw new Error(`Server Error: ${response.status}`);
            }
        
            const isValid = isTokenNotValid(data);
            if (isValid) {
                console.log('Response:', data);
                alert("Data berhasil dikirim");
                // itemsForm.reset();
                window.location.href = "http://localhost:5500/item-list/index.html";
                itemsForm.reset();
            }
        })
        .catch(error => {
            console.log('Terjadi kesalahan: ' + error);
            alert("Data gagal terkirim");
            
        });
    });
    
})


