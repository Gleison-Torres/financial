(function () {
  "use strict";

  const form = document.getElementById("register-form");
  const cpfInput = document.getElementById("cpf");

  // -------- Máscara de CPF --------
  cpfInput.addEventListener("input", function (e) {
    let v = e.target.value.replace(/\D/g, "").slice(0, 11);
    if (v.length > 9) {
      v = v.replace(/^(\d{3})(\d{3})(\d{3})(\d{0,2}).*/, "$1.$2.$3-$4");
    } else if (v.length > 6) {
      v = v.replace(/^(\d{3})(\d{3})(\d{0,3}).*/, "$1.$2.$3");
    } else if (v.length > 3) {
      v = v.replace(/^(\d{3})(\d{0,3}).*/, "$1.$2");
    }
    e.target.value = v;
  });

  // -------- Validação de CPF (algoritmo oficial) --------
  function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, "");
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;
    let soma = 0;
    for (let i = 0; i < 9; i++) soma += parseInt(cpf[i]) * (10 - i);
    let d1 = (soma * 10) % 11;
    if (d1 === 10) d1 = 0;
    if (d1 !== parseInt(cpf[9])) return false;
    soma = 0;
    for (let i = 0; i < 10; i++) soma += parseInt(cpf[i]) * (11 - i);
    let d2 = (soma * 10) % 11;
    if (d2 === 10) d2 = 0;
    return d2 === parseInt(cpf[10]);
  }

  function validarEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
  }

  function setError(fieldId, message) {
    const errEl = document.getElementById("err-" + fieldId);
    const field = document.getElementById(fieldId).closest(".field");
    if (message) {
      errEl.textContent = message;
      field.classList.add("has-error");
    } else {
      errEl.textContent = "";
      field.classList.remove("has-error");
    }
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const nome = document.getElementById("nome").value.trim();
    const sexo = document.getElementById("sexo").value;
    const cpf = document.getElementById("cpf").value;
    const email = document.getElementById("email").value.trim();

    let ok = true;

    if (nome.length < 3 || !nome.includes(" ")) {
      setError("nome", "Informe seu nome completo.");
      ok = false;
    } else setError("nome", "");

    if (!sexo) {
      setError("sexo", "Selecione uma opção.");
      ok = false;
    } else setError("sexo", "");

    if (!validarCPF(cpf)) {
      setError("cpf", "CPF inválido.");
      ok = false;
    } else setError("cpf", "");

    if (!validarEmail(email)) {
      setError("email", "E-mail inválido.");
      ok = false;
    } else setError("email", "");

    if (!ok) return;

    // Sucesso — envie via fetch para o Django ou deixe o form submeter
    console.log("Cadastro válido:", { nome, sexo, cpf, email });
    alert("Cadastro realizado com sucesso!");
    form.reset();
  });
})();