    /*
      Navegação entre meses + renderização das despesas.
      Os dados abaixo são apenas de exemplo (frontend).
      No Django, substitua "dadosExemplo" pelos dados vindos do backend.
    */

    const MESES = [
      "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
      "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
    ];

    // chave: "ano-mes" (mes 0..11)
    const dadosExemplo = {
      "2026-7": {
        despesas: [
          { titulo: "Internet", data: "05/08/2026", categoria: "Casa", valor: 120 },
          { titulo: "Supermercado", data: "12/08/2026", categoria: "Alimentação", valor: 540.9 },
          { titulo: "Notebook", data: "15/08/2026", categoria: "Eletrônicos", valor: 416.25, parcela: 3, parcelas: 8, total: 3330 },
        ],
      },
      "2026-8": {
        despesas: [
          { titulo: "Internet", data: "05/09/2026", categoria: "Casa", valor: 120 },
          { titulo: "Energia", data: "08/09/2026", categoria: "Casa", valor: 185.4 },
          { titulo: "Supermercado", data: "10/09/2026", categoria: "Alimentação", valor: 612.3 },
          { titulo: "Academia", data: "12/09/2026", categoria: "Saúde", valor: 100 },
          { titulo: "Notebook", data: "15/09/2026", categoria: "Eletrônicos", valor: 416.25, parcela: 4, parcelas: 8, total: 3330 },
          { titulo: "Sofá", data: "18/09/2026", categoria: "Casa", valor: 249.9, parcela: 2, parcelas: 10, total: 2499 },
        ],
      },
      "2026-9": {
        despesas: [
          { titulo: "Internet", data: "05/10/2026", categoria: "Casa", valor: 120 },
          { titulo: "Notebook", data: "15/10/2026", categoria: "Eletrônicos", valor: 416.25, parcela: 5, parcelas: 8, total: 3330 },
        ],
      },
    };

    const brl = (v) =>
      v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

    const hoje = new Date();
    let mesAtual = hoje.getMonth();
    let anoAtual = hoje.getFullYear();

    const el = (id) => document.getElementById(id);

    function renderizar() {
      const chave = `${anoAtual}-${mesAtual}`;
      const despesas = (dadosExemplo[chave] && dadosExemplo[chave].despesas) || [];

      // Rótulos de navegação
      const anterior = new Date(anoAtual, mesAtual - 1, 1);
      const proximo = new Date(anoAtual, mesAtual + 1, 1);
      el("prevMonthLabel").textContent = MESES[anterior.getMonth()];
      el("nextMonthLabel").textContent = MESES[proximo.getMonth()];
      el("currentMonthLabel").textContent = `${MESES[mesAtual]} ${anoAtual}`;
      el("listMonthLabel").textContent = MESES[mesAtual];

      // Total do mês
      const total = despesas.reduce((soma, d) => soma + d.valor, 0);
      el("monthTotal").textContent = brl(total);
      el("monthCount").textContent =
        despesas.length === 1 ? "1 despesa" : `${despesas.length} despesas`;

      // Lista
      const lista = el("expenseList");
      lista.innerHTML = "";
      el("emptyState").hidden = despesas.length > 0;

      despesas.forEach((d) => {
        const item = document.createElement("li");
        item.className = "expense-item";
        item.innerHTML = `
          <div class="expense-info">
            <span class="expense-name">${d.titulo}</span>
            <span class="expense-meta">
              <span class="expense-category">${d.categoria}</span>
              <span>${d.data}</span>
              ${d.parcelas ? `<span class="expense-tag-installment">${d.parcela}/${d.parcelas}</span>` : ""}
            </span>
          </div>
          <span class="expense-value">${brl(d.valor)}</span>
        `;
        lista.appendChild(item);
      });

      // Cards de compras parceladas
      const parceladas = despesas.filter((d) => d.parcelas);
      const grid = el("installmentGrid");
      grid.innerHTML = "";
      el("emptyInstallments").hidden = parceladas.length > 0;

      parceladas.forEach((d) => {
        const progresso = Math.round((d.parcela / d.parcelas) * 100);
        const card = document.createElement("article");
        card.className = "installment-card";
        card.innerHTML = `
          <div class="installment-top">
            <span class="installment-name">${d.titulo}</span>
            <span class="installment-badge">${d.parcela}/${d.parcelas}</span>
          </div>
          <div class="installment-value">
            ${brl(d.valor)}
            <small>Valor da parcela</small>
          </div>
          <div class="installment-bar"><span style="width:${progresso}%"></span></div>
          <div class="installment-footer">
            <span>Total da compra</span>
            <span class="installment-total">${brl(d.total)}</span>
          </div>
        `;
        grid.appendChild(card);
      });
    }

    el("prevMonth").addEventListener("click", () => {
      const d = new Date(anoAtual, mesAtual - 1, 1);
      mesAtual = d.getMonth();
      anoAtual = d.getFullYear();
      renderizar();
    });

    el("nextMonth").addEventListener("click", () => {
      const d = new Date(anoAtual, mesAtual + 1, 1);
      mesAtual = d.getMonth();
      anoAtual = d.getFullYear();
      renderizar();
    });

    renderizar();
