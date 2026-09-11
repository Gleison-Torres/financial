    const form = document.getElementById("expenseForm");
    const isInstallment = document.getElementById("isInstallment");
    const installmentBox = document.getElementById("installmentBox");
    const installments = document.getElementById("installments");
    const hasInterest = document.getElementById("hasInterest");
    const interestBox = document.getElementById("interestBox");
    const installmentValue = document.getElementById("installmentValue");
    const hint = document.getElementById("installmentHint");

    const list = document.getElementById("expenseList");
    const emptyState = document.getElementById("emptyState");
    const totalValue = document.getElementById("totalValue");

    const brl = (n) =>
      n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

    // ---------- Toggles ----------
    isInstallment.addEventListener("change", () => {
      installmentBox.hidden = !isInstallment.checked;
      if (!isInstallment.checked) {
        hasInterest.checked = false;
        interestBox.hidden = true;
        installmentValue.value = "";
      }
      updateHint();
    });

    hasInterest.addEventListener("change", () => {
      interestBox.hidden = !hasInterest.checked;
      if (!hasInterest.checked) installmentValue.value = "";
      updateHint();
    });

    ["input", "change"].forEach((ev) => {
      document.getElementById("amount").addEventListener(ev, updateHint);
      installments.addEventListener(ev, updateHint);
      installmentValue.addEventListener(ev, updateHint);
    });

    function currentInstallmentValue() {
      const amount = parseFloat(document.getElementById("amount").value) || 0;
      if (!isInstallment.checked) return amount;
      const times = Math.max(2, parseInt(installments.value, 10) || 2);
      if (hasInterest.checked) return parseFloat(installmentValue.value) || 0;
      return amount / times;
    }

    function updateHint() {
      if (!isInstallment.checked) {
        hint.textContent = "";
        return;
      }
      const times = Math.max(2, parseInt(installments.value, 10) || 2);
      const parcela = currentInstallmentValue();
      hint.textContent = parcela > 0 ? `${times}x de ${brl(parcela)}` : "";
    }

    // ---------- Lista ----------
    const expenses = [];

    function render() {
      list.innerHTML = "";
      expenses.forEach((item) => {
        const li = document.createElement("li");
        li.className = "expense-item";

        const info = document.createElement("div");
        info.className = "expense-item-info";

        const title = document.createElement("div");
        title.className = "expense-item-title";
        title.textContent = item.title;

        const meta = document.createElement("div");
        meta.className = "expense-item-meta";

        const date = document.createElement("span");
        date.textContent = item.date;

        const chip = document.createElement("span");
        chip.className = "expense-chip";
        chip.textContent = item.category;

        meta.append(date, chip);

        if (item.installments > 1) {
          const parc = document.createElement("span");
          parc.textContent = `Parcela de ${item.installments}x`;
          meta.append(parc);
        }

        info.append(title, meta);

        const right = document.createElement("div");
        right.className = "expense-item-right";

        const value = document.createElement("span");
        value.className = "expense-item-value";
        value.textContent = brl(item.value);

        const remove = document.createElement("button");
        remove.type = "button";
        remove.className = "expense-remove";
        remove.setAttribute("aria-label", `Remover ${item.title}`);
        remove.innerHTML = '<i class="fa-solid fa-trash-can"></i>';
        remove.addEventListener("click", () => {
          const i = expenses.indexOf(item);
          if (i > -1) expenses.splice(i, 1);
          render();
        });

        right.append(value, remove);
        li.append(info, right);
        list.append(li);
      });

      emptyState.hidden = expenses.length > 0;
      const total = expenses.reduce((sum, e) => sum + e.value, 0);
      totalValue.textContent = brl(total);
    }

    function formatDate(value) {
      if (!value) return "";
      const [y, m, d] = value.split("-");
      return `${d}/${m}/${y}`;
    }

    form.addEventListener("submit", (event) => {
      event.preventDefault();

      const title = document.getElementById("title").value.trim();
      const amount = parseFloat(document.getElementById("amount").value) || 0;
      const date = document.getElementById("date").value;
      const category = document.getElementById("category").value;

      if (!title || amount <= 0 || !date || !category) {
        form.reportValidity();
        return;
      }

      const times = isInstallment.checked
        ? Math.max(2, parseInt(installments.value, 10) || 2)
        : 1;

      // Em compras parceladas, guarda apenas o valor da parcela atual
      const value = currentInstallmentValue();
      if (value <= 0) return;

      expenses.push({
        title,
        value,
        date: formatDate(date),
        category,
        installments: times,
      });

      render();

      form.reset();
      installmentBox.hidden = true;
      interestBox.hidden = true;
      hint.textContent = "";
    });
