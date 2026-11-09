import re
import json

with open('/workspaces/backup_final-thesis/data/processed/interactive_triangulation_heatmap.json') as f:
    heatmap_data = json.load(f)

json_str = json.dumps(heatmap_data, indent=2)

new_component = f"""
        <!-- ================================================================= -->
        <!-- INTERACTIVE TRIANGULATION HEATMAP (AFROBAROMETER R10 x MACRO)     -->
        <!-- ================================================================= -->
        <div class="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm mb-8" id="triangulation-heatmap-section">
          <div class="flex flex-wrap items-center justify-between gap-4 pb-5 border-b border-slate-200 mb-6">
            <div>
              <div class="flex items-center gap-2 mb-1.5">
                <span class="badge-pill bg-rose-100 text-rose-800 text-xs font-bold font-mono">Layer 1 × Layer 2 Triangulation</span>
                <span class="badge-pill bg-indigo-100 text-indigo-800 text-xs font-bold font-mono">Afrobarometer R10 (N=11,200)</span>
                <span class="badge-pill bg-slate-100 text-slate-700 text-xs font-bold font-mono">7 Focus Economies</span>
              </div>
              <h3 class="text-xl sm:text-2xl font-extrabold text-slate-900 font-serif">Multi-Country Discrepancy Heatmap: Macro vs. Ground Truth</h3>
              <p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-4xl">
                Contrasting nationally aggregated open indicators (World Bank WDI, UIS, ITU) against face-to-face citizen self-reports from <strong>Afrobarometer Round 10</strong>. Click any cell to inspect the empirical divergence and policy implications.
              </p>
            </div>
            <div class="flex items-center gap-2">
              <a href="#survey-portal-anchor" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-bold bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>
                Access Practitioner Survey Forms
              </a>
            </div>
          </div>

          <!-- Heatmap Interactive Table -->
          <div class="overflow-x-auto rounded-xl border border-slate-200 shadow-sm mb-6">
            <table class="w-full text-left text-xs border-collapse">
              <thead class="bg-slate-50 text-slate-700 font-serif font-bold uppercase tracking-wider text-[11px] border-b border-slate-200">
                <tr>
                  <th class="py-3 px-4">Country & Sample</th>
                  <th class="py-3 px-3 text-center">Pillar 2: HH Electricity<br><span class="text-[9px] font-sans font-normal text-slate-500">WB National vs AB Mains</span></th>
                  <th class="py-3 px-3 text-center">Pillar 2: Rural Grid<br><span class="text-[9px] font-sans font-normal text-slate-500">WB Rural vs AB Observed</span></th>
                  <th class="py-3 px-3 text-center">Pillar 2: Internet Access<br><span class="text-[9px] font-sans font-normal text-slate-500">WB Users vs AB Mobile</span></th>
                  <th class="py-3 px-3 text-center">Governance Paradox<br><span class="text-[9px] font-sans font-normal text-slate-500">Edu Satisfaction vs School Grid</span></th>
                  <th class="py-3 px-3 text-center">Pillar 3: Cash Precarity<br><span class="text-[9px] font-sans font-normal text-slate-500">AB Lived Income Shortage</span></th>
                  <th class="py-3 px-3 text-center bg-slate-100">Layer 3: Practitioner<br><span class="text-[9px] font-sans font-normal text-slate-500">AoA Field Diagnostic</span></th>
                </tr>
              </thead>
              <tbody id="interactive-heatmap-body" class="divide-y divide-slate-200">
                <!-- Injected via JavaScript -->
              </tbody>
            </table>
          </div>

          <!-- Active Drilldown Drawer / Card -->
          <div id="heatmap-drilldown-card" class="bg-slate-50 rounded-xl p-5 border border-slate-200 transition-all duration-300">
            <div class="flex items-center justify-between pb-3 border-b border-slate-200 mb-3">
              <div class="flex items-center gap-2">
                <span id="drilldown-badge" class="badge-pill bg-slate-200 text-slate-800 text-[10px] font-bold font-mono">SELECT A METRIC</span>
                <h4 id="drilldown-title" class="font-bold text-slate-900 text-sm font-serif">Click any cell above to inspect the empirical divergence</h4>
              </div>
              <span id="drilldown-country" class="text-xs font-bold text-indigo-700"></span>
            </div>
            <div id="drilldown-content" class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              <div class="bg-white p-3.5 rounded-lg border border-slate-200">
                <span class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Macro Aggregation (Layer 1)</span>
                <div id="drilldown-macro-val" class="text-base font-extrabold text-slate-800">—</div>
                <div id="drilldown-macro-src" class="text-[10px] text-slate-500 mt-0.5">Select a cell</div>
              </div>
              <div class="bg-white p-3.5 rounded-lg border border-slate-200">
                <span class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Citizen Self-Report (Layer 2)</span>
                <div id="drilldown-field-val" class="text-base font-extrabold text-slate-800">—</div>
                <div id="drilldown-field-src" class="text-[10px] text-slate-500 mt-0.5">Afrobarometer Round 10</div>
              </div>
              <div class="bg-white p-3.5 rounded-lg border border-slate-200">
                <span class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Empirical Divergence &amp; Policy Distortion</span>
                <div id="drilldown-gap-val" class="text-base font-extrabold text-indigo-700">—</div>
                <div id="drilldown-desc" class="text-[11px] text-slate-600 mt-1 leading-relaxed">Click any cell in the heatmap matrix above to drill down into the specific indicator gap and examine why procurement decisions fail.</div>
              </div>
            </div>
          </div>

          <!-- Static Matrix Fallback (Collapsible) -->
          <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Methodological note: Macro indicators sourced from World Bank WDI &amp; UIS. Citizen data from Afrobarometer R10 (38-country release, 2024-2026).</span>
            <details class="cursor-pointer text-indigo-600 font-semibold hover:underline">
              <summary class="list-none">View Legacy 4-Country Synthesis Matrix Image</summary>
              <div class="mt-3 p-3 bg-white border border-slate-200 rounded-lg">
                <img src="./data/analysis_b/master_discrepancy_matrix.png" alt="Legacy Matrix" class="w-full max-h-[350px] object-contain mx-auto">
              </div>
            </details>
          </div>
        </div>

        <script>
        const heatmapData = {json_str};

        function renderInteractiveHeatmap() {{
          const tbody = document.getElementById('interactive-heatmap-body');
          if (!tbody) return;
          tbody.innerHTML = '';

          heatmapData.forEach(c => {{
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-50/80 transition-colors border-b border-slate-100';

            // Country cell
            let html = `
              <td class="py-3 px-4">
                <div class="font-bold text-slate-900 flex items-center gap-1.5">
                  <span class="text-base">${{c.flag}}</span> ${{c.name}}
                </div>
                <div class="text-[10px] text-slate-400 font-mono">${{c.sample_size_ab ? 'N=' + c.sample_size_ab.toLocaleString() + ' (AB R10)' : c.note}}</div>
              </td>
            `;

            // Helper for cell badge
            function getCellHTML(dimKey, dim) {{
              if (!dim || dim.gap === null && dim.field_val === null) {{
                return `<td class="py-2.5 px-3 text-center text-slate-300 font-mono text-[11px]">—</td>`;
              }}
              if (dimKey === 'practitioner_audit') {{
                return `
                  <td class="py-2.5 px-3 text-center bg-slate-50">
                    <span onclick="selectHeatmapCell('${{c.iso3}}', '${{dimKey}}')" class="cursor-pointer inline-flex items-center gap-1 px-2 py-1 rounded bg-slate-200 text-slate-600 font-mono text-[10px] font-bold hover:bg-slate-300 transition">
                      <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                      Pending N
                    </span>
                  </td>
                `;
              }}
              if (dimKey === 'economic_precarity') {{
                const val = dim.field_val;
                const color = val > 80 ? 'bg-rose-100 text-rose-800 border-rose-200' : (val > 60 ? 'bg-amber-100 text-amber-800 border-amber-200' : 'bg-emerald-100 text-emerald-800 border-emerald-200');
                return `
                  <td class="py-2.5 px-3 text-center">
                    <button onclick="selectHeatmapCell('${{c.iso3}}', '${{dimKey}}')" class="px-2 py-1 rounded border font-mono font-bold text-[11px] ${{color}} hover:ring-2 hover:ring-indigo-400 transition">
                      ${{val}}%
                    </button>
                  </td>
                `;
              }}

              const gap = dim.gap;
              let bg = 'bg-slate-100 text-slate-700 border-slate-200';
              let sign = gap > 0 ? '+' : '';
              if (dimKey === 'electricity') {{
                if (gap < -15) bg = 'bg-rose-100 text-rose-900 border-rose-300 font-bold';
                else if (gap < -5) bg = 'bg-amber-100 text-amber-900 border-amber-300';
                else bg = 'bg-emerald-100 text-emerald-800 border-emerald-200';
              }} else if (dimKey === 'internet') {{
                if (Math.abs(gap) > 20) bg = 'bg-indigo-100 text-indigo-900 border-indigo-300 font-bold';
                else if (Math.abs(gap) > 10) bg = 'bg-amber-100 text-amber-800 border-amber-200';
                else bg = 'bg-emerald-100 text-emerald-800 border-emerald-200';
              }} else if (dimKey === 'gov_paradox') {{
                if (gap > 30) bg = 'bg-purple-100 text-purple-900 border-purple-300 font-bold';
                else if (gap > 15) bg = 'bg-blue-100 text-blue-900 border-blue-200';
                else bg = 'bg-slate-100 text-slate-700 border-slate-200';
              }} else if (dimKey === 'rural_grid') {{
                if (Math.abs(gap) > 20) bg = 'bg-orange-100 text-orange-900 border-orange-300';
                else bg = 'bg-slate-100 text-slate-700 border-slate-200';
              }}

              return `
                <td class="py-2.5 px-3 text-center">
                  <button onclick="selectHeatmapCell('${{c.iso3}}', '${{dimKey}}')" class="px-2 py-1 rounded border font-mono text-[11px] ${{bg}} hover:ring-2 hover:ring-indigo-400 transition" title="Click to view drilldown">
                    ${{sign}}${{gap}}pp
                  </button>
                </td>
              `;
            }}

            html += getCellHTML('electricity', c.dimensions.electricity);
            html += getCellHTML('rural_grid', c.dimensions.rural_grid);
            html += getCellHTML('internet', c.dimensions.internet);
            html += getCellHTML('gov_paradox', c.dimensions.gov_paradox);
            html += getCellHTML('economic_precarity', c.dimensions.economic_precarity);
            html += getCellHTML('practitioner_audit', c.dimensions.practitioner_audit);

            tr.innerHTML = html;
            tbody.appendChild(tr);
          }});
        }}

        function selectHeatmapCell(iso3, dimKey) {{
          const c = heatmapData.find(x => x.iso3 === iso3);
          if (!c) return;
          const dim = c.dimensions[dimKey];
          if (!dim) return;

          document.getElementById('drilldown-country').textContent = `${{c.flag}} ${{c.name}} (${{c.iso3}})`;
          document.getElementById('drilldown-badge').textContent = dim.name.toUpperCase();
          document.getElementById('drilldown-title').textContent = `${{c.name}}: ${{dim.name}} Divergence`;
          
          document.getElementById('drilldown-macro-val').textContent = dim.macro_val !== null ? `${{dim.macro_val}}${{dim.unit}}` : 'N/A';
          document.getElementById('drilldown-macro-src').textContent = dim.macro_src || '—';

          document.getElementById('drilldown-field-val').textContent = dim.field_val !== null ? `${{dim.field_val}}${{dim.unit}}` : 'Pending Field Data';
          document.getElementById('drilldown-field-src').textContent = dim.field_src || '—';

          const gapText = dim.gap !== null ? (dim.gap > 0 ? `+${{dim.gap}}pp Gap` : `${{dim.gap}}pp Gap`) : (dimKey === 'economic_precarity' ? `${{dim.field_val}}% Stress Rate` : 'Awaiting Collection');
          document.getElementById('drilldown-gap-val').textContent = gapText;
          document.getElementById('drilldown-desc').textContent = dim.desc || '';

          // Highlight drilldown card smoothly
          const card = document.getElementById('heatmap-drilldown-card');
          card.classList.add('ring-2', 'ring-indigo-500');
          setTimeout(() => card.classList.remove('ring-2', 'ring-indigo-500'), 800);
        }}

        document.addEventListener('DOMContentLoaded', () => {{
          renderInteractiveHeatmap();
        }});
        if (document.readyState === 'complete' || document.readyState === 'interactive') {{
          renderInteractiveHeatmap();
        }}
        </script>
"""

with open('/workspaces/backup_final-thesis/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm mb-8">
          <h3 class="font-bold text-slate-900 text-lg mb-3 font-serif">Master Discrepancy Matrix Visualization</h3>
          <p class="text-xs text-slate-600 mb-4">
            Triangulating the 4 pilot archetypes across the 3 core structural gaps: Connectivity, Sustainability, and Linguistic Inclusion.
          </p>
          <img src="./data/analysis_b/master_discrepancy_matrix.png" alt="Master Discrepancy Matrix" class="w-full max-h-[460px] object-contain mx-auto rounded-lg shadow-sm border border-slate-100">
        </div>'''

if target in content:
    content = content.replace(target, new_component)
    with open('/workspaces/backup_final-thesis/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully replaced static image with interactive heatmap in index.html!")
else:
    print("Target block not found. Checking regex...")
