// Alterar senha — apenas a funcionalidade do olho para mostrar/ocultar a senha.
// O botão "Alterar senha" não executa ação; a lógica será implementada no backend.

document.addEventListener('DOMContentLoaded', () => {
  const toggles = document.querySelectorAll('.toggle-password');

  toggles.forEach((button) => {
    button.addEventListener('click', () => {
      const targetId = button.getAttribute('data-target');
      const input = document.getElementById(targetId);
      const icon = button.querySelector('i');

      if (!input || !icon) return;

      const isPassword = input.type === 'password';
      input.type = isPassword ? 'text' : 'password';

      icon.classList.toggle('fa-eye', !isPassword);
      icon.classList.toggle('fa-eye-slash', isPassword);

      button.setAttribute('aria-label', isPassword ? 'Ocultar senha' : 'Mostrar senha');
    });
  });
});