(function () {
  "use strict";

  // Dados vindos do Django via {{ expenses_json|json_script:"expensesData" }}.
  // Se não houver, usa dados de exemplo para visualizar o layout.
  var SAMPLE = [
    { title: "Mercado Extra", category: "Alimentação", date: "2026-11-02", amount: 412.9 },
    { title: "iFood", category: "Alimentação", date: "2026-11-05", amount: 86.5 },
    { title: "Tênis Nike", category: "Compras", date: "2026-11-04", amount: 299.9 },
    { title: "Uber", category: "Transporte", date: "2026-11-06", amount: 54.3 },
    { title: "Gasolina", category: "Transporte", date: "2026-11-10", amount: 220 },
    { title: "Conta de luz", category: "Moradia", date: "2026-11-08", amount: 185.4 },
    { title: "Aluguel", category: "Moradia", date: "2026-11-01", amount: 1500 },
    { title: "Cinema", category: "Lazer", date: "2026-11-09", amount: 72 },
    { title: "Farmácia", category: "Saúde", date: "2026-11-07", amount: 64.8 },
    { title: "Curso online", category: "Educação", date: "2026-11-03", amount: 129.9 }
  ];

  var COLORS = ["#38bdf8", "#a855f7", "#2dd4bf", "#facc15", "#f43f5e", "#4ade80", "#fb923c", "#818cf8", "#e879f9", "#94a3b8"];

  var dataEl = document.getElementById("expensesData");
  var all = SAMPLE;
  try {
    var parsed = dataEl ? JSON.parse(dataEl.textContent) : null;
    if (Array.isArray(parsed)) all = parsed;
  } catch (e) {}
  all = all.map(function (e) { return { title: e.title, category: e.category, date: e.date, amount: Number(e.amount) || 0 }; });

  var brl = function (n) { return n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" }); };
  var brDate = function (iso) { var p = String(iso).split("-"); return p.length === 3 ? p[2] + "/" + p[1] + "/" + p[0] : iso; };

  var categories = Array.from(new Set(all.map(function (e) { return e.category; }))).sort();
  var colorOf = {};
  categories.forEach(function (c, i) { colorOf[c] = COLORS[i % COLORS.length]; });

  var hidden = new Set();
  var filtered = all.slice();
  var chart = null;

  var $ = function (id) { return document.getElementById(id); };
  var legend = $("categoryLegend"), totalEl = $("categoryTotal"), list = $("resultList"), count = $("resultCount");
  var selCat = $("filterCategory");

  categories.forEach(function (c) {
    var o = document.createElement("option");
    o.value = c; o.textContent = c; selCat.appendChild(o);
  });

  function groupByCategory(rows) {
    var map = {};
    rows.forEach(function (e) { map[e.category] = (map[e.category] || 0) + e.amount; });
    return Object.keys(map).map(function (k) { return { category: k, total: map[k] }; })
      .sort(function (a, b) { return b.total - a.total; });
  }

  function render() {
    var groups = groupByCategory(filtered);
    var visible = groups.filter(function (g) { return !hidden.has(g.category); });
    var visibleTotal = visible.reduce(function (s, g) { return s + g.total; }, 0);
    var fullTotal = groups.reduce(function (s, g) { return s + g.total; }, 0);

    legend.innerHTML = "";
    groups.forEach(function (g) {
      var off = hidden.has(g.category);
      var pct = !off && visibleTotal ? " (" + (g.total / visibleTotal * 100).toFixed(1).replace(".", ",") + "%)" : "";
      var li = document.createElement("li");
      li.innerHTML =
        '<button type="button" class="cat-legend-item' + (off ? " is-off" : "") + '" aria-pressed="' + !off + '">' +
        '<span class="cat-swatch" style="background:' + colorOf[g.category] + '"></span>' +
        '<span class="cat-legend-name"></span>' +
        '<span class="cat-legend-value">' + (off ? "" : brl(g.total)) + "</span></button>";
      li.querySelector(".cat-legend-name").textContent = g.category + pct;
      li.firstChild.addEventListener("click", function () {
        off ? hidden.delete(g.category) : hidden.add(g.category);
        render();
      });
      legend.appendChild(li);
    });

    totalEl.textContent = hidden.size ? brl(visibleTotal) + " (" + brl(fullTotal) + " com todas)" : brl(visibleTotal);
    $("chartEmpty").hidden = visible.length > 0;
    drawChart(visible);
    renderList();
  }

  function drawChart(groups) {
    if (typeof Chart === "undefined") return;
    var cfg = {
      labels: groups.map(function (g) { return g.category; }),
      datasets: [{
        data: groups.map(function (g) { return g.total; }),
        backgroundColor: groups.map(function (g) { return colorOf[g.category]; }),
        borderColor: "rgba(15, 23, 42, .9)", borderWidth: 3, hoverOffset: 8
      }]
    };
    if (chart) { chart.data = cfg; chart.update(); return; }
    chart = new Chart($("categoryChart"), {
      type: "doughnut",
      data: cfg,
      options: {
        cutout: "55%", maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { callbacks: { label: function (c) { return " " + c.label + ": " + brl(c.parsed); } } }
        }
      }
    });
  }

  function renderList() {
    list.innerHTML = "";
    count.textContent = filtered.length + " despesa(s)";
    if (!filtered.length) {
      list.innerHTML = '<li class="cat-result-empty">Nenhuma despesa corresponde ao filtro.</li>';
      return;
    }
    filtered.slice().sort(function (a, b) { return a.date < b.date ? 1 : -1; }).forEach(function (e) {
      var li = document.createElement("li");
      li.className = "cat-result-item";
      li.innerHTML =
        '<span class="cat-swatch" style="background:' + colorOf[e.category] + '"></span>' +
        '<div class="cat-result-info"><div class="cat-result-name"></div><div class="cat-result-meta"></div></div>' +
        '<span class="cat-result-value">' + brl(e.amount) + "</span>";
      li.querySelector(".cat-result-name").textContent = e.title;
      li.querySelector(".cat-result-meta").textContent = e.category + " • " + brDate(e.date);
      list.appendChild(li);
    });
  }

  function applyFilter() {
    var q = $("filterName").value.trim().toLowerCase();
    var cat = selCat.value, start = $("filterStart").value, end = $("filterEnd").value;
    filtered = all.filter(function (e) {
      return (!q || e.title.toLowerCase().indexOf(q) !== -1) &&
        (!cat || e.category === cat) &&
        (!start || e.date >= start) &&
        (!end || e.date <= end);
    });
    hidden.clear();
    render();
  }

  $("filterForm").addEventListener("submit", function (ev) { ev.preventDefault(); applyFilter(); });
  $("filterClear").addEventListener("click", function () { $("filterForm").reset(); applyFilter(); });

  // ---------- Exportação ----------
  function reportRows() {
    return filtered.map(function (e) { return [e.title, e.category, brDate(e.date), e.amount]; });
  }
  function fileName(ext) {
    var label = ($("monthLabel").textContent || "relatorio").trim().toLowerCase().replace(/\s+/g, "-");
    return "despesas-" + label + "." + ext;
  }
  function download(blob, name) {
    var url = URL.createObjectURL(blob), a = document.createElement("a");
    a.href = url; a.download = name; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 30000);
  }

  $("exportCsv").addEventListener("click", function () {
    var esc = function (v) { v = String(v); return /[";\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    var lines = [["Título", "Categoria", "Data", "Valor"]].concat(reportRows().map(function (r) {
      return [r[0], r[1], r[2], r[3].toFixed(2).replace(".", ",")];
    }));
    var csv = "\uFEFF" + lines.map(function (r) { return r.map(esc).join(";"); }).join("\r\n");
    download(new Blob([csv], { type: "text/csv;charset=utf-8" }), fileName("csv"));
  });

  $("exportXlsx").addEventListener("click", function () {
    if (typeof XLSX === "undefined") { alert("Biblioteca de Excel não carregada."); return; }
    var rows = [["Título", "Categoria", "Data", "Valor (R$)"]].concat(reportRows());
    var summary = [["Categoria", "Total (R$)"]].concat(groupByCategory(filtered).map(function (g) { return [g.category, g.total]; }));
    var wb = XLSX.utils.book_new();
    var ws1 = XLSX.utils.aoa_to_sheet(rows); ws1["!cols"] = [{ wch: 28 }, { wch: 16 }, { wch: 12 }, { wch: 12 }];
    var ws2 = XLSX.utils.aoa_to_sheet(summary); ws2["!cols"] = [{ wch: 18 }, { wch: 14 }];
    XLSX.utils.book_append_sheet(wb, ws1, "Despesas");
    XLSX.utils.book_append_sheet(wb, ws2, "Por categoria");
    XLSX.writeFile(wb, fileName("xlsx"));
  });

  render();
})();