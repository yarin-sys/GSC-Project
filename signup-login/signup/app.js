
    const signupForm = document.getElementById('signupForm');
    let fileInput = document.querySelector('input[type="file"]');


    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        let signupFormData = new FormData(signupForm);

        // mandatory if you input file (in this case image)
        let fileInput = document.querySelector('input[type="file"]');
        signupFormData.append('file', fileInput.files[0]);
    
        fetch('http://localhost:8000/signup2/', {
            method: 'POST',
            body: signupFormData
        })
        .then(async response => {
            const data = await response.json();  // tetap ambil JSON untuk tahu pesan error
        
            if (!response.ok) {
                // contoh error handling spesifik
                // if (data.price_offered && data.price_offered[0]) {
                //     warningPrice.innerHTML = `<p>${data.price_offered[0]}</p>`;
                // }
                throw new Error(`Server Error: ${response.status}`);
            } else {
                console.log('Response:', data);
                alert("Sign up berhasil");
                // itemsForm.reset();
                window.location.href = "http://localhost:5500/signup-login/login/index.html";
                itemsForm.reset();
            }
            
        })
        .catch(error => {
            console.log('Terjadi kesalahan: ' + error);
            alert("Data gagal terkirim");
            
        });
    });
    



