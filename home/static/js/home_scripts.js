    document.addEventListener('DOMContentLoaded', () => {

      // ---------- Referências ----------
      const form = document.getElementById('formDespesa');

      const inputTitulo = document.getElementById('titulo');
      const inputValor = document.getElementById('valor');
      const inputData = document.getElementById('data');
      const inputCategoria = document.getElementById('categoria');

      const btnParcelado = document.getElementById('btnParcelado');
      const parceladoBox = document.getElementById('parceladoBox');
      const inputNumParcelas = document.getElementById('numParcelas');

      const btnJuros = document.getElementById('btnJuros');
      const jurosBox = document.getElementById('jurosBox');
      const inputValorParcela = document.getElementById('valorParcela');

      const listaDespesas = document.getElementById('listaDespesas');
      const emptyState = document.getElementById('emptyState');
      const totalValorEl = document.getElementById('totalValor');
      const btnSalvar = document.getElementById('btnSalvar');

      // ---------- Estado ----------
      let despesas = [];
      let proximoId = 1;

      const categoriasLabel = {
        alimentacao: 'Alimentação',
        transporte: 'Transporte',
        moradia: 'Moradia',
        saude: 'Saúde',
        lazer: 'Lazer',
        educacao: 'Educação',
        outros: 'Outros',
      };

      const formatarMoeda = (valor) =>
        new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor || 0);

      // Recebe uma data no formato "YYYY-MM-DD" (padrão do <input type="date">)
      // e devolve "DD/MM/AAAA" para exibição, sem problemas de fuso horário.
      const formatarData = (dataISO) => {
        if (!dataISO) return '';
        const [ano, mes, dia] = dataISO.split('-');
        return `${dia}/${mes}/${ano}`;
      };

      // Preenche o campo de data com a data de hoje por padrão
      const hoje = new Date();
      const hojeISO = new Date(hoje.getTime() - hoje.getTimezoneOffset() * 60000)
        .toISOString()
        .slice(0, 10);
      inputData.value = hojeISO;
      inputData.max = hojeISO; // evita lançar despesas com data futura, se não fizer sentido no seu fluxo

      // ---------- Toggles ----------
      function alternarToggle(botao, caixa, aoFechar) {
        const ativo = botao.getAttribute('aria-pressed') === 'true';
        const novoEstado = !ativo;
        botao.setAttribute('aria-pressed', String(novoEstado));
        caixa.hidden = !novoEstado;
        if (!novoEstado && typeof aoFechar === 'function') aoFechar();
      }

      btnParcelado.addEventListener('click', () => {
        alternarToggle(btnParcelado, parceladoBox, () => {
          inputNumParcelas.value = '';
          // fechar juros também, já que não faz sentido sem parcelamento
          btnJuros.setAttribute('aria-pressed', 'false');
          jurosBox.hidden = true;
          inputValorParcela.value = '';
        });
      });

      btnJuros.addEventListener('click', () => {
        alternarToggle(btnJuros, jurosBox, () => {
          inputValorParcela.value = '';
        });
      });

      // ---------- Adicionar despesa ----------
      form.addEventListener('submit', (evento) => {
        evento.preventDefault();

        const titulo = inputTitulo.value.trim();
        const valor = parseFloat(inputValor.value);
        const data = inputData.value;
        const categoria = inputCategoria.value;
        const parcelado = btnParcelado.getAttribute('aria-pressed') === 'true';
        const temJuros = btnJuros.getAttribute('aria-pressed') === 'true';

        if (!titulo || isNaN(valor) || valor <= 0 || !data || !categoria) {
          alert('Preencha título, valor, data e categoria corretamente.');
          return;
        }

        let numParcelas = null;
        let valorParcela = null;
        let valorTotal = valor;

        if (parcelado) {
          numParcelas = parseInt(inputNumParcelas.value, 10);
          if (!numParcelas || numParcelas < 2) {
            alert('Informe em quantas parcelas foi dividido (mínimo 2).');
            return;
          }

          if (temJuros) {
            valorParcela = parseFloat(inputValorParcela.value);
            if (isNaN(valorParcela) || valorParcela <= 0) {
              alert('Informe o valor de cada parcela.');
              return;
            }
            // com juros, o valor efetivamente pago é a soma das parcelas
            valorTotal = valorParcela * numParcelas;
          } else {
            valorParcela = valor / numParcelas;
          }
        }

        despesas.push({
          id: proximoId++,
          titulo,
          data,
          categoria,
          valorTotal,
          parcelado,
          numParcelas,
          temJuros,
          valorParcela,
        });

        renderizarLista();
        form.reset();
        inputData.value = hojeISO;
        parceladoBox.hidden = true;
        jurosBox.hidden = true;
        btnParcelado.setAttribute('aria-pressed', 'false');
        btnJuros.setAttribute('aria-pressed', 'false');
        inputTitulo.focus();
      });

      // ---------- Renderização ----------
      function renderizarLista() {
        listaDespesas.innerHTML = '';

        if (despesas.length === 0) {
          listaDespesas.appendChild(emptyState);
          totalValorEl.textContent = formatarMoeda(0);
          return;
        }

        let total = 0;

        // Mostra as despesas em ordem cronológica (mais antiga primeiro)
        const despesasOrdenadas = [...despesas].sort((a, b) => a.data.localeCompare(b.data));

        despesasOrdenadas.forEach((despesa) => {
          total += despesa.valorTotal;

          const item = document.createElement('li');
          item.className = 'receipt-item';
          item.dataset.id = despesa.id;

          const parcelasInfo = despesa.parcelado
            ? `<div class="item-installments">${despesa.numParcelas}x de ${formatarMoeda(despesa.valorParcela)}${despesa.temJuros ? ' · com juros' : ' · sem juros'}</div>`
            : '';

          item.innerHTML = `
            <div class="item-main">
              <span class="item-title">${escapeHtml(despesa.titulo)}</span>
              <div class="item-meta">
                <span class="item-date">${formatarData(despesa.data)}</span>
                <span class="item-tag">${categoriasLabel[despesa.categoria] || despesa.categoria}</span>
              </div>
              ${parcelasInfo}
            </div>
            <div class="item-right">
              <span class="item-value">${formatarMoeda(despesa.valorTotal)}</span>
              <button type="button" class="btn-delete" title="Excluir despesa" aria-label="Excluir despesa">🗑</button>
            </div>
          `;

          item.querySelector('.btn-delete').addEventListener('click', () => {
            despesas = despesas.filter((d) => d.id !== despesa.id);
            renderizarLista();
          });

          listaDespesas.appendChild(item);
        });

        totalValorEl.textContent = formatarMoeda(total);
      }

      function escapeHtml(texto) {
        const div = document.createElement('div');
        div.textContent = texto;
        return div.innerHTML;
      }

      // ---------- Salvar despesas ----------
      // Sem funcionalidade por enquanto — a integração com o backend
      // (envio para a view Django, CSRF, etc.) fica por conta do usuário.
      btnSalvar.addEventListener('click', () => {
        // TODO: implementar o salvamento das despesas.
        // O array `despesas` já está pronto para ser enviado (ex.: via fetch/JSON).
      });

      // Estado inicial
      renderizarLista();
    });