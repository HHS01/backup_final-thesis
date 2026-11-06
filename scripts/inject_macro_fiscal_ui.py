#!/usr/bin/env python3
"""
inject_macro_fiscal_ui.py
=========================
Embeds the Macro-Fiscal & External Aid dataset and interactive visualization
into index.html:
  1. Injects MACRO_FISCAL_DATA JavaScript constant.
  2. Enhances Lens 4 (National Policy & Capital Allocation) with dual-gatekeeping
     metrics (domestic budget % vs external aid), the 40:1 ICT recurrent gap,
     and the interactive 2017-2024 disbursement sparkline bar strip.
  3. Updates renderDeepDive() to dynamically drive Lens 4 across all 7 countries.
  4. Adds a Macro-Fiscal & External Aid Observatory Matrix card to Tab 1.
"""

import json
from pathlib import Path

def main():
    root = Path('/workspaces/CC_3')
    html_path = root / 'index.html'
    data_path = root / 'data/processed/macro_fiscal_data.js'

    html = html_path.read_text(encoding='utf-8')
    js_data = data_path.read_text(encoding='utf-8')

    # Remove node.js export wrapper for inlining
    js_inline = js_data.split('if (typeof module')[0].strip()

    # --------------------------------------------------------------------------
    # 1. Update Lens 4 Markup in HTML
    # --------------------------------------------------------------------------
    old_lens4_start = '<!-- Lens 4: National Policy & Capital Allocation -->'
    old_lens4_target = '''              <!-- Lens 4: National Policy & Capital Allocation -->
              <div class="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between mb-3">
                    <span class="inline-flex items-center gap-1.5 text-xs font-bold text-amber-700 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-200">
                      🏛️ Lens 4: National Policy &amp; Capital
                    </span>
                    <span id="lens4-source" class="text-[11px] text-slate-400 font-mono">World Bank · UIS · Ookla Q1 2024</span>
                  </div>
                  <h4 id="lens4-heading" class="font-extrabold text-slate-900 text-base mb-2 font-serif">The CapEx Trap &amp; Recurrent Budget Lock</h4>
                  <p id="lens4-desc" class="text-xs text-slate-600 leading-relaxed mb-4">
                    Ministries borrow heavily for initial hardware imports ($150M+ DLP tablets) while 92.5% of education budget is locked in recurrent salaries, leaving 0% for maintenance.
                  </p>
                  <!-- Ookla speed-test panel -->
                  <div class="bg-slate-50 rounded-lg border border-slate-100 px-3 py-2 mb-3">
                    <div class="text-[10px] uppercase font-bold text-slate-400 mb-1.5 tracking-wider">Network Speed Reality (Ookla Speedtest · Q1 2024)</div>
                    <div class="grid grid-cols-3 gap-2 text-center text-[11px]">
                      <div>
                        <span id="quad-speed-mobile" class="block font-extrabold text-blue-700 text-base">46.2</span>
                        <span class="text-slate-500">Mbps ↓ mobile<br><span class="font-mono text-[10px]">test-weighted</span></span>
                      </div>
                      <div class="border-x border-slate-200/60">
                        <span id="quad-speed-median" class="block font-extrabold text-amber-700 text-base">23.4</span>
                        <span class="text-slate-500">Mbps ↓ median<br><span class="font-mono text-[10px]">tile (rural proxy)</span></span>
                      </div>
                      <div>
                        <span id="quad-speed-latency" class="block font-extrabold text-rose-700 text-base">47.7ms</span>
                        <span class="text-slate-500">Latency<br><span class="font-mono text-[10px]">test-weighted</span></span>
                      </div>
                    </div>
                    <p id="quad-speed-note" class="text-[10px] text-slate-400 mt-1.5 italic">⚠ Ookla tiles skew urban (Speedtest app users). Median tile (23 Mbps) better proxies non-urban reachability. Fixed broadband median: 10.6 Mbps across 6,453 tiles.</p>
                  </div>
                  
                  <div class="grid grid-cols-3 gap-2 py-3 bg-slate-50 rounded-lg border border-slate-100 text-center mb-4">
                    <div class="p-2">
                      <span class="text-[10px] text-slate-500 block uppercase">Learning Poverty</span>
                      <span id="quad-pol-pov" class="text-base font-extrabold text-rose-700">79.3%</span>
                      <span class="text-[9px] text-slate-400 block mt-0.5">World Bank 2023</span>
                    </div>
                    <div class="p-2 border-x border-slate-200/60">
                      <span class="text-[10px] text-slate-500 block uppercase">School Power</span>
                      <span id="quad-pol-elec" class="text-base font-extrabold text-blue-700">82.6%</span>
                      <span class="text-[9px] text-slate-400 block mt-0.5">Primary Schools</span>
                    </div>
                    <div class="p-2">
                      <span class="text-[10px] text-slate-500 block uppercase">Recurrent Lock</span>
                      <span id="quad-pol-opex" class="text-base font-extrabold text-amber-700">92.5%</span>
                      <span class="text-[9px] text-slate-400 block mt-0.5">OpEx vs CapEx</span>
                    </div>
                  </div>
                </div>

                <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span>Out-of-School Primary Rate:</span>
                  <span id="quad-pol-outreach" class="font-bold text-rose-700">18.8% (World Bank 2023)</span>
                </div>
              </div>'''

    new_lens4_markup = '''              <!-- Lens 4: National Policy & Capital Allocation -->
              <div class="bg-white rounded-xl p-5 border border-slate-200 shadow-sm flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between mb-3">
                    <span class="inline-flex items-center gap-1.5 text-xs font-bold text-amber-700 bg-amber-50 px-2.5 py-1 rounded-full border border-amber-200">
                      🏛️ Lens 4: Macro Policy &amp; External Aid
                    </span>
                    <span id="lens4-source" class="text-[11px] text-slate-400 font-mono">IMF GFS COFOG · IATI Datastore · World Bank</span>
                  </div>
                  
                  <div class="flex items-start justify-between gap-2 mb-2">
                    <h4 id="lens4-heading" class="font-extrabold text-slate-900 text-base font-serif">The CapEx Trap &amp; The Recurrent Cliff</h4>
                    <span id="lens4-cliff-badge" class="badge-pill bg-rose-100 text-rose-800 border border-rose-200 font-bold text-[10px] whitespace-nowrap">High Tension (40:1 Gap)</span>
                  </div>
                  
                  <p id="lens4-desc" class="text-xs text-slate-600 leading-relaxed mb-4">
                    Kenya allocates 18.43% of national budget to education (strong domestic commitment), yet central ICT receives only 0.46%. With over $1B in external education aid driving hardware deployments, schools lack ongoing public connectivity and maintenance subsidies.
                  </p>

                  <!-- DUAL-GATEKEEPING MACRO-FISCAL & AID CARDS (2x2 GRID) -->
                  <div class="grid grid-cols-2 gap-2 mb-3 text-left">
                    <div class="p-2.5 bg-blue-50/60 rounded-lg border border-blue-100">
                      <span class="text-[10px] text-blue-700 block uppercase font-bold tracking-wider">Domestic Education Share</span>
                      <div class="flex items-baseline gap-1 mt-0.5">
                        <span id="lens4-edu-budget" class="text-lg font-black text-blue-900">18.4%</span>
                        <span class="text-[10px] text-blue-600 font-medium">of Gov Budget</span>
                      </div>
                      <span class="text-[9px] text-slate-400 block mt-0.5 font-mono">IMF GFS COFOG (2023)</span>
                    </div>

                    <div class="p-2.5 bg-amber-50/60 rounded-lg border border-amber-100">
                      <div class="flex items-center justify-between">
                        <span class="text-[10px] text-amber-700 block uppercase font-bold tracking-wider">Central ICT Budget</span>
                        <span id="lens4-gap-ratio" class="text-[9px] font-bold text-rose-700 bg-rose-100/80 px-1 py-0.2 rounded font-mono">40:1 Gap</span>
                      </div>
                      <div class="flex items-baseline gap-1 mt-0.5">
                        <span id="lens4-comm-budget" class="text-lg font-black text-amber-900">0.46%</span>
                        <span class="text-[10px] text-amber-600 font-medium">of Gov Budget</span>
                      </div>
                      <span class="text-[9px] text-slate-400 block mt-0.5 font-mono">Communication Envelope</span>
                    </div>

                    <div class="p-2.5 bg-purple-50/60 rounded-lg border border-purple-100">
                      <span class="text-[10px] text-purple-700 block uppercase font-bold tracking-wider">External Education Aid</span>
                      <div class="flex items-baseline gap-1 mt-0.5">
                        <span id="lens4-aid-8yr" class="text-lg font-black text-purple-900">$1,016.6M</span>
                        <span class="text-[10px] text-purple-600 font-medium">8-Yr Disbursed</span>
                      </div>
                      <span class="text-[9px] text-slate-400 block mt-0.5 font-mono">IATI Normalized 2017–24</span>
                    </div>

                    <div class="p-2.5 bg-emerald-50/60 rounded-lg border border-emerald-100">
                      <span class="text-[10px] text-emerald-700 block uppercase font-bold tracking-wider">2020 COVID Aid Surge</span>
                      <div class="flex items-baseline gap-1 mt-0.5">
                        <span id="lens4-covid-surge" class="text-lg font-black text-emerald-900">+$139.3M</span>
                        <span class="text-[10px] text-emerald-700 font-bold">(+137%)</span>
                      </div>
                      <span class="text-[9px] text-slate-400 block mt-0.5 font-mono">Emergency Remote Spike</span>
                    </div>
                  </div>

                  <!-- INTERACTIVE 8-YEAR DISBURSEMENT TRAJECTORY (2017-2024) -->
                  <div class="bg-slate-50 rounded-lg border border-slate-200/80 px-3 py-2.5 mb-3">
                    <div class="flex items-center justify-between mb-1.5">
                      <span class="text-[10px] uppercase font-bold text-slate-600 tracking-wider">Annual Education Aid Disbursed ($M USD · 2017–2024)</span>
                      <span class="text-[9px] font-mono text-slate-400">Peak: 2020 COVID</span>
                    </div>
                    <div id="lens4-timeseries-bars" class="flex items-end gap-1.5 h-14 pt-1">
                      <!-- Rendered dynamically by renderLens4MacroFiscal() -->
                    </div>
                  </div>

                  <!-- Ookla speed-test panel -->
                  <div class="bg-slate-50 rounded-lg border border-slate-100 px-3 py-2 mb-3">
                    <div class="text-[10px] uppercase font-bold text-slate-400 mb-1.5 tracking-wider">Network Speed Reality (Ookla Speedtest · Q1 2024)</div>
                    <div class="grid grid-cols-3 gap-2 text-center text-[11px]">
                      <div>
                        <span id="quad-speed-mobile" class="block font-extrabold text-blue-700 text-base">46.2</span>
                        <span class="text-slate-500">Mbps ↓ mobile<br><span class="font-mono text-[10px]">test-weighted</span></span>
                      </div>
                      <div class="border-x border-slate-200/60">
                        <span id="quad-speed-median" class="block font-extrabold text-amber-700 text-base">23.4</span>
                        <span class="text-slate-500">Mbps ↓ median<br><span class="font-mono text-[10px]">tile (rural proxy)</span></span>
                      </div>
                      <div>
                        <span id="quad-speed-latency" class="block font-extrabold text-rose-700 text-base">47.7ms</span>
                        <span class="text-slate-500">Latency<br><span class="font-mono text-[10px]">test-weighted</span></span>
                      </div>
                    </div>
                    <p id="quad-speed-note" class="text-[10px] text-slate-400 mt-1.5 italic">⚠ Ookla tiles skew urban (Speedtest app users). Median tile (23 Mbps) better proxies non-urban reachability. Fixed broadband median: 10.6 Mbps across 6,453 tiles.</p>
                  </div>
                  
                  <div class="grid grid-cols-3 gap-2 py-2.5 bg-slate-50 rounded-lg border border-slate-100 text-center mb-3">
                    <div class="p-1.5">
                      <span class="text-[10px] text-slate-500 block uppercase">Learning Poverty</span>
                      <span id="quad-pol-pov" class="text-base font-extrabold text-rose-700">79.3%</span>
                      <span class="text-[9px] text-slate-400 block mt-0.5">World Bank 2023</span>
                    </div>
                    <div class="p-2 border-x border-slate-200/60">
                      <span class="text-[10px] text-slate-500 block uppercase">School Power</span>
                      <span id="quad-pol-elec" class="text-base font-extrabold text-blue-700">82.6%</span>
                      <span class="text-[9px] text-slate-400 block mt-0.5">Primary Schools</span>
                    </div>
                    <div class="p-2">
                      <span class="text-[10px] text-slate-500 block uppercase">Recurrent Lock</span>
                      <span id="quad-pol-opex" class="text-base font-extrabold text-amber-700">92.5%</span>
                      <span class="text-[9px] text-slate-400 block mt-0.5">OpEx vs CapEx</span>
                    </div>
                  </div>
                </div>

                <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                  <span>Out-of-School Primary Rate:</span>
                  <span id="quad-pol-outreach" class="font-bold text-rose-700">18.8% (World Bank 2023)</span>
                </div>
              </div>'''

    if old_lens4_target not in html:
        print("Error: old_lens4_target not found in index.html!")
        return 1

    html = html.replace(old_lens4_target, new_lens4_markup)

    # --------------------------------------------------------------------------
    # 2. Add Macro-Fiscal & External Aid Observatory Matrix Section in Tab 1
    # --------------------------------------------------------------------------
    matrix_section_target = '<!-- INTERACTIVE DECISION SIMULATOR: GEEAP & EDTECH HUB LIFECYCLE MODEL -->'
    macro_table_markup = '''<!-- ================================================================= -->
            <!-- MACRO-FISCAL & EXTERNAL AID OBSERVATORY MATRIX (2017-2024)       -->
            <!-- ================================================================= -->
            <div class="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm mb-10" id="macro-fiscal-observatory-section">
              <div class="flex flex-wrap items-center justify-between gap-4 pb-5 border-b border-slate-200 mb-6">
                <div>
                  <div class="flex items-center gap-2 mb-1.5">
                    <span class="badge-pill bg-blue-100 text-blue-800 text-xs font-bold">IMF GFS COFOG · IATI Datastore</span>
                    <span class="badge-pill bg-purple-100 text-purple-800 text-xs font-bold">2017–2024 Harmonized Window</span>
                  </div>
                  <h3 class="text-xl sm:text-2xl font-extrabold text-slate-900 font-serif">
                    Macro-Fiscal &amp; External Aid Observatory
                  </h3>
                  <p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-4xl">
                    Triangulating domestic government budget commitments against bilateral/multilateral development assistance to expose the <strong>Digital Recurrent Cliff</strong> — where large donor hardware imports collide with thin domestic recurring operational envelopes.
                  </p>
                </div>
                <div class="text-xs bg-slate-50 p-2.5 rounded-xl border border-slate-200 text-slate-600">
                  <div><strong>7-Country Education Aid:</strong> <span class="font-bold text-blue-700">$6,843.6M</span></div>
                  <div><strong>7-Country ICT/Comm Aid:</strong> <span class="font-bold text-purple-700">$552.1M</span></div>
                </div>
              </div>

              <!-- Comparative Table Container -->
              <div class="overflow-x-auto border border-slate-200 rounded-xl">
                <table class="w-full text-left text-xs border-collapse divide-y divide-slate-200" id="macro-fiscal-table">
                  <thead class="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
                    <tr>
                      <th class="p-3 bg-slate-50 min-w-[150px]">Economy &amp; Focus</th>
                      <th class="p-3 min-w-[130px]">Domestic Edu % Budget</th>
                      <th class="p-3 min-w-[130px]">Central ICT % Budget</th>
                      <th class="p-3 min-w-[120px]">Domestic Gap Ratio</th>
                      <th class="p-3 min-w-[140px]">8-Yr Edu Aid (IATI)</th>
                      <th class="p-3 min-w-[140px]">2020 COVID Surge</th>
                      <th class="p-3 min-w-[200px]">Recurrent Cliff Risk &amp; Dynamic Diagnosis</th>
                    </tr>
                  </thead>
                  <tbody id="macro-fiscal-table-tbody" class="divide-y divide-slate-100 bg-white">
                    <!-- Populated dynamically by renderMacroFiscalTable() -->
                  </tbody>
                </table>
              </div>

              <div class="mt-4 pt-3 border-t border-slate-200 flex flex-wrap items-center justify-between text-xs text-slate-500">
                <div>Source: IMF Government Finance Statistics (GFS) COFOG 2017-2024, IATI Datastore Solr API (29,388 transactions), World Bank EdStats.</div>
                <div class="italic text-[11px]">Click any country row above to load its full Quad-Lens ecosystem deep dive.</div>
              </div>
            </div>

            <!-- INTERACTIVE DECISION SIMULATOR: GEEAP & EDTECH HUB LIFECYCLE MODEL -->'''

    if matrix_section_target not in html:
        print("Error: matrix_section_target not found in index.html!")
        return 1

    html = html.replace(matrix_section_target, macro_table_markup)

    # --------------------------------------------------------------------------
    # 3. Inject JavaScript Data & Rendering Engine
    # --------------------------------------------------------------------------
    js_target = '// SYSTEMIC DATA: 7-COUNTRY EMPIRICAL DATA STORE & DEEP-DIVE ENGINES'

    engine_code = f"""// =================================================================
    // MACRO-FISCAL & EXTERNAL AID OBSERVATORY DATASET (IMF + IATI)
    // =================================================================
    {js_inline}

    function renderLens4MacroFiscal(iso) {{
      if (typeof MACRO_FISCAL_DATA === 'undefined') return;
      const cData = MACRO_FISCAL_DATA.countries?.[iso];
      if (!cData) return;

      const dom = cData.domestic_fiscal || {{}};
      const ext = cData.external_assistance || {{}};
      const cliff = cData.recurrent_cliff_analysis || {{}};

      const srcEl = document.getElementById('lens4-source');
      if (srcEl) srcEl.textContent = dom.source + ' · ' + ext.source;

      const headEl = document.getElementById('lens4-heading');
      if (headEl) headEl.textContent = 'The CapEx Trap & The Recurrent Cliff';

      const descEl = document.getElementById('lens4-desc');
      if (descEl) descEl.textContent = cliff.narrative;

      const badgeEl = document.getElementById('lens4-cliff-badge');
      if (badgeEl) {{
        badgeEl.textContent = cliff.cliff_risk_tier;
        if (cliff.cliff_risk_tier.includes('High Tension')) {{
          badgeEl.className = 'badge-pill bg-rose-100 text-rose-800 border border-rose-300 font-bold text-[10px] whitespace-nowrap';
        }} else if (cliff.cliff_risk_tier.includes('Severe')) {{
          badgeEl.className = 'badge-pill bg-amber-100 text-amber-800 border border-amber-300 font-bold text-[10px] whitespace-nowrap';
        }} else if (cliff.cliff_risk_tier.includes('Self-Financed')) {{
          badgeEl.className = 'badge-pill bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold text-[10px] whitespace-nowrap';
        }} else {{
          badgeEl.className = 'badge-pill bg-blue-100 text-blue-800 border border-blue-300 font-bold text-[10px] whitespace-nowrap';
        }}
      }}

      const eduBudgetEl = document.getElementById('lens4-edu-budget');
      if (eduBudgetEl) eduBudgetEl.textContent = dom.education_pct_budget != null ? `${{dom.education_pct_budget}}%` : 'N/A';

      const commBudgetEl = document.getElementById('lens4-comm-budget');
      if (commBudgetEl) commBudgetEl.textContent = dom.communication_pct_budget != null ? `${{dom.communication_pct_budget}}%` : 'Unreported';

      const gapRatioEl = document.getElementById('lens4-gap-ratio');
      if (gapRatioEl) {{
        if (cliff.domestic_edu_to_comm_ratio != null) {{
          gapRatioEl.textContent = `${{cliff.domestic_edu_to_comm_ratio}}:1 Gap`;
          gapRatioEl.className = 'font-bold text-rose-700 bg-rose-100/90 px-1.5 py-0.5 rounded text-[10px] font-mono';
        }} else {{
          gapRatioEl.textContent = 'No Comm COFOG';
          gapRatioEl.className = 'text-slate-400 text-[10px] font-mono';
        }}
      }}

      const aid8yrEl = document.getElementById('lens4-aid-8yr');
      if (aid8yrEl) aid8yrEl.textContent = `$${{ext.education_disbursed_8yr_usd_m?.toLocaleString() || 0}}M`;

      const covidSurgeEl = document.getElementById('lens4-covid-surge');
      if (covidSurgeEl) {{
        const surge = ext.covid_2020_surge || {{}};
        if (surge.surge_growth_pct != null) {{
          const sign = surge.surge_absolute_usd_m >= 0 ? '+' : '';
          covidSurgeEl.textContent = `${{sign}}$${{surge.surge_absolute_usd_m}}M (${{sign}}${{surge.surge_growth_pct}}%)`;
        }} else {{
          covidSurgeEl.textContent = 'Baseline 2020';
        }}
      }}

      const barContainer = document.getElementById('lens4-timeseries-bars');
      if (barContainer && ext.annual_timeseries) {{
        const ts = ext.annual_timeseries;
        const years = ['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'];
        const values = years.map(yr => ts[yr]?.education_disbursements_usd_m || 0);
        const maxVal = Math.max(...values, 1.0);

        barContainer.innerHTML = years.map((yr, idx) => {{
          const val = values[idx];
          const heightPct = Math.max(14, Math.round((val / maxVal) * 100));
          const isCovid = yr === '2020';
          const barBg = isCovid ? 'bg-amber-500 group-hover:bg-amber-600' : 'bg-blue-600 group-hover:bg-blue-700';
          return `
            <div class="flex-1 flex flex-col items-center group relative cursor-pointer" title="${{yr}}: $${{val.toFixed(1)}}M USD disbursed">
              <div class="text-[9px] font-mono text-slate-500 group-hover:text-slate-900 group-hover:font-bold mb-0.5 opacity-0 group-hover:opacity-100 transition-opacity">$${{val.toFixed(0)}}M</div>
              <div class="w-full ${{barBg}} rounded-t transition-all duration-300" style="height: ${{heightPct}}%"></div>
              <div class="text-[9px] font-mono mt-1 ${{isCovid ? 'text-amber-800 font-black' : 'text-slate-500'}}">${{yr.slice(2)}}'</div>
            </div>
          `;
        }}).join('');
      }}
    }}

    function renderMacroFiscalTable() {{
      if (typeof MACRO_FISCAL_DATA === 'undefined') return;
      const tbody = document.getElementById('macro-fiscal-table-tbody');
      if (!tbody) return;

      const rows = MACRO_FISCAL_DATA.comparison_table || [];
      const flags = {{ 'KEN': '🇰🇪', 'RWA': '🇷🇼', 'TZA': '🇹🇿', 'MUS': '🇲🇺', 'GHA': '🇬🇭', 'NGA': '🇳🇬', 'ZMB': '🇿🇲' }};

      tbody.innerHTML = rows.map(r => {{
        const flag = flags[r.iso3] || '🌍';
        const eduB = r.edu_pct_budget != null ? `${{r.edu_pct_budget}}%` : '<span class="text-slate-400">N/A</span>';
        const commB = r.comm_pct_budget != null ? `${{r.comm_pct_budget}}%` : '<span class="text-slate-400 italic">Unreported</span>';
        
        let ratioStr = '<span class="text-slate-400">-</span>';
        if (r.edu_pct_budget && r.comm_pct_budget) {{
          const ratio = (r.edu_pct_budget / r.comm_pct_budget).toFixed(1);
          ratioStr = `<span class="font-bold text-rose-700 bg-rose-50 px-1.5 py-0.5 rounded font-mono">${{ratio}}:1</span>`;
        }}

        const covidStr = r.covid_2020_disb_usd_m != null ? `$${{r.covid_2020_disb_usd_m}}M` : '<span class="text-slate-400">-</span>';

        let riskBadge = 'bg-slate-100 text-slate-700';
        if (r.cliff_risk.includes('High Tension')) riskBadge = 'bg-rose-100 text-rose-800 border border-rose-200';
        else if (r.cliff_risk.includes('Severe')) riskBadge = 'bg-amber-100 text-amber-800 border border-amber-200';
        else if (r.cliff_risk.includes('Self-Financed')) riskBadge = 'bg-emerald-100 text-emerald-800 border border-emerald-200';
        else if (r.cliff_risk.includes('High External')) riskBadge = 'bg-blue-100 text-blue-800 border border-blue-200';

        return `
          <tr class="hover:bg-slate-50 cursor-pointer transition" onclick="selectCountry('${{r.iso3}}')">
            <td class="p-3 font-semibold text-slate-900 flex items-center gap-2">
              <span class="text-base">${{flag}}</span>
              <div>
                <div class="font-bold">${{r.name}} (${{r.iso3}})</div>
              </div>
            </td>
            <td class="p-3 font-extrabold text-blue-800">${{eduB}}</td>
            <td class="p-3 font-semibold text-amber-800">${{commB}}</td>
            <td class="p-3">${{ratioStr}}</td>
            <td class="p-3 font-extrabold text-purple-800">$${{r.edu_aid_disb_usd_m?.toLocaleString() || 0}}M</td>
            <td class="p-3 font-bold text-emerald-700">${{covidStr}}</td>
            <td class="p-3">
              <span class="badge-pill ${{riskBadge}} text-[10px] font-bold">${{r.cliff_risk}}</span>
            </td>
          </tr>
        `;
      }}).join('');
    }}

    // SYSTEMIC DATA: 7-COUNTRY EMPIRICAL DATA STORE & DEEP-DIVE ENGINES"""

    if js_target not in html:
        print("Error: js_target not found in index.html!")
        return 1

    html = html.replace(js_target, engine_code)

    # --------------------------------------------------------------------------
    # 4. Connect renderLens4MacroFiscal(iso) inside renderDeepDive(iso, segment)
    # --------------------------------------------------------------------------
    render_dd_target = "if (document.getElementById('quad-pol-outreach')) document.getElementById('quad-pol-outreach').textContent = dd.lens4.outreachRate;"
    render_dd_replacement = """if (document.getElementById('quad-pol-outreach')) document.getElementById('quad-pol-outreach').textContent = dd.lens4.outreachRate;

      // Render Enhanced Macro-Fiscal & External Aid Reality
      renderLens4MacroFiscal(iso);"""

    if render_dd_target not in html:
        print("Error: render_dd_target not found in index.html!")
        return 1

    html = html.replace(render_dd_target, render_dd_replacement)

    # --------------------------------------------------------------------------
    # 5. Initialize Macro-Fiscal Table on DOM Load
    # --------------------------------------------------------------------------
    init_target = "selectCountry('KEN');"
    init_replacement = """selectCountry('KEN');
      renderMacroFiscalTable();"""

    if init_target not in html:
        print("Error: init_target not found in index.html!")
        return 1

    html = html.replace(init_target, init_replacement)

    # Write updated index.html
    html_path.write_text(html, encoding='utf-8')
    print("Successfully injected Macro-Fiscal & Aid UI into index.html!")
    return 0

if __name__ == '__main__':
    exit(main())
