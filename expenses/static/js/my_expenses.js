// ============================================================
// Minhas despesas — apenas abre/fecha os modais de confirmação
// (Excluir e Informar pagamento).
//
// Os botões "Sim, excluir" e "Sim, está pago" NÃO fazem nada:
// é só o ponto onde você conecta a sua lógica Django
// (fetch para a sua view, ou submit de um form).
// ============================================================

(function () {
  var deleteModal = document.getElementById("deleteModal");
  var payModal = document.getElementById("payModal");

  if (!deleteModal || !payModal) return;

  function openModal(modal, expenseName) {
    var nameEl = modal.querySelector(".modal-card strong");
    if (nameEl && expenseName) {
      nameEl.textContent = '"' + expenseName + '"';
    }
    modal.hidden = false;
  }

  function closeModal(modal) {
    modal.hidden = true;
  }

  // Botões de ação dentro de cada despesa da lista
  document
    .querySelectorAll(".expense-actions [data-action]")
    .forEach(function (btn) {
      btn.addEventListener("click", function () {
        var item = btn.closest(".expense-item");
        var nameEl = item ? item.querySelector(".expense-name") : null;
        var name = nameEl ? nameEl.textContent.trim() : "";

        if (btn.dataset.action === "delete") openModal(deleteModal, name);
        if (btn.dataset.action === "pay") openModal(payModal, name);
      });
    });

  // Fechar: botão Cancelar, botão de confirmar (sem ação) e clique no overlay
  [deleteModal, payModal].forEach(function (modal) {
    modal
      .querySelectorAll("[data-close-modal], [data-confirm-modal]")
      .forEach(function (btn) {
        btn.addEventListener("click", function () {
          // PONTO DE INTEGRAÇÃO: se o botão for de confirmação
          // (btn.hasAttribute("data-confirm-modal")), trate aqui
          // a chamada ao seu backend antes de fechar o modal.
          closeModal(modal);
        });
      });

    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeModal(modal);
    });
  });

  // Tecla Esc fecha qualquer modal aberto
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      if (!deleteModal.hidden) closeModal(deleteModal);
      if (!payModal.hidden) closeModal(payModal);
    }
  });
})();
