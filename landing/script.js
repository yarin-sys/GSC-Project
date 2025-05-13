const searchIcon = document.getElementById("search-icon");
const searchForm = document.getElementById("search-form");
const input = searchForm.querySelector("input");
const button = searchForm.querySelector("button");
const icon = searchForm.querySelector("icon");

searchIcon.addEventListener("click", function () {
  // toggle tampil/sembunyi
  if (input.style.display === "none") {
    input.style.display = "inline-block";
    button.style.display = "inline-block";
    input.focus(); // langsung fokus ke input
  } else {
    input.style.display = "none";
    button.style.display = "none";
  }
});
