// Seleção dos elementos do DOM
const expenseForm = document.getElementById('expense-form');
const expenseList = document.getElementById('expense-list');
const totalAmountElement = document.getElementById('total-amount');

// Array para armazenar as despesas (Estado da aplicação)
let expenses = [];

// Função para formatar moeda para Real (BRL)
function formatCurrency(value) {
    return value.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

// Função para formatar a data (AAAA-MM-DD para DD/MM/AAAA)
function formatDate(dateString) {
    const [year, month, day] = dateString.split('-');
    return `${day}/${month}/${year}`;
}

// Função para atualizar a exibição da tabela e o total
function updateUI() {
    // Limpa a tabela antes de renderizar
    expenseList.innerHTML = '';

    let total = 0;

    // Itera sobre o array de despesas e cria as linhas da tabela
    expenses.forEach((expense, index) => {
        total += expense.valor;

        // Verifica se a descrição está vazia. Se sim, define o texto padrão.
        const temDescricao = expense.descricao && expense.descricao.trim() !== "";
        const textoDescricao = temDescricao ? expense.descricao : "Sem descrição";

        // Se não tiver descrição, aplica uma classe CSS para deixar o texto cinza
        const estiloDescricao = temDescricao ? "" : "class='no-description'";

        const row = document.createElement('tr');

        row.innerHTML = `
            <td>${expense.titulo}</td>
            <td style="color: #0066cc; font-weight: 600;">${formatCurrency(expense.valor)}</td>
            <td><span class="category-badge">${expense.categoria}</span></td>
            <td>${formatDate(expense.data)}</td>
            <td ${estiloDescricao}>${textoDescricao}</td> <td class="actions-col">
                <button class="btn-delete" onclick="deleteExpense(${index})" title="Excluir despesa">
                    <i class="fa-solid fa-trash-can"></i>
                </button>
            </td>
        `;

        expenseList.appendChild(row);
    });

    // Atualiza o valor total na interface
    totalAmountElement.textContent = formatCurrency(total);
}

// Evento de submissão do formulário
expenseForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o recarregamento da página

    // Captura os valores dos campos
    const titulo = document.getElementById('titulo').value;
    const valor = parseFloat(document.getElementById('valor').value);
    const categoria = document.getElementById('categoria').value;
    const data = document.getElementById('data').value;
    const descricao = document.getElementById('descricao').value;

    // Validação básica (o HTML 'required' já ajuda)
    if (!titulo || isNaN(valor) || !categoria || !data) {
        alert("Por favor, preencha todos os campos obrigatórios (*).");
        return;
    }

    // Cria o objeto da nova despesa
    const newExpense = {
        titulo,
        valor,
        categoria,
        data,
        descricao
    };

    // Adiciona ao array
    expenses.push(newExpense);

    // Atualiza a interface
    updateUI();

    // Limpa o formulário
    expenseForm.reset();
});

// Função para deletar uma despesa baseada no índice
function deleteExpense(index) {
    // Confirmação simples antes de deletar
    if (confirm(`Tem certeza que deseja excluir a despesa "${expenses[index].titulo}"?`)) {
        // Remove o item do array
        expenses.splice(index, 1);

        // Atualiza a interface
        updateUI();
    }
}