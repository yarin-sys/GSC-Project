const map = L.map("map").setView([-7.797068, 110.370529], 13);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors",
}).addTo(map);
L.marker([-7.797068, 110.370529]).addTo(map).bindPopup("Yogyakarta").openPopup();

// Cek apakah halaman ini ditampilkan di dalam iframe
if (window !== window.parent) {
  // Artinya: halaman ini sedang dibuka dari iframe
  // Sembunyikan navbar
  document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector(".navbar"); // atau ID jika pakai #navbar
    if (navbar) {
      navbar.style.display = "none";
    }
  });
}
