document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.app-sidebar');
    const toggle = document.querySelector('[data-sidebar-toggle]');

    if (!sidebar || !toggle) {
        return;
    }

    const setCollapsed = (collapsed) => {
        document.documentElement.classList.toggle('sidebar-collapsed', collapsed);
        sidebar.classList.toggle('app-sidebar-collapsed', collapsed);
        toggle.setAttribute('aria-expanded', String(!collapsed));
        toggle.setAttribute('aria-label', collapsed ? 'Mostrar barra lateral' : 'Ocultar barra lateral');
        toggle.querySelector('span').textContent = collapsed ? '›' : '‹';
    };

    setCollapsed(window.localStorage.getItem('sidebar-collapsed') === 'true');

    toggle.addEventListener('click', () => {
        const collapsed = !sidebar.classList.contains('app-sidebar-collapsed');
        setCollapsed(collapsed);
        window.localStorage.setItem('sidebar-collapsed', String(collapsed));
    });
});