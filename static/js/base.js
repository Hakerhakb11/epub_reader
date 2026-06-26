document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('mainSidebar');
    
    if (sidebar) {
        const isSidebarOpen = localStorage.getItem('mainSidebarOpen');
        
        if (isSidebarOpen === 'true') {
            sidebar.open = true;
        } else if (isSidebarOpen === 'false') {
            sidebar.open = false;
        }

        sidebar.addEventListener('toggle', () => {
            localStorage.setItem('mainSidebarOpen', sidebar.open);
        });
    }
});
