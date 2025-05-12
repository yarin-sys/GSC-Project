document.addEventListener('DOMContentLoaded', () => {
    const chatbotLog = document.getElementById('chatbot-log-standalone');
    const chatbotForm = document.getElementById('chatbot-form-standalone');
    const messageInput = document.getElementById('chatbot-message-input-standalone');
    const imageInput = document.getElementById('chatbot-image-input-standalone');
    const imagePreviewContainer = document.getElementById('chatbot-preview-container-standalone');
    const imagePreview = document.getElementById('chatbot-image-preview-standalone');
    const removeImageBtn = document.getElementById('chatbot-remove-image-btn-standalone');
    const loadingIndicator = document.getElementById('chatbot-loading-standalone');

    // Fungsi untuk menambahkan pesan ke log chat
    function addMessageToLog(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chatbot-message-standalone');
        if (sender === 'user') {
            messageDiv.classList.add('user-message-standalone');
        } else {
            messageDiv.classList.add('bot-message-standalone');
        }
        messageDiv.textContent = message; // Untuk teks sederhana
        // Jika ingin render HTML (misal <br>), gunakan .innerHTML, tapi hati-hati XSS jika message dari user
        chatbotLog.appendChild(messageDiv);
        chatbotLog.scrollTop = chatbotLog.scrollHeight; // Auto-scroll ke pesan terbaru
    }

    // Pratinjau gambar
    if (imageInput) {
        imageInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                    imagePreviewContainer.style.display = 'block'; // Tampilkan kontainer pratinjau
                }
                reader.readAsDataURL(file);
            } else {
                imagePreviewContainer.style.display = 'none';
                imagePreview.src = '#';
            }
        });
    }

    // Tombol hapus gambar pratinjau
    if (removeImageBtn) {
        removeImageBtn.addEventListener('click', function() {
            imageInput.value = ''; // Reset file input
            imagePreview.src = '#';
            imagePreviewContainer.style.display = 'none';
        });
    }

    // Handle submit form
    if (chatbotForm) {
        chatbotForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const userMessage = messageInput.value.trim();
            const imageFile = imageInput.files[0];

            if (!userMessage && !imageFile) {
                // Mungkin tampilkan pesan error kecil atau abaikan
                return;
            }

            // Tampilkan pesan pengguna di log
            if (userMessage) {
                addMessageToLog(userMessage, 'user');
            }
            if (imageFile) {
                addMessageToLog(`[Gambar: ${imageFile.name}]`, 'user'); // Atau tampilkan pratinjau kecil di chat
            }

            // Kosongkan input teks
            messageInput.value = '';
            // Kosongkan input file dan pratinjau (jika diinginkan setelah submit)
            // imageInput.value = '';
            // imagePreview.src = '#';
            // imagePreviewContainer.style.display = 'none';

            // --- Di sini Anda akan menambahkan logika fetch ke API backend ---
            // Tampilkan loading
            loadingIndicator.style.display = 'block';
            console.log("Pesan:", userMessage, "Gambar:", imageFile ? imageFile.name : "Tidak ada");

            // Simulasi respons bot setelah beberapa saat
            setTimeout(() => {
                loadingIndicator.style.display = 'none';
                let botReply = "Saya menerima pesan Anda";
                if (userMessage.toLowerCase().includes("harga")) {
                    botReply = "Untuk perkiraan harga, saya perlu melihat gambar kerusakannya.";
                } else if (imageFile) {
                    botReply = "Terima kasih untuk gambarnya. Saya akan coba analisis dan berikan perkiraan harga.";
                }
                addMessageToLog(botReply, 'bot');
            }, 1500); // Delay 1.5 detik

            // Jangan lupa untuk membersihkan input file & preview jika sudah dikirim ke backend
            // dan backend sudah merespons.
            // imageInput.value = '';
            // imagePreview.src = '#';
            // imagePreviewContainer.style.display = 'none';
        });
    }

    // Contoh: jika Anda memiliki tombol buka/tutup modal yang berdiri sendiri
    // const openBtnStandalone = document.getElementById('open-chatbot-btn-standalone');
    // const chatbotContainerStandalone = document.getElementById('chatbot-container-standalone');
    // if(openBtnStandalone && chatbotContainerStandalone){
    //     openBtnStandalone.addEventListener('click', () => {
    //         chatbotContainerStandalone.style.display = 'flex'; // Atau 'block'
    //     });
    // }
    // (Anda perlu tombol close juga jika menggunakan ini)
});