document.addEventListener('DOMContentLoaded', () => {

    // Back button
    let depth = parseInt(sessionStorage.getItem("app_depth")) || 0;
    depth++;
    sessionStorage.setItem("app_depth", depth);

    const backButton = document.getElementById('button-btn');

    if (backButton) {
        if (depth <= 1) {
            backButton.classList.add("disabled");
        } else {
            backButton.classList.remove("disabled");
        }
    }

    // Sidebar state
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

    // Color settings
    const form = document.querySelector('.settings-panel form');
    const bgHidden = document.getElementById('bg-color-hidden');
    const textHidden = document.getElementById('text-color-hidden');
    const bgPicker = document.getElementById('bg-picker');
    const textPicker = document.getElementById('text-picker');
    const presetButtons = document.querySelectorAll('.preset-btn');

    const interfaceFontSizeInput = document.getElementById('interface-font-size-select');
    const textFontSizeInput = document.getElementById('text-font-size-select');
    const containerWidthInput = document.getElementById('container-width-select');
    const asideWidthInput = document.getElementById('aside-width-select');
    const paragraphSpacingInput = document.getElementById('paragraph-spacing-select');

    function saveSettingsToServer() {
        if (!form) return;

        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => {
            if (!response.ok) {
                console.error('Error. saveSettingsToServer failed:', response.statusText);
            }
        })
        .catch(error => console.error('Network error:', error));
    }

    function updateColors(bgColor, textColor) {
        document.documentElement.style.setProperty('--body-background-color', bgColor);
        document.documentElement.style.setProperty('--body-color', textColor);

        if (bgHidden) bgHidden.value = bgColor;
        if (textHidden) textHidden.value = textColor;

        if (bgPicker) bgPicker.value = bgColor;
        if (textPicker) textPicker.value = textColor;
    }

    presetButtons.forEach(button => {
        button.addEventListener('click', () => {
            const bg = button.getAttribute('data-bg');
            const text = button.getAttribute('data-text');
            
            updateColors(bg, text);
            saveSettingsToServer();
        });
    });

    if (bgPicker && textPicker) {
        bgPicker.addEventListener('input', (e) => {
            document.documentElement.style.setProperty('--body-background-color', e.target.value);
            if (bgHidden) bgHidden.value = e.target.value;
        });
        textPicker.addEventListener('input', (e) => {
            document.documentElement.style.setProperty('--body-color', e.target.value);
            if (textHidden) textHidden.value = e.target.value;
        });

        bgPicker.addEventListener('change', saveSettingsToServer);
        textPicker.addEventListener('change', saveSettingsToServer);
    }

    // Font size and container width settings
    if (interfaceFontSizeInput) {
        interfaceFontSizeInput.addEventListener('input', (event) => {
            const value = event.target.value;
            document.documentElement.style.setProperty('--body-font-size', `${value}px`);
            if (interfaceFontSizeInput.nextElementSibling) {
                interfaceFontSizeInput.nextElementSibling.value = value;
            }
        });
        interfaceFontSizeInput.addEventListener('change', saveSettingsToServer);
    }

    if (textFontSizeInput) {
        textFontSizeInput.addEventListener('input', (event) => {
            const value = event.target.value;
            document.documentElement.style.setProperty('--text-font-size', `${value}px`);
            if (textFontSizeInput.nextElementSibling) {
                textFontSizeInput.nextElementSibling.value = value;
            }
        });
        textFontSizeInput.addEventListener('change', saveSettingsToServer);
    }

    if (containerWidthInput) {
        containerWidthInput.addEventListener('input', (event) => {
            const value = event.target.value;
            document.documentElement.style.setProperty('--block-content-width', `${value}%`);
            if (containerWidthInput.nextElementSibling) {
                containerWidthInput.nextElementSibling.value = value;
            }
        });
        containerWidthInput.addEventListener('change', saveSettingsToServer);
    }

    if (asideWidthInput) {
        asideWidthInput.addEventListener('input', (event) => {
            const value = event.target.value;
            document.documentElement.style.setProperty('--aside-width', `${value}px`);
            if (asideWidthInput.nextElementSibling) {
                asideWidthInput.nextElementSibling.value = value;
            }
        });
        asideWidthInput.addEventListener('change', saveSettingsToServer);
    }

    if (paragraphSpacingInput) {
        paragraphSpacingInput.addEventListener('input', (event) => {
            const value = event.target.value;
            document.documentElement.style.setProperty('--paragraph-spacing', `${value}px`);
            if (paragraphSpacingInput.nextElementSibling) {
                paragraphSpacingInput.nextElementSibling.value = value;
            }
        });
        paragraphSpacingInput.addEventListener('change', saveSettingsToServer);
    }

});

function safeBack(fallbackUrl = '/') {
    let depth = parseInt(sessionStorage.getItem("app_depth")) || 1;

    if (depth <= 1) return; 

    sessionStorage.setItem("app_depth", depth - 2);
    history.back();
}
