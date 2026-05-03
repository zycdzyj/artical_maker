(function () {
    const hamburger = document.getElementById("hamburgerBtn");
    const navMenu = document.getElementById("navMenu");
    let isMenuOpen = false;

    function closeMenu() {
        if (navMenu && navMenu.classList.contains("open")) {
            navMenu.classList.remove("open");
            if (hamburger) hamburger.classList.remove("active");
            if (hamburger) hamburger.setAttribute("aria-expanded", "false");
            isMenuOpen = false;
        }
    }

    function openMenu() {
        if (navMenu && !navMenu.classList.contains("open")) {
            navMenu.classList.add("open");
            if (hamburger) hamburger.classList.add("active");
            if (hamburger) hamburger.setAttribute("aria-expanded", "true");
            isMenuOpen = true;
        }
    }

    if (hamburger) {
        hamburger.addEventListener("click", (e) => {
            e.stopPropagation();
            if (navMenu && navMenu.classList.contains("open")) {
                closeMenu();
            } else {
                openMenu();
            }
        });
    }

    if (navMenu) {
        const links = navMenu.querySelectorAll("a");
        links.forEach((link) => {
            link.addEventListener("click", (e) => {
                if (window.innerWidth <= 768) {
                    closeMenu();
                }
            });
        });
    }

    window.addEventListener("resize", function () {
        if (window.innerWidth > 768) {
            closeMenu();
        }
    });

    document.addEventListener("click", function (event) {
        const isMobile = window.innerWidth <= 768;
        if (isMobile && navMenu && navMenu.classList.contains("open")) {
            const navContainer = document.querySelector(".nav-container");
            if (navContainer && !navContainer.contains(event.target)) {
                closeMenu();
            }
        }
    });

    document.addEventListener("keydown", function (e) {
        if (
            e.key === "Escape" &&
            navMenu &&
            navMenu.classList.contains("open")
        ) {
            closeMenu();
        }
    });
})();
