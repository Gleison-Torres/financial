document.addEventListener("DOMContentLoaded", function () {
    const chartCanvas = document.getElementById("categoryChart");
    const dataElement = document.getElementById("expenses-category-data");
    const legendContainer = document.getElementById("categoryLegend");

    if (!chartCanvas || !dataElement || !legendContainer) {
        return;
    }

    const expenses = JSON.parse(dataElement.textContent);

    if (!expenses.length) {
        return;
    }

    const labels = expenses.map(item => item.category);
    const values = expenses.map(item => item.total);

    const colors = [
        "#568FDC",
        "#9B82DD",
        "#2BB98D",
        "#D568A8",
        "#E7A65D",
        "#38BDF8",
        "#F87171",
        "#A3E635"
    ];

    const currencyFormatter = new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL"
    });

    const totalExpenses = values.reduce(
        (total, value) => total + value,
        0
    );

    new Chart(chartCanvas, {
        type: "doughnut",

        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors.slice(0, values.length),
                borderWidth: 0,
                hoverOffset: 6
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "60%",

            plugins: {
                legend: {
                    display: false
                },

                tooltip: {
                    enabled: false,

                    external: function (context) {
                        const tooltip = context.tooltip;
                        const tooltipElement = document.getElementById("categoryTooltip");

                        if (!tooltipElement) {
                            return;
                        }

                        if (tooltip.opacity === 0) {
                            tooltipElement.style.display = "none";
                            return;
                        }

                        const item = tooltip.dataPoints[0];

                        if (!item) {
                            tooltipElement.style.display = "none";
                            return;
                        }

                        const percentage = totalExpenses > 0
                            ? (item.parsed / totalExpenses) * 100
                            : 0;

                        tooltipElement.replaceChildren();

                        const category = document.createElement("strong");
                        category.textContent = item.label;

                        const amount = document.createElement("span");
                        amount.textContent = currencyFormatter.format(item.parsed);

                        const percent = document.createElement("span");
                        percent.textContent =
                            percentage.toLocaleString("pt-BR", {
                                maximumFractionDigits: 1
                            }) + "%";

                        tooltipElement.append(category, amount, percent);
                        tooltipElement.style.display = "flex";
                    }
                }
            }
        }
    });

    expenses.forEach((expense, index) => {
        const percentage = totalExpenses > 0
            ? (expense.total / totalExpenses) * 100
            : 0;

        const item = document.createElement("div");
        item.className = "category-legend-item";

        const color = document.createElement("span");
        color.className = "category-legend-color";
        color.style.backgroundColor = colors[index];

        const name = document.createElement("span");
        name.className = "category-legend-name";
        name.textContent = expense.category;

        const value = document.createElement("span");
        value.className = "category-legend-value";
        value.textContent = percentage.toLocaleString("pt-BR", {
            maximumFractionDigits: 1
        }) + "%";

        item.append(color, name, value);
        legendContainer.appendChild(item);
    });
});