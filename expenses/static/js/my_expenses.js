
    (function () {
        const deleteModal = document.getElementById("deleteModal");
        const payModal = document.getElementById("payModal");

        const deleteForm = document.getElementById("deleteExpenseForm");
        const payForm = document.getElementById("payExpenseForm");

        const payModalTitle = document.getElementById("payModalTitle");
        const payModalMessage = document.getElementById("payModalMessage");
        const payConfirmButton = document.getElementById("payConfirmButton");

        const installmentWarning = document.getElementById("deleteInstallmentWarning");

        // Elementos do modal de exclusão
        const deleteModalTitle = document.getElementById("deleteModalTitle");
        const deleteModalMessage = document.getElementById("deleteModalMessage");
        const deleteModalIcon = document.getElementById("deleteModalIcon");
        const deleteModalFinalMessage = document.getElementById("deleteModalFinalMessage");
        const deleteConfirmButton = document.getElementById("deleteConfirmButton");

        if (
            !deleteModal ||
            !payModal ||
            !deleteForm ||
            !payForm ||
            !payModalTitle ||
            !payModalMessage ||
            !payConfirmButton ||
            !installmentWarning ||
            !deleteModalTitle ||
            !deleteModalMessage ||
            !deleteModalIcon ||
            !deleteModalFinalMessage ||
            !deleteConfirmButton
        ) return;

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

                        const isInstallment =
                            btn.dataset.isInstallment === "true";

                        const isRecurringActive =
                            btn.dataset.isRecurringActive === "true";

                        const isRecurring =
                            btn.dataset.isRecurringActive === "true" ||
                            btn.dataset.isRecurringActive === "false";

                        // Exibe o aviso se for uma compra parcelada
                        installmentWarning.hidden = !isInstallment;

                        if (isRecurringActive) {

                            // Cancelamento de recorrência
                            deleteModalTitle.textContent = "Cancelar recorrência";
                            deleteModalMessage.textContent =
                                "Deseja cancelar a recorrência de";

                            deleteModalFinalMessage.hidden = true;
                            deleteConfirmButton.textContent =
                                "Sim, cancelar recorrência";

                            deleteModalIcon.innerHTML =
                                '<i class="fa-solid fa-repeat"></i>';

                        } else if (isRecurring) {

                            // Exclusão de ocorrência cancelada
                            deleteModalTitle.textContent = "Excluir Despesa";
                            deleteModalMessage.textContent =
                                "Deseja excluir definitivamente";

                            deleteModalFinalMessage.hidden = false;
                            deleteConfirmButton.textContent =
                                "Sim, excluir despesa";

                            deleteModalIcon.innerHTML =
                                '<i class="fa-solid fa-trash-can"></i>';

                        } else {

                            // Exclusão normal ou compra parcelada
                            deleteModalTitle.textContent = isInstallment
                                ? "Excluir compra parcelada"
                                : "Excluir despesa";

                            deleteModalMessage.textContent =
                                "Tem certeza que deseja excluir";

                            deleteModalFinalMessage.hidden = false;

                            deleteConfirmButton.textContent = isInstallment
                                ? "Sim, excluir compra"
                                : "Sim, excluir";

                            deleteModalIcon.innerHTML =
                                '<i class="fa-solid fa-trash-can"></i>';
                        }

                        openModal(deleteModal, expenseName);
                    }

                    if (btn.dataset.action === "pay") {
                        payForm.action = btn.dataset.payUrl;

                        const isPaid = btn.dataset.isPaid === "true";

                        if (isPaid) {
                            payModalTitle.textContent = "Desfazer pagamento";
                            payModalMessage.textContent =
                                "Deseja voltar para pendente a despesa";

                            payConfirmButton.textContent =
                                "Sim, voltar para pendente";
                        } else {
                            payModalTitle.textContent = "Informar pagamento";
                            payModalMessage.textContent =
                                "Confirma o pagamento de";

                            payConfirmButton.textContent = "Sim, está pago";
                        }

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

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape") {
                closeModal(deleteModal);
                closeModal(payModal);
            }
        });
    })();
