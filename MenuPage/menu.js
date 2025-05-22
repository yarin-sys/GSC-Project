// Toggle search bar
document.addEventListener("DOMContentLoaded", function () {
  const searchIcon = document.getElementById("search-icon");
  const searchForm = document.getElementById("search-form");

  if (searchIcon && searchForm) {
    searchIcon.addEventListener("click", function () {
      searchForm.classList.toggle("d-none");
    });
  }

  const scrollWrapper = document.querySelector('.scrolling-wrapper');

  if (scrollWrapper) {
    scrollWrapper.addEventListener('wheel', function (e) {
      if (e.deltaY !== 0) {
        e.preventDefault();
        scrollWrapper.scrollBy({
          left: e.deltaY < 0 ? -100 : 100,
          behavior: 'smooth'
        });
      }
    }, { passive: false }); // Important to allow preventDefault()
  }
});
