document.addEventListener('DOMContentLoaded', function () {
    const desktopSidebarToggle = document.getElementById('desktopSidebarToggle');
    const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.querySelector('.sidebar-overlay');
    const closeSidebarBtn = document.querySelector('.btn-close-sidebar');

    if (desktopSidebarToggle) {
        desktopSidebarToggle.addEventListener('click', function () {
            sidebar.classList.toggle('collapsed');
            document.body.classList.toggle('sidebar-collapsed');
        });
    }

    if (mobileSidebarToggle) {
        mobileSidebarToggle.addEventListener('click', function () {
            sidebar.classList.add('show');
            sidebarOverlay.classList.add('show');
        });
    }

    function closeMobileSidebar() {
        if (sidebar && sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
            sidebarOverlay.classList.remove('show');
        }
    }

    if (closeSidebarBtn) {
        closeSidebarBtn.addEventListener('click', closeMobileSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeMobileSidebar);
    }

    // Close sidebar on section click in mobile
    const navLinks = document.querySelectorAll('#sidebar .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992) {
                closeMobileSidebar();
            }
        });
    });
});