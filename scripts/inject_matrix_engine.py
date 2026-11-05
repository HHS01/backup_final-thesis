with open('/workspaces/CC_3/data/processed/supply_demand_matrix_data.js', 'r', encoding='utf-8') as f:
    js_data = f.read()

with open('/workspaces/CC_3/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

init_target = "// Initialize on DOM load\n    document.addEventListener('DOMContentLoaded', () => {"

matrix_code_template = """
    // =================================================================
    // SUPPLY-DEMAND MISMATCH MATRIX ENGINE (48 SSA Demand vs 148 Supply)
    // =================================================================
""" + js_data + """

    let matrixPlayerScope = 'core'; // 'core' | 'all_ssa' | 'mena_tier'
    let matrixDomainFilter = 'ALL';

    function setMatrixPlayerScope(scope) {
      matrixPlayerScope = scope;
      const btnCore = document.getElementById('btn-scope-core');
      const btnSSA = document.getElementById('btn-scope-ssa');
      const btnMENA = document.getElementById('btn-scope-mena');

      [btnCore, btnSSA, btnMENA].forEach(btn => {
        if (!btn) return;
        btn.className = 'px-3 py-1.5 rounded-lg font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition text-xs';
      });

      if (scope === 'core' && btnCore) {
        btnCore.className = 'px-3 py-1.5 rounded-lg font-bold bg-slate-900 text-white shadow-sm transition text-xs';
      } else if (scope === 'all_ssa' && btnSSA) {
        btnSSA.className = 'px-3 py-1.5 rounded-lg font-bold bg-indigo-900 text-white shadow-sm transition text-xs';
      } else if (scope === 'mena_tier' && btnMENA) {
        btnMENA.className = 'px-3 py-1.5 rounded-lg font-bold bg-slate-700 text-white shadow-sm transition text-xs';
      }

      renderSupplyMatrix();
    }

    function filterMatrixDomain(domain) {
      matrixDomainFilter = domain;
      document.querySelectorAll('.matrix-domain-btn').forEach(btn => {
        if (btn.getAttribute('data-domain') === domain) {
          btn.className = 'matrix-domain-btn px-2.5 py-1 rounded-md text-xs font-bold bg-indigo-700 text-white';
        } else {
          btn.className = 'matrix-domain-btn px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200';
        }
      });
      renderSupplyMatrix();
    }

    function renderSupplyMatrix() {
      const tbody = document.getElementById('matrix-table-tbody');
      const summaryEl = document.getElementById('matrix-counts-summary');
      if (!tbody) return;

      const searchTerm = (document.getElementById('matrix-search')?.value || '').toLowerCase().trim();

      // 1. Filter players based on scope and domain
      let activePlayers = MATRIX_PLAYERS.filter(p => !p.qa_flag); // Exclude duplicates & university non-startups

      if (matrixPlayerScope === 'core') {
        activePlayers = activePlayers.filter(p => p.is_core_25);
      } else if (matrixPlayerScope === 'all_ssa') {
        activePlayers = activePlayers.filter(p => !p.is_mena);
      } else if (matrixPlayerScope === 'mena_tier') {
        activePlayers = activePlayers.filter(p => p.is_mena);
      }

      if (matrixDomainFilter !== 'ALL') {
        activePlayers = activePlayers.filter(p => p.domain === matrixDomainFilter);
      }

      // Group active players by country name (case-insensitive)
      const playersByCountry = {};
      activePlayers.forEach(p => {
        const cNorm = p.country.toLowerCase().trim();
        if (!playersByCountry[cNorm]) playersByCountry[cNorm] = [];
        playersByCountry[cNorm].push(p);
      });

      // 2. Filter countries
      let activeCountries = MATRIX_COUNTRIES;
      if (matrixPlayerScope === 'mena_tier') {
        activeCountries = activeCountries.filter(c => c.region === 'MENA');
      } else {
        activeCountries = activeCountries.filter(c => c.region === 'SSA');
      }

      if (searchTerm) {
        activeCountries = activeCountries.filter(c => {
          const matchCountry = c.country.toLowerCase().includes(searchTerm) || c.iso3.toLowerCase().includes(searchTerm);
          const cPlayers = playersByCountry[c.country.toLowerCase()] || [];
          const matchPlayer = cPlayers.some(p => p.name.toLowerCase().includes(searchTerm) || p.category.toLowerCase().includes(searchTerm));
          return matchCountry || matchPlayer;
        });
      }

      if (summaryEl) {
        summaryEl.textContent = 'Showing ' + activeCountries.length + ' ' + (matrixPlayerScope === 'mena_tier' ? 'MENA Reference' : 'Sub-Saharan Africa') + ' nations matched against ' + activePlayers.length + ' active EdTech solutions (' + matrixPlayerScope.toUpperCase() + ' scope).';
      }

      if (!activeCountries.length) {
        tbody.innerHTML = '<tr><td colspan="5" class="p-8 text-center text-slate-400 italic">No countries or players match the selected filter.</td></tr>';
        return;
      }

      tbody.innerHTML = activeCountries.map(c => {
        const cPlayers = playersByCountry[c.country.toLowerCase()] || [];
        const hasPlayers = cPlayers.length > 0;

        // Demand Badges
        const lpText = c.learning_poverty !== null ? (c.learning_poverty + '%') : '<span class="text-slate-400">Unreported</span>';
        const lpBadge = c.is_lp_proxy
          ? '<span class="badge-pill bg-amber-100 text-amber-800 text-[10px] font-mono font-bold" title="Official Learning Poverty unmeasured; UNESCO Adult Illiteracy deficit used as anchor.">⚠️ PROXY: ' + c.learning_poverty + '%</span>'
          : '<span class="font-bold text-slate-800 font-mono">' + lpText + '</span>';

        const elecText = c.rural_electrification !== null ? (c.rural_electrification + '%') : '—';
        const elecClass = c.rural_electrification !== null && c.rural_electrification < 30 ? 'text-rose-700 font-bold' : 'text-slate-700';

        const bbText = c.fixed_broadband_per100 !== null ? (c.fixed_broadband_per100 + ' /100') : '—';
        const bbClass = c.fixed_broadband_per100 !== null && c.fixed_broadband_per100 < 1.0 ? 'text-amber-700 font-semibold' : 'text-slate-700';

        // Render mapped solutions cell
        let solutionsHtml = '';
        if (hasPlayers) {
          solutionsHtml = '<div class="flex flex-wrap gap-1.5">' +
            cPlayers.map(p => {
              const borderClass = p.is_core_25 ? 'bg-indigo-50 border-indigo-200 text-indigo-900 font-bold' : (p.is_mena ? 'bg-slate-100 border-slate-200 text-slate-700' : 'bg-slate-50 border-slate-200 text-slate-800');
              const pillClass = p.is_core_25 ? 'bg-indigo-200 text-indigo-800' : 'bg-slate-200 text-slate-600';
              return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md border text-[11px] ' + borderClass + '">' +
                '<span>' + p.name + '</span>' +
                '<span class="text-[9px] uppercase px-1 rounded ' + pillClass + ' font-mono">' + p.category + '</span>' +
              '</span>';
            }).join('') +
          '</div>';
        } else {
          solutionsHtml = '<div class="text-[11px] text-slate-400 italic flex items-center justify-between">' +
            '<span>Zero domestic players catalogued in landscape.</span>' +
            '<span class="badge-pill bg-rose-50 text-rose-700 text-[10px]">Supply Desert</span>' +
          '</div>';
        }

        const litRow = c.adult_literacy ? '<span class="block text-[10px] text-slate-400">Adult Lit: ' + c.adult_literacy + '%</span>' : '';

        return '<tr class="hover:bg-slate-50/80 transition">' +
          '<td class="p-3 sticky left-0 z-10 bg-inherit border-r border-slate-200 font-bold text-slate-900 whitespace-nowrap">' +
            '<span>' + c.country + '</span>' +
            '<span class="block text-[10px] font-mono text-slate-400 font-normal">' + c.iso3 + ' · ' + c.region + '</span>' +
          '</td>' +
          '<td class="p-3 whitespace-nowrap">' +
            lpBadge + litRow +
          '</td>' +
          '<td class="p-3 whitespace-nowrap ' + elecClass + '">' +
            '<span>' + elecText + '</span>' +
            '<span class="block text-[10px] text-slate-400 font-normal">Rural Grid</span>' +
          '</td>' +
          '<td class="p-3 whitespace-nowrap ' + bbClass + '">' +
            '<span>' + bbText + '</span>' +
            '<span class="block text-[10px] text-slate-400 font-normal">School/Fixed BB</span>' +
          '</td>' +
          '<td class="p-3">' +
            solutionsHtml +
          '</td>' +
        '</tr>';
      }).join('');
    }

    // Initialize on DOM load
    document.addEventListener('DOMContentLoaded', () => {
"""

if init_target not in html:
    print("Error: init_target not found!")
    exit(1)

html = html.replace(init_target, matrix_code_template)

dom_load_target = "fetchGigaData();\n      selectCountry('KEN');"
dom_load_replacement = "fetchGigaData();\n      renderSupplyMatrix();\n      selectCountry('KEN');"

if dom_load_target in html:
    html = html.replace(dom_load_target, dom_load_replacement)

with open('/workspaces/CC_3/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully injected Supply-Demand Matrix Engine into index.html!")
