document.addEventListener('DOMContentLoaded', function () {
  const toggleEye = document.getElementById('toggle-eye');
  const passwordInput = document.getElementById('password');
  const eyeIcon = document.getElementById('eye-icon');

  // SVG paths for eye (show) and eye-off (hide)
  const eyeSvg = `
    <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/>
    <circle cx="12" cy="12" r="3"/>
  `;

  const eyeOffSvg = `
    <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24"/>
    <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68"/>
    <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7c.78 0 1.53-.09 2.24-.26"/>
    <path d="M2 2l20 20"/>
  `;

  let showPassword = false;

  toggleEye.addEventListener('click', function () {
    showPassword = !showPassword;

    // Toggle input type
    passwordInput.type = showPassword ? 'text' : 'password';

    // Update aria-label
    toggleEye.setAttribute('aria-label', showPassword ? 'Ocultar senha' : 'Mostrar senha');

    // Swap SVG icon
    eyeIcon.innerHTML = showPassword ? eyeOffSvg : eyeSvg;
  });

  // Prevent actual form submission for demo
  const loginForm = document.getElementById('login-form');
  loginForm.addEventListener('submit', function (e) {
    e.preventDefault();
    // Aqui você pode adicionar a lógica de autenticação
    console.log('Formulário enviado!');
  });
});
