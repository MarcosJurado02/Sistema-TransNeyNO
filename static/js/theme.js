document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('[data-theme-toggle]');
    const label = document.querySelector('[data-theme-label]');

    if (!toggle || !label) {
        return;
    }

    const setTheme = (theme) => {
        const isDark = theme === 'dark';
        document.documentElement.classList.toggle('dark-theme', isDark);
        document.body.classList.toggle('dark-theme', isDark);
        toggle.setAttribute('aria-pressed', String(isDark));
        toggle.setAttribute('aria-label', isDark ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
        toggle.setAttribute('title', isDark ? 'Cambiar a tema claro' : 'Cambiar a tema oscuro');
        label.textContent = isDark ? 'Tema claro' : 'Tema oscuro';
    };

    setTheme(window.localStorage.getItem('theme') || 'light');

    toggle.addEventListener('click', () => {
        const nextTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
        setTheme(nextTheme);
        window.localStorage.setItem('theme', nextTheme);
    });
});