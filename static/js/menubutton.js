var menu_btn = document.querySelector("#menu-btn");
var sidebar = document.querySelector("#sidebar");
var container = document.querySelector(".my-container");
menu_btn.addEventListener("click", () => {
  sidebar.classList.toggle("active-nav");
  container.classList.toggle("active-cont");
});  
function checkSidebarVisibility() {
if (window.innerWidth < 768) {
sidebar.classList.remove("active-nav");
container.classList.remove("active-cont");
} else {
sidebar.classList.add("active-nav");
container.classList.add("active-cont");
}
}
// Event listener for window resize
window.addEventListener("resize", checkSidebarVisibility);

// Event listener for page load
window.addEventListener("load", checkSidebarVisibility);