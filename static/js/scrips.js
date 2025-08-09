function toggleSidebar() {
    const sidebar = document.getElementById("sidebar");
    if (window.innerWidth <= 768) {
        sidebar.classList.toggle("open");
    } else {
        sidebar.classList.toggle("minimized");
    }
}

function expandSidebar() {
    document.getElementById("sidebar").classList.remove("minimized", "closed");
}

function closeSidebar() {
    document.getElementById("sidebar").classList.add("closed");
}
