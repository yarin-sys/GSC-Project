const map = L.map("map").setView([-7.797068, 110.370529], 13);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "© OpenStreetMap contributors",
}).addTo(map);
L.marker([-7.797068, 110.370529]).addTo(map).bindPopup("Yogyakarta").openPopup();
