document.addEventListener('DOMContentLoaded', () => {
  const toggleEye = document.getElementById('toggle-eye');
  const passwordInput = document.getElementById('password');
  const eyeIcon = document.getElementById('eye-icon');

  toggleEye.addEventListener('click', () => {
    const isHidden = passwordInput.type === 'password';
    passwordInput.type = isHidden ? 'text' : 'password';
    toggleEye.setAttribute('aria-label', isHidden ? 'Ocultar senha' : 'Mostrar senha');
    eyeIcon.innerHTML = isHidden
      ? `<path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/><path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/><path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7c.78 0 1.53-.09 2.24-.26"/><path d="M2 2l20 20"/>`
      : `<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>`;
  });
});