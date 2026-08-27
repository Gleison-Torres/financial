
document.addEventListener('DOMContentLoaded', () => {
  // Toggle password visibility
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

      button.setAttribute(
        'aria-label',
        isHidden ? 'Ocultar senha' : 'Mostrar senha'
      );
    });
  });

  // Toggle edit mode for profile fields
  document.querySelectorAll('.edit-btn').forEach((button) => {
    button.addEventListener('click', () => {
      const targetId = button.getAttribute('data-target');
      const input = document.getElementById(targetId);
      if (!input) return;

      const isReadonly = input.hasAttribute('readonly');

      if (isReadonly) {
        input.removeAttribute('readonly');
        input.focus();
        button.classList.add('active');
        const icon = button.querySelector('i');
        if (icon) {
          icon.classList.remove('fa-pen');
          icon.classList.add('fa-check');
        }
      } else {
        input.setAttribute('readonly', '');
        button.classList.remove('active');
        const icon = button.querySelector('i');
        if (icon) {
          icon.classList.remove('fa-check');
          icon.classList.add('fa-pen');
        }
      }
    });
  });

  // Prevent form submission (backend will handle it)
  const form = document.getElementById('profile-form');
  if (form) {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
    });
  }
});
