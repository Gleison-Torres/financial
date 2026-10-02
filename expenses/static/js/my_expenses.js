
(function () {
    const deleteModal = document.getElementById("deleteModal");
    const payModal = document.getElementById("payModal");

    const deleteForm = document.getElementById("deleteExpenseForm");
    const installmentWarning = document.getElementById("deleteInstallmentWarning");

    if (!deleteModal || !payModal || !deleteForm || !installmentWarning) return;

    function openModal(modal, expenseName) {
        const nameEl = modal.querySelector(".modal-card strong");

        if (nameEl) {
            nameEl.textContent = `"${expenseName}"`;
        }

        modal.hidden = false;
    }

    function closeModal(modal) {
        modal.hidden = true;
    }

    document
        .querySelectorAll(".expense-actions [data-action]")
        .forEach(function (btn) {

            btn.addEventListener("click", function () {
                const item = btn.closest(".expense-item");
                const nameEl = item.querySelector(".expense-name");
                const expenseName = nameEl.textContent.trim();

                if (btn.dataset.action === "delete") {

                    // Define para qual despesa o formulário será enviado
                    deleteForm.action = btn.dataset.deleteUrl;

                    // Exibe o aviso se for uma compra parcelada
                    installmentWarning.hidden =
                        btn.dataset.isInstallment !== "true";

                    openModal(deleteModal, expenseName);
                }

                if (btn.dataset.action === "pay") {
                    openModal(payModal, expenseName);
                }
            });
        });

    [deleteModal, payModal].forEach(function (modal) {

        modal.querySelectorAll("[data-close-modal]").forEach(function (btn) {
            btn.addEventListener("click", function () {
                closeModal(modal);
            });
        });

        modal.addEventListener("click", function (event) {
            if (event.target === modal) {
                closeModal(modal);
            }
        });
    });

    // Pagamento ainda não implementado
    payModal.querySelector("[data-confirm-modal]")
        .addEventListener("click", function () {
            closeModal(payModal);
        });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeModal(deleteModal);
            closeModal(payModal);
        }
    });
})();
