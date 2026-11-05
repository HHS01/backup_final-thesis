with open('/workspaces/CC_3/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '''        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
          <h3 class="font-bold text-slate-900 text-lg mb-3 font-serif">Master Discrepancy Matrix Visualization</h3>
          <p class="text-xs text-slate-600 mb-4">
            Triangulating the 4 pilot archetypes across the 3 core structural gaps: Connectivity, Sustainability, and Linguistic Inclusion.
          </p>
          <img src="./data/analysis_b/master_discrepancy_matrix.png" alt="Master Discrepancy Matrix" class="w-full max-h-[460px] object-contain mx-auto rounded-lg shadow-sm border border-slate-100">
        </div>
      </div>'''

supply_matrix_markup = '''        <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm mb-8">
          <h3 class="font-bold text-slate-900 text-lg mb-3 font-serif">Master Discrepancy Matrix Visualization</h3>
          <p class="text-xs text-slate-600 mb-4">
            Triangulating the 4 pilot archetypes across the 3 core structural gaps: Connectivity, Sustainability, and Linguistic Inclusion.
          </p>
          <img src="./data/analysis_b/master_discrepancy_matrix.png" alt="Master Discrepancy Matrix" class="w-full max-h-[460px] object-contain mx-auto rounded-lg shadow-sm border border-slate-100">
        </div>

        <!-- ================================================================= -->
        <!-- SUPPLY-DEMAND MISMATCH MATRIX & TRANSPARENT PROXY OBSERVATORY     -->
        <!-- ================================================================= -->
        <div class="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm">
          <div class="flex flex-wrap items-center justify-between gap-4 pb-5 border-b border-slate-200 mb-6">
            <div>
              <div class="flex items-center gap-2 mb-1.5">
                <span class="badge-pill bg-indigo-100 text-indigo-800 text-xs font-bold">Empirical Macro Layer</span>
                <span class="badge-pill bg-amber-100 text-amber-800 text-xs font-mono">PISA Blind Spot &amp; Proxy Badges</span>
              </div>
              <h3 class="text-xl sm:text-2xl font-extrabold text-slate-900 font-serif">Supply-Demand Mismatch Matrix (48 SSA Demand vs. 148 Supply)</h3>
              <p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-4xl">
                Contrasting foundational national learning poverty and infrastructure scarcity against active market solutions. Highlighting the <strong>PISA Data Blind Spot</strong> with transparent proxy indicators where official learning poverty is unmeasured.
              </p>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <span class="font-bold text-slate-500">Player Scope:</span>
              <button onclick="setMatrixPlayerScope('core')" id="btn-scope-core" class="px-3 py-1.5 rounded-lg font-bold bg-slate-900 text-white shadow-sm transition">
                Core 25 Cohort
              </button>
              <button onclick="setMatrixPlayerScope('all_ssa')" id="btn-scope-ssa" class="px-3 py-1.5 rounded-lg font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 transition">
                All 118 SSA Players
              </button>
              <button onclick="setMatrixPlayerScope('mena_tier')" id="btn-scope-mena" class="px-3 py-1.5 rounded-lg font-semibold bg-white border border-slate-200 text-slate-500 hover:bg-slate-50 transition">
                MENA Reference (21)
              </button>
            </div>
          </div>

          <!-- Domain Cluster Filters & Controls -->
          <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
            <div class="flex flex-wrap items-center gap-1.5 text-xs" id="matrix-domain-filters">
              <span class="font-bold text-slate-400 uppercase text-[10px] mr-1">Clustered Domain:</span>
              <button onclick="filterMatrixDomain('ALL')" class="matrix-domain-btn px-2.5 py-1 rounded-md text-xs font-bold bg-indigo-700 text-white" data-domain="ALL">All Domains</button>
              <button onclick="filterMatrixDomain('K-12 & Foundational')" class="matrix-domain-btn px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200" data-domain="K-12 & Foundational">📚 K-12 &amp; Foundational</button>
              <button onclick="filterMatrixDomain('Digital Content & Literacy')" class="matrix-domain-btn px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200" data-domain="Digital Content & Literacy">📖 Content &amp; Literacy</button>
              <button onclick="filterMatrixDomain('Learning Platforms & LMS')" class="matrix-domain-btn px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200" data-domain="Learning Platforms & LMS">💻 Platforms &amp; LMS</button>
              <button onclick="filterMatrixDomain('Workforce, TVET & Skills')" class="matrix-domain-btn px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200" data-domain="Workforce, TVET & Skills">🔧 TVET &amp; Skills</button>
              <button onclick="filterMatrixDomain('AI, Inclusion & Frontier')" class="matrix-domain-btn px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-700 hover:bg-slate-200" data-domain="AI, Inclusion & Frontier">🤖 AI &amp; Inclusion</button>
            </div>
            <div class="flex items-center gap-2 text-xs">
              <input type="text" id="matrix-search" placeholder="Search country or player..." oninput="renderSupplyMatrix()" class="px-2.5 py-1 rounded-lg border border-slate-200 text-xs w-48 focus:ring-1 focus:ring-indigo-500">
            </div>
          </div>

          <!-- Methodological Epistemic Callout -->
          <div class="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200 text-xs text-amber-900 mb-4 flex items-start gap-2.5">
            <span class="text-base">🔍</span>
            <div class="leading-relaxed">
              <strong>Methodological Transparency Anchor:</strong>
              Cells marked with <span class="badge-pill bg-amber-200 text-amber-900 text-[10px] py-0 px-1.5 font-bold">PROXY</span> denote countries where World Bank 2022–2025 standardized Learning Poverty is unmeasured. Rather than dropping these nations (creating digital austerity) or assuming 0%, the observatory anchors on UNESCO Adult Illiteracy deficit (<code class="text-[10px] font-mono">100 - Adult Literacy Rate</code>) as an explicit proxy, confronting the PISA data blind spot directly.
            </div>
          </div>

          <!-- Matrix Table Container -->
          <div class="overflow-x-auto border border-slate-200 rounded-xl max-h-[560px] relative">
            <table class="w-full text-left text-xs border-collapse divide-y divide-slate-200" id="matrix-table">
              <thead class="bg-slate-50 sticky top-0 z-20 text-slate-700 font-bold border-b border-slate-200 shadow-sm">
                <tr>
                  <th class="p-3 bg-slate-50 sticky left-0 z-30 min-w-[170px] border-r border-slate-200">Country &amp; Macro Need</th>
                  <th class="p-3 min-w-[120px]">Demand: Learning Poverty</th>
                  <th class="p-3 min-w-[110px]">Rural Electrification</th>
                  <th class="p-3 min-w-[110px]">School / Fixed BB</th>
                  <th class="p-3 min-w-[340px]">Mapped Market Solutions &amp; Alignment Fit</th>
                </tr>
              </thead>
              <tbody id="matrix-table-tbody" class="divide-y divide-slate-100 bg-white">
                <!-- Dynamically populated by JS -->
              </tbody>
            </table>
          </div>

          <!-- Footer Count & Summary -->
          <div class="mt-4 pt-3 border-t border-slate-200 flex flex-wrap items-center justify-between text-xs text-slate-500">
            <div id="matrix-counts-summary">Showing 48 Sub-Saharan Africa demand profiles matched against curated EdTech supply.</div>
            <div class="flex items-center gap-3">
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Verified Core SSA</span>
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-amber-500"></span> Proxy Indicator</span>
              <span class="flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-slate-400"></span> MENA Comparison</span>
            </div>
          </div>

        </div>
      </div>'''

if target not in html:
    print("Error: target not found!")
    exit(1)

html = html.replace(target, supply_matrix_markup)

with open('/workspaces/CC_3/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully injected Supply-Demand Matrix markup into Tab 4!")
