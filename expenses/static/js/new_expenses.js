    const amountInput = document.getElementById("amount");

    const isInstallment = document.getElementById("isInstallment");
    const installmentBox = document.getElementById("installmentBox");
    const installments = document.getElementById("installments");

    const hasInterest = document.getElementById("hasInterest");
    const interestBox = document.getElementById("interestBox");
    const installmentValue = document.getElementById("installmentValue");

    const hint = document.getElementById("installmentHint");


    // ==================================================
    // Formatação
    // ==================================================

    const brl = (value) =>
      value.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
      });


    // ==================================================
    // Parcelamento
    // ==================================================

    function updateInstallmentFields(clearValues = false) {
      installmentBox.hidden = !isInstallment.checked;

      if (!isInstallment.checked) {
        if (clearValues) {
          installments.value = "";
          hasInterest.checked = false;
          installmentValue.value = "";
        }

        interestBox.hidden = true;

        installments.required = false;
        installmentValue.required = false;
      } else {
        installments.required = true;

        interestBox.hidden = !hasInterest.checked;
        installmentValue.required = hasInterest.checked;
      }

      updateHint();
    }


    function updateInterestFields(clearValue = false) {
      interestBox.hidden = !hasInterest.checked;

      if (hasInterest.checked) {
        installmentValue.required = true;
      } else {
        if (clearValue) {
          installmentValue.value = "";
        }

        installmentValue.required = false;
      }

      updateHint();
    }


    isInstallment.addEventListener("change", () => {
      updateInstallmentFields(true);
    });


    hasInterest.addEventListener("change", () => {
      updateInterestFields(true);
    });


    ["input", "change"].forEach((eventName) => {
      amountInput.addEventListener(eventName, updateHint);
      installments.addEventListener(eventName, updateHint);
      installmentValue.addEventListener(eventName, updateHint);
    });


    // ==================================================
    // Cálculo da parcela
    // ==================================================

    function currentInstallmentValue() {
      const amount = parseFloat(amountInput.value) || 0;

      const times = parseInt(
        installments.value,
        10
      );

      if (!times || times < 2) {
        return 0;
      }

      if (hasInterest.checked) {
        return parseFloat(
          installmentValue.value
        ) || 0;
      }

      return amount / times;
    }


    function updateHint() {
      if (!isInstallment.checked) {
        hint.textContent = "";
        return;
      }

      const times = parseInt(
        installments.value,
        10
      );

      const value = currentInstallmentValue();

      if (!times || times < 2 || value <= 0) {
        hint.textContent = "";
        return;
      }

      hint.textContent =
        `${times}x de ${brl(value)}`;
    }


    // ==================================================
    // Estado inicial da página
    // ==================================================

    updateInstallmentFields();
    updateInterestFields();