document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('[data-password-toggle]');
    const password = document.querySelector('#id_password');

    if (!toggle || !password) {
        return;
    }

    toggle.addEventListener('click', () => {
        const isHidden = password.type === 'password';
        password.type = isHidden ? 'text' : 'password';
        toggle.setAttribute('aria-label', isHidden ? 'Ocultar contraseña' : 'Mostrar contraseña');
        toggle.classList.toggle('password-is-visible', isHidden);
    });
});
