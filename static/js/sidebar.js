
    var menu_btn = document.querySelector("#menu-btn");
    var sidebar = document.querySelector("#sidebar");
    var container = document.querySelector(".my-container");
    menu_btn.addEventListener("click", () => {
      sidebar.classList.toggle("active-nav");
      container.classList.toggle("active-cont");
    });

    // Add a click event listener to each navigation item
    var navs = document.querySelectorAll(".inner-anchor");
    navs.forEach(function(nav) {
      nav.addEventListener("click", function() {
        // Remove the "selected" class from all navigation items
        navs.forEach(function(item) {
          item.classList.remove("selected");
        });
        // Add the "selected" class to the clicked navigation item
        this.classList.add("selected");
      });
    });
