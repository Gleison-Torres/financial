// Botões de lápis dentro dos inputs: habilitam/desabilitam a edição de cada campo individualmente
// Os botões "Salvar alterações" e "Alterar senha" permanecem sem funcionalidade para integração com o backend.

document.addEventListener('DOMContentLoaded', () => {
  const toggles = document.querySelectorAll('.edit-field-toggle');

  toggles.forEach((button) => {
    button.addEventListener('click', () => {
      const targetId = button.getAttribute('data-target');
      const input = document.getElementById(targetId);
      const icon = button.querySelector('i');

      if (!input) return;

      const isReadonly = input.hasAttribute('readonly');

      if (isReadonly) {
        input.removeAttribute('readonly');
        input.focus();
        button.classList.add('is-editing');
        if (icon) {
          icon.classList.remove('fa-pencil');
          icon.classList.add('fa-check');
        }
      } else {
        input.setAttribute('readonly', '');
        input.blur();
        button.classList.remove('is-editing');
        if (icon) {
          icon.classList.remove('fa-check');
          icon.classList.add('fa-pencil');
        }
      }
    });
  });
});
