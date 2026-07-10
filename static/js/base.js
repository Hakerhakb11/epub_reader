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

    const themeSelect = document.getElementById('theme-select');
    const interfaceFontSizeInput = document.getElementById('interface-font-size-select')
    const textFontSizeInput = document.getElementById('text-font-size-select');
    const containerWidthInput = document.getElementById('container-width-select');

    if (themeSelect) {
        themeSelect.addEventListener('change', (event) => {
            const selectedTheme = event.target.value;
            document.body.className = selectedTheme;
            
            saveSettingsToServer();
        });
    }

    if (interfaceFontSizeInput) {
        interfaceFontSizeInput.addEventListener('input', (event) => {
            const value = event.target.value;
            document.documentElement.style.setProperty('--body-font-size', `${value}px`);

            interfaceFontSizeInput.nextElementSibling.value = value;
        });

        interfaceFontSizeInput.addEventListener('change', saveSettingsToServer);
    }

    if (textFontSizeInput) {
        textFontSizeInput.addEventListener('input', (event) => {
            const value = event.target.value;
            document.documentElement.style.setProperty('--text-font-size', `${value}px`);
            
            textFontSizeInput.nextElementSibling.value = value;
        });

        textFontSizeInput.addEventListener('change', saveSettingsToServer);
    }

    if (containerWidthInput) {
        containerWidthInput.addEventListener('input', (event) => {
            const value = event.target.value;
            document.documentElement.style.setProperty('--block-content-width', `${value}%`);
            
            containerWidthInput.nextElementSibling.value = value;
        });

        containerWidthInput.addEventListener('change', saveSettingsToServer);
    }
});

function saveSettingsToServer() {
    const form = document.querySelector('.settings-panel form');
    if (!form) return;

    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            console.error('Eror, saveSettingsToServer failed:', response.statusText);
        }
    })
    .catch(error => console.error('Network error:', error));
}
