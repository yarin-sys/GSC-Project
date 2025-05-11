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
