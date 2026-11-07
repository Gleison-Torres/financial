
(function () {
  "use strict";

  // ----------------------------------------
  // CONFIGURAÇÕES
  // ----------------------------------------

  var categories = [
    "Alimentação",
    "Transporte",
    "Moradia",
    "Lazer",
    "Saúde",
    "Educação",
    "Compras",
    "Outros"
  ];

  var colorOf = {
    "Alimentação": "#38bdf8",
    "Transporte": "#a855f7",
    "Moradia": "#9B82DD",
    "Lazer": "#568FDC",
    "Saúde": "#E7A65D",
    "Educação": "#D568A8",
    "Compras": "#fb923c",
    "Outros": "#2BB98D"
  };

  // ----------------------------------------
  // ELEMENTOS HTML
  // ----------------------------------------

  var $ = function (id) {
    return document.getElementById(id);
  };

  var legend = $("categoryLegend");
  var totalEl = $("categoryTotal");
  var list = $("resultList");
  var count = $("resultCount");
  var selCat = $("filterCategory");

  var filterForm = $("filterForm");
  var filterClear = $("filterClear");

  var nameInput = $("filterName");
  var startInput = $("filterStart");
  var endInput = $("filterEnd");

  // ----------------------------------------
  // PARÂMETROS DA URL
  // ----------------------------------------

  var params = new URLSearchParams(window.location.search);

  var currentYear = params.get("year");
  var currentMonth = params.get("month");

  // ----------------------------------------
  // DADOS VINDOS DO DJANGO
  // ----------------------------------------

  var dataEl = $("expensesData");
  var all = [];

  try {
    var parsed = dataEl
      ? JSON.parse(dataEl.textContent)
      : [];

    if (Array.isArray(parsed)) {
      all = parsed;
    }

  } catch (error) {
    console.error("Erro ao carregar as despesas:", error);
  }

  all = all.map(function (expense) {
    return {
      title: expense.title || "",
      category: expense.category || "Outros",
      date: expense.date || "",
      amount: Number(expense.amount) || 0,
      is_paid: expense.is_paid
    };
  });

  // O Django já entrega os resultados filtrados.
  // Não aplicamos outro filtro localmente.
  var filtered = all.slice();

  var hidden = new Set();
  var chart = null;

  // ----------------------------------------
  // FORMATAÇÃO
  // ----------------------------------------

  function brl(value) {
    return Number(value || 0).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL"
    });
  }

  function brDate(value) {
    if (!value) return "";

    var parts = value.split("-");

    if (parts.length !== 3) return value;

    return parts[2] + "/" + parts[1] + "/" + parts[0];
  }

  // ----------------------------------------
  // RECUPERAR FILTROS DA URL
  // ----------------------------------------

  if (nameInput) {
    nameInput.value = params.get("q") || "";
  }

  if (startInput) {
    startInput.value = params.get("start") || "";
  }

  if (endInput) {
    endInput.value = params.get("end") || "";
  }

  // ----------------------------------------
  // PREENCHER FILTRO DE CATEGORIAS
  // ----------------------------------------

  if (selCat) {
    var selectedCategory = params.get("category") || "";

    categories.forEach(function (category) {
      var option = document.createElement("option");

      option.value = category;
      option.textContent = category;

      if (category === selectedCategory) {
        option.selected = true;
      }

      selCat.appendChild(option);
    });
  }

  // ----------------------------------------
  // PRESERVAR MÊS E ANO NO FORMULÁRIO
  // ----------------------------------------

  if (filterForm) {
    if (currentYear && currentMonth) {
      var yearInput = document.createElement("input");

      yearInput.type = "hidden";
      yearInput.name = "year";
      yearInput.value = currentYear;

      filterForm.appendChild(yearInput);

      var monthInput = document.createElement("input");

      monthInput.type = "hidden";
      monthInput.name = "month";
      monthInput.value = currentMonth;

      filterForm.appendChild(monthInput);
    }

    // Validação básica do intervalo.
    // O envio continua sendo feito normalmente ao Django.
    filterForm.addEventListener("submit", function (event) {
      var start = startInput ? startInput.value : "";
      var end = endInput ? endInput.value : "";

      if ((start && !end) || (!start && end)) {
        event.preventDefault();

        alert("Informe a data inicial e a data final.");

        return;
      }

      if (start && end && start > end) {
        event.preventDefault();

        alert("A data inicial não pode ser maior que a data final.");
      }
    });
  }

  // ----------------------------------------
  // BOTÃO LIMPAR
  // ----------------------------------------

  if (filterClear) {
    filterClear.addEventListener("click", function () {
      var url = window.location.pathname;

      // Preserva o mês selecionado na navegação.
      if (currentYear && currentMonth) {
        url += "?year=" + encodeURIComponent(currentYear) +
          "&month=" + encodeURIComponent(currentMonth);
      }

      window.location.href = url;
    });
  }

  // ----------------------------------------
  // AGRUPAR DESPESAS POR CATEGORIA
  // ----------------------------------------

  function groupByCategory(rows) {
    var map = {};

    rows.forEach(function (expense) {
      map[expense.category] =
        (map[expense.category] || 0) + expense.amount;
    });

    return Object.keys(map).map(function (category) {
      return {
        category: category,
        total: map[category]
      };
    }).sort(function (a, b) {
      return b.total - a.total;
    });
  }

  // ----------------------------------------
  // RENDERIZAR PÁGINA
  // ----------------------------------------

  function render() {
    var groups = groupByCategory(filtered);

    var visible = groups.filter(function (group) {
      return !hidden.has(group.category);
    });

    // Total de todas as categorias.
    var fullTotal = groups.reduce(function (sum, group) {
      return sum + group.total;
    }, 0);

    var visibleTotal = visible.reduce(function (sum, group) {
      return sum + group.total;
    }, 0);

    // Legenda do gráfico.
    if (legend) {
      legend.innerHTML = "";

      groups.forEach(function (group) {
        var off = hidden.has(group.category);

        // A porcentagem sempre considera o total completo.
        var pct = fullTotal
          ? " (" + (
              group.total / fullTotal * 100
            ).toFixed(1).replace(".", ",") + "%)"
          : "";

        var li = document.createElement("li");

        li.innerHTML =
          '<button type="button" class="cat-legend-item' +
          (off ? " is-off" : "") +
          '" aria-pressed="' + !off + '">' +

          '<span class="cat-swatch" style="background:' +
          (colorOf[group.category] || "#94a3b8") +
          '"></span>' +

          '<span class="cat-legend-name"></span>' +

          '<span class="cat-legend-value">' +
          (off ? "" : brl(group.total)) +
          "</span></button>";

        li.querySelector(".cat-legend-name").textContent =
          group.category + pct;

        li.firstChild.addEventListener("click", function () {
          if (off) {
            hidden.delete(group.category);
          } else {
            hidden.add(group.category);
          }

          render();
        });

        legend.appendChild(li);
      });
    }

    // Total exibido.
    if (totalEl) {
      totalEl.textContent = hidden.size
        ? brl(visibleTotal) + " (" + brl(fullTotal) + " com todas)"
        : brl(fullTotal);
    }

    // Estado vazio do gráfico.
    var chartEmpty = $("chartEmpty");

    if (chartEmpty) {
      chartEmpty.hidden = visible.length > 0;
    }

    drawChart(visible);
    renderList();
  }

  // ----------------------------------------
  // GRÁFICO DO CHART.JS
  // ----------------------------------------

  function drawChart(groups) {
    if (typeof Chart === "undefined") {
      console.error("Chart.js não foi carregado.");
      return;
    }

    var canvas = $("categoryChart");

    if (!canvas) return;

    var config = {
      labels: groups.map(function (group) {
        return group.category;
      }),

      datasets: [{
        data: groups.map(function (group) {
          return group.total;
        }),

        backgroundColor: groups.map(function (group) {
          return colorOf[group.category] || "#94a3b8";
        }),

        borderColor: "rgba(15, 23, 42, .9)",
        borderWidth: 3,
        hoverOffset: 8
      }]
    };

    if (chart) {
      chart.data = config;
      chart.update();
      return;
    }

    chart = new Chart(canvas, {
      type: "doughnut",
      data: config,

      options: {
        cutout: "55%",
        maintainAspectRatio: false,

        plugins: {
          legend: {
            display: false
          },

          tooltip: {
            callbacks: {
              label: function (context) {
                return " " + context.label + ": " +
                  brl(context.parsed);
              }
            }
          }
        }
      }
    });
  }

  // ----------------------------------------
  // LISTA DE DESPESAS
  // ----------------------------------------

  function renderList() {
    if (!list || !count) return;

    list.innerHTML = "";

    count.textContent = filtered.length + " despesa(s)";

    if (!filtered.length) {
      list.innerHTML =
        '<li class="cat-result-empty">' +
        "Nenhuma despesa corresponde ao filtro." +
        "</li>";

      return;
    }

    filtered.slice().sort(function (a, b) {
      return a.date < b.date ? 1 : -1;
    }).forEach(function (expense) {
      var li = document.createElement("li");

      li.className = "cat-result-item";

      li.innerHTML =
        '<span class="cat-swatch" style="background:' +
        (colorOf[expense.category] || "#94a3b8") +
        '"></span>' +

        '<div class="cat-result-info">' +
          '<div class="cat-result-name"></div>' +
          '<div class="cat-result-meta"></div>' +
        "</div>" +

        '<span class="cat-result-value">' +
        brl(expense.amount) +
        "</span>";

      li.querySelector(".cat-result-name").textContent =
        expense.title;

      li.querySelector(".cat-result-meta").textContent =
        expense.category + " • " + brDate(expense.date);

      list.appendChild(li);
    });
  }

  // ----------------------------------------
  // EXPORTAÇÃO
  // ----------------------------------------

  function reportRows() {
    return filtered.map(function (expense) {
      return [
        expense.title,
        expense.category,
        brDate(expense.date),
        expense.amount
      ];
    });
  }

  function fileName(extension) {
    var start = startInput ? startInput.value : "";
    var end = endInput ? endInput.value : "";

    var label;

    if (start && end) {
      label = brDate(start) + "-a-" + brDate(end);
    } else {
      var monthLabel = $("monthLabel");

      label = monthLabel
        ? monthLabel.textContent
        : "relatorio";
    }

    label = label.trim().toLowerCase().replace(/\s+/g, "-");

    return "despesas-" + label + "." + extension;
  }

  function download(blob, name) {
    var url = URL.createObjectURL(blob);
    var link = document.createElement("a");

    link.href = url;
    link.download = name;

    document.body.appendChild(link);

    link.click();
    link.remove();

    setTimeout(function () {
      URL.revokeObjectURL(url);
    }, 30000);
  }

  // ----------------------------------------
  // EXPORTAR CSV
  // ----------------------------------------

  var exportCsv = $("exportCsv");

  if (exportCsv) {
    exportCsv.addEventListener("click", function () {
      var escapeCsv = function (value) {
        value = String(value);

        return /[";\n]/.test(value)
          ? '"' + value.replace(/"/g, '""') + '"'
          : value;
      };

      var lines = [
        ["Título", "Categoria", "Data", "Valor"]
      ].concat(
        reportRows().map(function (row) {
          return [
            row[0],
            row[1],
            row[2],
            row[3].toFixed(2).replace(".", ",")
          ];
        })
      );

      var csv = "\uFEFF" + lines.map(function (row) {
        return row.map(escapeCsv).join(";");
      }).join("\r\n");

      download(
        new Blob([csv], {
          type: "text/csv;charset=utf-8"
        }),
        fileName("csv")
      );
    });
  }

  // ----------------------------------------
  // EXPORTAR EXCEL
  // ----------------------------------------

  var exportXlsx = $("exportXlsx");

  if (exportXlsx) {
    exportXlsx.addEventListener("click", function () {
      if (typeof XLSX === "undefined") {
        alert("Biblioteca de Excel não carregada.");
        return;
      }

      var rows = [
        ["Título", "Categoria", "Data", "Valor (R$)"]
      ].concat(reportRows());

      var summary = [
        ["Categoria", "Total (R$)"]
      ].concat(
        groupByCategory(filtered).map(function (group) {
          return [group.category, group.total];
        })
      );

      var workbook = XLSX.utils.book_new();

      var worksheet1 = XLSX.utils.aoa_to_sheet(rows);

      worksheet1["!cols"] = [
        { wch: 28 },
        { wch: 16 },
        { wch: 12 },
        { wch: 12 }
      ];

      var worksheet2 = XLSX.utils.aoa_to_sheet(summary);

      worksheet2["!cols"] = [
        { wch: 18 },
        { wch: 14 }
      ];

      XLSX.utils.book_append_sheet(
        workbook,
        worksheet1,
        "Despesas"
      );

      XLSX.utils.book_append_sheet(
        workbook,
        worksheet2,
        "Por categoria"
      );

      XLSX.writeFile(workbook, fileName("xlsx"));
    });
  }

  // ----------------------------------------
  // INICIALIZAÇÃO
  // ----------------------------------------

  render();

})();
