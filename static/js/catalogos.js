document.addEventListener('DOMContentLoaded', () => {
    const dialog = document.querySelector('[data-confirm-dialog]');
    let pendingForm = null;

    document.querySelectorAll('[data-confirm-delete]').forEach((form) => {
        form.addEventListener('submit', (event) => {
            if (form.dataset.confirmed === 'true') {
                delete form.dataset.confirmed;
                return;
            }
            event.preventDefault();
            pendingForm = form;
            dialog.hidden = false;
        });
    });

    document.querySelector('[data-confirm-cancel]')?.addEventListener('click', () => {
        dialog.hidden = true;
        pendingForm = null;
    });

    document.querySelector('[data-confirm-accept]')?.addEventListener('click', () => {
        if (!pendingForm) return;
        pendingForm.dataset.confirmed = 'true';
        dialog.hidden = true;
        pendingForm.requestSubmit();
    });

    dialog?.addEventListener('click', (event) => {
        if (event.target === dialog) {
            dialog.hidden = true;
            pendingForm = null;
        }
    });

    document.querySelectorAll('.catalog-message-close').forEach((button) => {
        button.addEventListener('click', () => button.parentElement.remove());
    });

    window.setTimeout(() => {
        document.querySelectorAll('.catalog-message').forEach((message) => message.classList.add('catalog-message-hidden'));
    }, 5000);
});