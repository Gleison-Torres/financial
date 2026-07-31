document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.toggle-password').forEach((button) => {
    button.addEventListener('click', () => {
      const targetId = button.getAttribute('data-target');
      const input = document.getElementById(targetId);
      if (!input) return;

      const isHidden = input.type === 'password';
      input.type = isHidden ? 'text' : 'password';

      const icon = button.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-eye', !isHidden);
        icon.classList.toggle('fa-eye-slash', isHidden);
      }
    });
  });
});
