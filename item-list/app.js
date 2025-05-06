const contentContainer = document.getElementById('content-container');
const baseEndpoint = "http://localhost:8000";

function isTokenNotValid(jsonData) {
    if(jsonData.code && jsonData.code === 'token_not_valid'){
        // run a refresh token query

        alert("Please Login Again");
        window.location.href = "http://127.0.0.1:5500/signup-login/login/index.html";
        return false;
    }
    return true;
}

const endpoint = `${baseEndpoint}/items/`;

const authToken = localStorage.getItem('access');

const options = {
    method: "GET",
    headers: {
        "Authorization" : `Bearer ${authToken}`
    }
};

fetch(endpoint, options)
    .then((response) => {
        console.log("respon sebagai berikut: ",response)
        return response.json()
    })
    .then(data => {
        console.log(data);
        const isValidData = isTokenNotValid(data);

        if (isValidData && data){
            let htmlStr = "";
            let result_data = data

            for (result of result_data){
                let rateString;

                switch(result.rate) {
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
    
                if (result.price_fina){
                    htmlStr +=  `
                    <div class="card mb-3 shadow-sm" id="card">
                        <div class="card-body">
                            <h5 class="card-title">${result.item_name}</h5>
                            <img src="${result.picture}" class="card-img-top img-fluid mx-auto d-block mt-3" 
                            alt="${result.item_name}" style="width: 220px; height:180px; object-fit: cover;">
                             <p class="card-text"><strong>Tingkat kerusakan:</strong> ${rateString} hari</p>
                            <p class="card-text"><strong>Deskripsi Kerusakan:</strong> ${result.deskripsi} ton</p>
                            <p class="card-text"><strong>Alamat:</strong> ${result.pick_address} ton</p>
                            <p class="card-text"><strong>Harga penawaran :</strong> Rp${result.price_offered.toLocaleString("id-ID")}</p>
                            <p class="card-text"><strong>Harga akhir :</strong> Rp${result.price_final.toLocaleString("id-ID")}</p>
                            <p class="card-text"><strong>Fixed:</strong> ${result.fixed}</p>
                            <br>
                        </div>
                    </div>
                    `;
                } else {
                    htmlStr +=  `
                    <div class="card mb-3 shadow-sm" id="card">
                        <div class="card-body">
                            <h5 class="card-title">${result.item_name}</h5>
                            <img src="${result.picture}" class="card-img-top img-fluid mx-auto d-block mt-3" 
                            alt="${result.item_name}" style="width: 220px; height:180px; object-fit: cover;">
                             <p class="card-text"><strong>Tingkat kerusakan:</strong> ${rateString} </p>
                            <p class="card-text"><strong>Deskripsi Kerusakan:</strong> ${result.deskripsi}</p>
                            <p class="card-text"><strong>Alamat:</strong> ${result.pick_address}</p>
                            <p class="card-text"><strong>Harga penawaran :</strong> Rp${result.price_offered.toLocaleString("id-ID")}</p>
                            <p class="card-text"><strong>Harga akhir :</strong> Rp${result.price_final.toLocaleString("id-ID")}</p>
                            <p class="card-text"><strong>Fixed:</strong> ${result.fixed}</p>
                            <br>
                        </div>
                    </div>
                `;
                }
            }     
            contentContainer.innerHTML = htmlStr
            if (!data[0]){
                contentContainer.innerHTML = "<p> Tidak ada Items </p>"
            }
        } else {
            contentContainer.innerHTML = "<p>Tidak ada Items </p>"
        }
    })
    .catch((error) =>{
        console.log(error);
});