document.addEventListener('DOMContentLoaded', () => {
    const dialog = document.querySelector('[data-printer-dialog]');
    const reason = document.querySelector('#printer-retire-reason');
    let pendingForm = null;

    document.querySelectorAll('[data-printer-confirm]').forEach((form) => {
        form.addEventListener('submit', (event) => {
            if (form.dataset.confirmed === 'true') {
                delete form.dataset.confirmed;
                return;
            }
            event.preventDefault();
            pendingForm = form;
            dialog.hidden = false;
            reason.value = '';
        });
    });

    document.querySelector('[data-printer-cancel]')?.addEventListener('click', () => {
        dialog.hidden = true;
        pendingForm = null;
    });

    document.querySelector('[data-printer-accept]')?.addEventListener('click', () => {
        if (!pendingForm) return;
        if (!reason.value.trim()) {
            reason.focus();
            return;
        }
        pendingForm.querySelector('input[name="motivo_baja"]')?.remove();
        const hiddenReason = document.createElement('input');
        hiddenReason.type = 'hidden';
        hiddenReason.name = 'motivo_baja';
        hiddenReason.value = reason.value.trim();
        pendingForm.appendChild(hiddenReason);
        pendingForm.dataset.confirmed = 'true';
        dialog.hidden = true;
        pendingForm.requestSubmit();
    });
});