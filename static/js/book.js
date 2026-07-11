document.addEventListener('DOMContentLoaded', () => {
    const divider = document.getElementById('sidebarDivider');
    const bookmarksPanel = document.getElementById('bookmarksPanel');
    const toggleBtn = document.getElementById('toggleBookmarksBtn');

    let isResizing = false;

    const activeChapter = document.querySelector('.chapters a.active');
    if (activeChapter) {
        activeChapter.scrollIntoView({ block: 'center', behavior: 'instant' });
    }

    const activeBookmark = document.querySelector('.bookmark-item .bookmark-link.active');
    if (activeBookmark) {
        activeBookmark.scrollIntoView({ block: 'center', behavior: 'instant' })
    }

    let savedHeight = parseInt(localStorage.getItem('bookmarksHeight'), 10) || 200;
    let isCollapsed = localStorage.getItem('bookmarksCollapsed') === 'true';

    bookmarksPanel.style.transition = 'none';

    if (isCollapsed) {
        bookmarksPanel.classList.add('collapsed');
        divider.classList.add('collapsed');
        bookmarksPanel.style.height = '0px';
    } else {
        bookmarksPanel.style.height = `${savedHeight}px`;
    }

    bookmarksPanel.offsetHeight;
    bookmarksPanel.style.transition = 'height 0.2s ease';

    toggleBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleBookmarks();
    });

    divider.addEventListener('dblclick', () => {
        toggleBookmarks();
    });

    function toggleBookmarks() {
        isCollapsed = !isCollapsed;
        localStorage.setItem('bookmarksCollapsed', isCollapsed);

        if (isCollapsed) {
            if (bookmarksPanel.offsetHeight > 0) {
                savedHeight = bookmarksPanel.offsetHeight;
                localStorage.setItem('bookmarksHeight', savedHeight);
            }
            bookmarksPanel.classList.add('collapsed');
            divider.classList.add('collapsed');
        } else {
            bookmarksPanel.classList.remove('collapsed');
            divider.classList.remove('collapsed');
            bookmarksPanel.style.height = `${savedHeight}px`;
        }
    }

    divider.addEventListener('mousedown', (e) => {
        if (e.target.closest('#toggleBookmarksBtn')) return;
        if (isCollapsed) return;

        e.preventDefault();
        isResizing = true;

        document.body.classList.add('resizing-active');
        document.body.style.cursor = 'row-resize';
        bookmarksPanel.style.transition = 'none';
    });

    document.addEventListener('mousemove', (e) => {
        if (!isResizing) return;
        e.preventDefault();

        const container = divider.parentElement;
        if (!container) return;

        const containerRect = container.getBoundingClientRect();
        const newHeight = containerRect.bottom - e.clientY;
        const maxHeight = containerRect.height * 0.75;

        if (newHeight >= 40 && newHeight <= maxHeight) {
            bookmarksPanel.style.height = `${newHeight}px`;
            savedHeight = newHeight;
        }
    });

    document.addEventListener('mouseup', () => {
        if (isResizing) {
            isResizing = false;

            document.body.classList.remove('resizing-active');
            document.body.style.cursor = 'default';
            bookmarksPanel.style.transition = 'height 0.2s ease';

            localStorage.setItem('bookmarksHeight', savedHeight);
        }
    });
});

function startEdit(button) {
    const item = button.closest('.aside-item');
    if (!item) return;

    item.classList.add('is-editing');

    const menu = item.querySelector('.aside-menu');
    if (menu) menu.removeAttribute('open');

    const input = item.querySelector('.bookmark-edit-input');
    if (input) {
        input.focus();
        input.setSelectionRange(input.value.length, input.value.length);
    }
}

function cancelEdit(button) {
    const item = button.closest('.aside-item');
    if (item) {
        item.classList.remove('is-editing');
    }
}
