document.addEventListener('DOMContentLoaded', () => {

    const outputDiv = document.querySelector('.output');
    const menu = document.getElementById('customContextMenu');
    const paragraphIdInput = document.getElementById('paragraphId');

    if (outputDiv && menu) {
        outputDiv.addEventListener('contextmenu', (event) => {
            const paragraph = event.target.closest('p');

            if (paragraph && outputDiv.contains(paragraph)) {
                event.preventDefault();

                if (paragraphIdInput) {
                    paragraphIdInput.value = paragraph.id;
                }

                document.querySelectorAll('.output p.selected').forEach(p => {
                    p.classList.remove('selected');
                });

                paragraph.classList.add('selected');

                const x = event.clientX;
                const y = event.clientY;

                menu.style.display = 'block';
                menu.style.left = `${x}px`;
                menu.style.top = `${y}px`;
            }
        });

        const bookmarkForms = document.querySelectorAll('.bookmark-form');
        if (bookmarkForms) {

            bookmarkForms.forEach(form => {
                form.addEventListener('submit', (event) => {
                    event.preventDefault(); 

                    const formData = new FormData(form);

                    fetch(form.action, {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => {
                        if (!response.ok) throw new Error('Ошибка сервера');
                        return response.json();
                    })
                    .then(data => {
                        if (data.status === 'success') {
                            console.log('Закладка успешно сохранена на абзац:', data.paragraph_id);
                            
                            if (menu.contains(form)) {
                                menu.style.display = 'none';
                            }

                            const activeParagraph = document.getElementById(`p-${data.paragraph_id}`);
                            if (activeParagraph) {
                                document.querySelectorAll('.output p.has-bookmark').forEach(p => {
                                    p.classList.remove('has-bookmark');
                                });
                                activeParagraph.classList.add('has-bookmark');
                            }

                            document.querySelectorAll('.output p.selected').forEach(p => {
                                p.classList.remove('selected');
                            });
                        }
                    })
                    .catch(error => {
                        console.error('Ошибка сохранения:', error);
                        alert('Не удалось сохранить закладку');
                    });
                });
            });
        }

        document.addEventListener('click', (event) => {
            if (!menu.contains(event.target)) {
                menu.style.display = 'none';
                
                if (!event.target.closest('.output p')) {
                    document.querySelectorAll('.output p.selected').forEach(p => {
                        p.classList.remove('selected');
                    });
                }
            }
        });
    }

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
