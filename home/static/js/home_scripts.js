    const CATEGORIES = [
      "Alimentação", "Transporte", "Moradia", "Lazer",
      "Saúde", "Educação", "Compras", "Outros",
    ];
    const STORAGE_KEY = "expenses.v1";

    const formatBRL = (n) =>
      n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

    const $ = (id) => document.getElementById(id);

    let expenses = [];
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) expenses = JSON.parse(raw);
    } catch {}

    // Populate categories
    const categorySel = $("category");
    CATEGORIES.forEach((c) => {
      const opt = document.createElement("option");
      opt.value = c;
      opt.textContent = c;
      categorySel.appendChild(opt);
    });

    // Default date today
    $("date").value = new Date().toISOString().slice(0, 10);

    // Installment toggle
    const installmentToggle = $("is-installment");
    const installmentsField = $("installments-field");
    const installmentsInput = $("installments");
    const installmentsHint = $("installments-hint");
    const amountInput = $("amount");

    function updateHint() {
      const value = parseFloat((amountInput.value || "").replace(",", "."));
      const inst = Math.max(2, parseInt(installmentsInput.value) || 2);
      if (installmentToggle.checked && value > 0) {
        installmentsHint.textContent = `${installmentsInput.value}x de ${formatBRL(value / inst)}`;
      } else {
        installmentsHint.textContent = "";
      }
    }

    installmentToggle.addEventListener("change", () => {
      installmentsField.style.display = installmentToggle.checked ? "" : "none";
      updateHint();
    });
    installmentsInput.addEventListener("input", updateHint);
    amountInput.addEventListener("input", updateHint);

    // Render list
    function save() {
      try { localStorage.setItem(STORAGE_KEY, JSON.stringify(expenses)); } catch {}
    }

    function render() {
      const total = expenses.reduce((acc, e) => acc + e.amount, 0);
      $("total").textContent = formatBRL(total);
      $("count").textContent = String(expenses.length);

      const container = $("list-container");
      if (expenses.length === 0) {
        container.innerHTML = `
          <div class="empty">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"/><path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4"/></svg>
            <p>Nenhuma despesa registrada ainda.</p>
          </div>`;
        return;
      }

      const ul = document.createElement("ul");
      ul.className = "expense-list";

      expenses.forEach((e) => {
        const li = document.createElement("li");
        li.className = "expense-item";

        const dateStr = new Date(e.date + "T00:00:00").toLocaleDateString("pt-BR");
        const installmentInfo = e.installments > 1
          ? `<span>${e.installments}x de ${formatBRL(e.amount / e.installments)}</span>`
          : "";

        li.innerHTML = `
          <div class="expense-main">
            <div class="expense-title"></div>
            <div class="expense-meta">
              <span class="chip"></span>
              <span>${dateStr}</span>
              ${installmentInfo}
            </div>
          </div>
          <div class="expense-right">
            <span class="expense-amount">${formatBRL(e.amount)}</span>
            <button type="button" class="icon-btn" aria-label="Remover despesa">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>
            </button>
          </div>`;
        li.querySelector(".expense-title").textContent = e.title;
        li.querySelector(".chip").textContent = e.category;
        li.querySelector(".icon-btn").addEventListener("click", () => {
          expenses = expenses.filter((x) => x.id !== e.id);
          save();
          render();
        });

        ul.appendChild(li);
      });

      container.innerHTML = "";
      container.appendChild(ul);
    }

    $("expense-form").addEventListener("submit", (ev) => {
      ev.preventDefault();
      const title = $("title").value.trim();
      const date = $("date").value;
      const value = parseFloat(($("amount").value || "").replace(",", "."));
      if (!title || !date || isNaN(value) || value <= 0) return;
      const inst = installmentToggle.checked
        ? Math.max(2, parseInt(installmentsInput.value) || 2)
        : 1;

      expenses.unshift({
        id: (crypto.randomUUID && crypto.randomUUID()) || String(Date.now() + Math.random()),
        title,
        date,
        amount: value,
        installments: inst,
        category: categorySel.value,
      });

      save();
      render();

      // reset
      $("title").value = "";
      $("amount").value = "";
      installmentToggle.checked = false;
      installmentsField.style.display = "none";
      installmentsInput.value = "2";
      categorySel.value = CATEGORIES[0];
      installmentsHint.textContent = "";
    });

    render();
