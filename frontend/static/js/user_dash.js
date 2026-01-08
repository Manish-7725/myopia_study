const sidebar = document.getElementById('sidebar');
const sidebarOverlay = document.querySelector('.sidebar-overlay');

function toggleSidebar() {
    sidebar.classList.toggle('show');
    sidebarOverlay.classList.toggle('show');
}

document.addEventListener('DOMContentLoaded', function () {
    // Close sidebar on section click in mobile
    const navLinks = document.querySelectorAll('#sidebar .nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (sidebar.classList.contains('show')) {
                toggleSidebar();
            }
        });
    });
});