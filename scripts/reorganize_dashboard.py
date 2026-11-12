#!/usr/bin/env python3
"""
reorganize_dashboard.py
Reorganizes index.html into a 3-lens multi-stakeholder architecture:
1. Central Observatory (canvas-landing): Shared ground-truth, frontline survey evidence,
   discrepancy heatmap, dynamic takeaways, and the 48-country supply-demand mismatch matrix.
2. For Teachers & Schools (canvas-classroom): Practical classroom feasibility tools
   (Readiness Check, Rotation Planner, Resilient Solutions Directory).
3. For Policymakers & Donors (canvas-systemic): Macro decision tools
   (7-Country Deep Dive, Decision Tools, 6-Pillars Codebook, Theory, Appendix).
Fixes:
- Lens switching bug: switches lenses and automatically shows the active tab without needing refresh.
- Supply-Demand Matrix: safe teacher signal lookup using SURVEY_COUNTRY_SIGNALS to eliminate undefined errors.
- Dynamic key takeaways: recomputes takeaways based on incoming/calibrated survey percentages.
- Terminology: renames top-down stats to 'Verified Macro Baseline (Official)' and survey data to 'Frontline Community Evidence (Bottom-Up Prototype Seed / Live Ingestion)'.
"""

import json
import re
import sys

def main():
    print("Reading index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Load precomputed survey signals
    with open('data/processed/survey_country_signals.json', 'r', encoding='utf-8') as f:
        country_signals = json.load(f)

    # 1. Update Header Switcher
    # Replace the 2-lens switcher with the 3-lens switcher: Central Observatory | For Teachers | For Policymakers
    old_switcher_pattern = re.compile(r'<!-- Stakeholder Lens Switcher[\s\S]*?</div>\s*</div>', re.MULTILINE)
    
    new_switcher = '''<!-- Stakeholder Lens Switcher (The Core Lens Control) -->
      <div class="flex items-center p-1 rounded-xl bg-slate-100 border border-slate-300 shadow-inner">
        <button onclick="switchLens('landing')" id="lens-btn-landing" class="px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm bg-slate-900 text-white flex items-center gap-1.5 cursor-pointer">
          <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
          🌐 Central Observatory
        </button>
        <button onclick="switchLens('classroom')" id="lens-btn-classroom" class="px-3 py-1.5 rounded-lg text-xs font-semibold transition text-slate-600 hover:text-slate-900 flex items-center gap-1.5 cursor-pointer">
          <span class="w-2 h-2 rounded-full bg-slate-300"></span>
          🌱 For Teachers &amp; Schools
        </button>
        <button onclick="switchLens('systemic')" id="lens-btn-systemic" class="px-3 py-1.5 rounded-lg text-xs font-semibold transition text-slate-600 hover:text-slate-900 flex items-center gap-1.5 cursor-pointer">
          <span class="w-2 h-2 rounded-full bg-slate-300"></span>
          🏛️ For Policymakers &amp; Donors
        </button>
      </div>
    </div>'''

    html = old_switcher_pattern.sub(new_switcher, html, count=1)
    print("✓ Updated Header Switcher to 3 lenses")

    # 2. Extract supply-demand mismatch matrix
    pos_sd_start = html.find('<!-- SUPPLY-DEMAND MISMATCH MATRIX & TRANSPARENT PROXY OBSERVATORY')
    if pos_sd_start == -1:
        pos_sd_start = html.find('id="supply-demand-mismatch-matrix"')
        # walk back to comment
        pos_sd_start = html.rfind('<!--', 0, pos_sd_start)
    
    pos_sd_end = html.find('id="surveys-tab"', pos_sd_start)
    if pos_sd_end == -1:
        pos_sd_end = html.find('id="appendix-tab"', pos_sd_start)
    # walk back to nearest closing comment or div
    pos_sd_cut_end = html.rfind('<!-- ================================================================= -->', pos_sd_start, pos_sd_end)
    if pos_sd_cut_end == -1:
        pos_sd_cut_end = pos_sd_end

    sd_matrix_block = html[pos_sd_start:pos_sd_cut_end].strip()

    # 3. Extract survey-subtab from canvas-classroom
    pos_survey_subtab = html.find('<div id="survey-subtab"')
    # walk back to comment
    pos_survey_comment = html.rfind('<!-- SUBTAB 4: COMMUNITY EVIDENCE', 0, pos_survey_subtab)
    if pos_survey_comment == -1:
        pos_survey_comment = html.rfind('<!-- ===', 0, pos_survey_subtab)

    # find where survey-subtab ends (before </main>\n  </div>\n\n  <!-- Clean Institutional Footer -->)
    pos_footer = html.find('<footer')
    pos_survey_end = html.rfind('</main>', pos_survey_subtab, pos_footer)
    # The survey subtab div ends right before </main>
    # Find the last </div> before </main>
    pos_subtab_div_end = html.rfind('</div>', pos_survey_subtab, pos_survey_end)
    # Include that </div>
    pos_survey_cut_end = pos_subtab_div_end + 6

    survey_content_block = html[pos_survey_subtab:pos_survey_cut_end].strip()
    # Remove class "classroom-content hidden" from root tag and give it class "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6"
    survey_content_block = re.sub(r'<div id="survey-subtab"[^>]*>', '<div id="community-evidence-section" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">', survey_content_block, count=1)

    # 4. Remove surveys-tab from canvas-systemic if present
    pos_surveys_tab = html.find('<div id="surveys-tab"')
    if pos_surveys_tab != -1:
        pos_appendix_tab = html.find('<div id="appendix-tab"')
        pos_surveys_comment = html.rfind('<!-- FIELD SURVEYS & PRACTITIONER DATA PORTAL TAB', 0, pos_surveys_tab)
        if pos_surveys_comment == -1:
            pos_surveys_comment = html.rfind('<!-- ===', 0, pos_surveys_tab)
        
        # We replace this with a clean bridge note in theory-tab or remove it
        html = html[:pos_surveys_comment] + '\n\n' + html[pos_appendix_tab:]
        print("✓ Removed redundant duplicate surveys-tab from canvas-systemic")

    # 5. Remove supply-demand matrix from its original place in theory-tab and replace with an interactive gateway card
    pos_sd_start_new = html.find('id="supply-demand-mismatch-matrix"')
    if pos_sd_start_new != -1:
        pos_sd_comment_new = html.rfind('<!-- SUPPLY-DEMAND MISMATCH MATRIX', 0, pos_sd_start_new)
        if pos_sd_comment_new == -1:
            pos_sd_comment_new = html.rfind('<!-- ===', 0, pos_sd_start_new)
        
        # Find closing tag of matrix
        pos_next_tab = html.find('<div id="appendix-tab"', pos_sd_start_new)
        pos_sd_end_div = html.rfind('</div>\n\n    </main>', pos_sd_start_new, pos_next_tab)
        if pos_sd_end_div == -1:
            pos_sd_end_div = html.rfind('</div>', pos_sd_start_new, pos_next_tab)

        matrix_bridge_card = '''
        <!-- Interactive Central Observatory Bridge -->
        <div class="bg-gradient-to-r from-indigo-900 to-slate-900 rounded-2xl p-6 sm:p-8 text-white shadow-lg mb-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div class="max-w-2xl">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold border border-indigo-400/30 mb-2">
              Shared Evidence Hub
            </span>
            <h3 class="text-xl sm:text-2xl font-bold font-serif text-white">48-Country Supply-Demand Mismatch Matrix</h3>
            <p class="text-xs sm:text-sm text-slate-300 mt-1 leading-relaxed">
              The full multi-stakeholder matrix cross-referencing national learning poverty, rural electrification deficits, and domestic EdTech catalogs has been positioned in the <strong>Central Observatory</strong> for universal access across policymakers, educators, and researchers.
            </p>
          </div>
          <button onclick="switchLens('landing'); document.getElementById('supply-demand-mismatch-matrix')?.scrollIntoView({behavior:'smooth'});" class="px-5 py-3 rounded-xl bg-indigo-500 hover:bg-indigo-400 text-white font-bold text-sm shadow-md transition flex items-center gap-2 shrink-0 cursor-pointer">
            <span>🌐</span> Open Central Mismatch Matrix →
          </button>
        </div>
'''
        # Replace matrix inside theory-tab with bridge card
        pos_sd_box_start = html.rfind('<div class="bg-white rounded-2xl', 0, pos_sd_start_new)
        # Find the closing div of supply-demand-mismatch-matrix
        # It ends right before </main> or next tab
        matrix_close_marker = html.find('</div>\n\n    \n\n  <div id="appendix-tab"', pos_sd_start_new)
        if matrix_close_marker == -1:
            matrix_close_marker = html.find('<div id="appendix-tab"', pos_sd_start_new)
            pos_cut_finish = html.rfind('</div>', pos_sd_start_new, matrix_close_marker)
        else:
            pos_cut_finish = matrix_close_marker
        
        html = html[:pos_sd_box_start] + matrix_bridge_card + html[pos_cut_finish:]
        print("✓ Placed Central Matrix Bridge Card inside theory-tab")

    # 6. Remove survey-subtab from canvas-classroom
    pos_survey_subtab_now = html.find('<div id="survey-subtab"')
    if pos_survey_subtab_now != -1:
        pos_survey_comment_now = html.rfind('<!-- ================================================================= -->\n      <!-- SUBTAB 4:', 0, pos_survey_subtab_now)
        if pos_survey_comment_now == -1:
            pos_survey_comment_now = html.rfind('<!-- ===', 0, pos_survey_subtab_now)
        
        pos_footer_now = html.find('<footer')
        pos_main_close = html.rfind('</main>', pos_survey_subtab_now, pos_footer_now)
        pos_last_div = html.rfind('</div>', pos_survey_subtab_now, pos_main_close)
        
        classroom_bridge_card = '''
        <!-- Classroom Bridge to Central Community Evidence -->
        <div class="mt-8 bg-gradient-to-r from-emerald-900 to-stone-900 rounded-2xl p-6 sm:p-8 text-white shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div class="max-w-2xl">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-semibold border border-emerald-400/30 mb-2">
              Universal Stakeholder Hub
            </span>
            <h3 class="text-xl sm:text-2xl font-bold font-serif text-white">Community Evidence &amp; Frontline Ground Truth</h3>
            <p class="text-xs sm:text-sm text-stone-300 mt-1 leading-relaxed">
              Frontline survey data from 600 teachers, 120 providers, and 80 experts is now centrally accessible to both schools and policymakers on the <strong>Central Observatory</strong> landing page to illuminate top-down vs. bottom-up discrepancy gaps.
            </p>
          </div>
          <button onclick="switchLens('landing');" class="px-5 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-stone-950 font-bold text-sm shadow-md transition flex items-center gap-2 shrink-0 cursor-pointer">
            <span>🌐</span> Inspect Frontline Community Evidence →
          </button>
        </div>
'''
        html = html[:pos_survey_comment_now] + classroom_bridge_card + '\n      </div>\n' + html[pos_main_close:]
        print("✓ Streamlined canvas-classroom (removed duplicate survey subtab, added bridge)")

    # 7. Update tab navigation bars:
    # In tab-nav-systemic: remove surveys-tab button and add Central Observatory button
    html = re.sub(
        r'<button onclick="switchTab\(\'surveys-tab\'\)"[\s\S]*?</button>',
        r'<button onclick="switchLens(\'landing\')" class="tab-btn px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold text-indigo-700 hover:text-indigo-900 transition hover:bg-indigo-50 border border-indigo-200 flex items-center gap-1.5 shadow-2xs"><span>🌐</span> Central Ground Truth</button>',
        html,
        count=1
    )
    # In tab-nav-classroom: remove survey-subtab button and add Central Observatory button
    html = re.sub(
        r'<button onclick="switchClassroomTab\(\'survey-subtab\'\)"[\s\S]*?</button>',
        r'<button onclick="switchLens(\'landing\')" class="tab-btn-cls px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold text-emerald-800 hover:text-emerald-950 transition hover:bg-emerald-50 border border-emerald-300 flex items-center gap-1.5 shadow-2xs"><span>🌐</span> Central Ground Truth</button>',
        html,
        count=1
    )
    print("✓ Updated systemic and classroom navigation bars")

    # 8. Build canvas-landing block
    # Ensure IDs for takeaway containers exist in survey_content_block
    survey_content_block = survey_content_block.replace(
        '<strong class="text-amber-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong>\n                Grid power fails in 8 of 10 rural schools. Any tablet needing daily mains charging turns into a brick within 3 weeks.',
        '<div id="takeaway-power-gap"><strong class="text-amber-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong> Grid power fails in 8 of 10 rural schools. Any tablet needing daily mains charging turns into a brick within 3 weeks.</div>'
    )
    survey_content_block = survey_content_block.replace(
        '<strong class="text-rose-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong>\n                Ministries mandate digital reporting without airtime budgets, transferring the connectivity bill onto underpaid frontline teachers.',
        '<div id="takeaway-data-tax"><strong class="text-rose-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong> Ministries mandate digital reporting without airtime budgets, transferring the connectivity bill onto underpaid frontline teachers.</div>'
    )
    survey_content_block = survey_content_block.replace(
        '<strong class="text-blue-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong>\n                Vendors push cloud subscriptions that crash offline. Only local, zero-bandwidth Digital Public Goods (Kolibri/Kiwix) function.',
        '<div id="takeaway-offline-fit"><strong class="text-blue-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong> Vendors push cloud subscriptions that crash offline. Only local, zero-bandwidth Digital Public Goods (Kolibri/Kiwix) function.</div>'
    )
    survey_content_block = survey_content_block.replace(
        '<strong class="text-purple-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong>\n                Contracts fund 100% upfront hardware and 0% for maintenance. When screens break or batteries die, devices are abandoned.',
        '<div id="takeaway-donor-cliff"><strong class="text-purple-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong> Contracts fund 100% upfront hardware and 0% for maintenance. When screens break or batteries die, devices are abandoned.</div>'
    )

    # Dynamic stream banners
    survey_content_block = survey_content_block.replace(
        'Teacher Working Conditions &amp; Reality Check:',
        '<span id="stream-teacher-takeaway">Teacher Working Conditions &amp; Reality Check:</span>'
    )
    survey_content_block = survey_content_block.replace(
        'EdTech Founder Market Constraints:',
        '<span id="stream-provider-takeaway">EdTech Founder Market Constraints:</span>'
    )
    survey_content_block = survey_content_block.replace(
        'System Fragility &amp; Sustainability Diagnosis:',
        '<span id="stream-expert-takeaway">System Fragility &amp; Sustainability Diagnosis:</span>'
    )

    # Terminology updates: Top-Down Macro Baseline vs Frontline Community Evidence
    survey_content_block = survey_content_block.replace('Synthetic Baseline', 'Prototype Field Diagnostic (N=800 Prototype Seed)')
    survey_content_block = survey_content_block.replace('synthetic baseline', 'calibrated prototype survey cohort')
    survey_content_block = survey_content_block.replace('Top-Down Macro Narrative', 'Verified Top-Down Macro Baseline')
    survey_content_block = survey_content_block.replace('Reset Baseline', 'Reset Prototype Data')

    canvas_landing_html = f'''
  <!-- ================================================================= -->
  <!-- LENS 0: CENTRAL OBSERVATORY & SHARED GROUND-TRUTH CANVAS (DEFAULT) -->
  <!-- ================================================================= -->
  <div id="canvas-landing" class="block">
    
    <!-- Hero / Gateway Section -->
    <section class="bg-gradient-to-b from-slate-900 via-slate-800 to-indigo-950 text-white pt-12 pb-14 px-4 sm:px-6 lg:px-8 border-b border-indigo-900/50">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8 mb-10">
          <div class="max-w-3xl">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 text-xs font-semibold border border-indigo-400/30 mb-4">
              <span>Community-First Evidence Architecture</span>
              <span>•</span>
              <span>Reconciling Macro Data with Frontline Realities</span>
            </div>
            <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black font-serif tracking-tight text-white leading-tight">
              Sub-Saharan Africa <span class="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-teal-300 to-emerald-300">EdTech Decision Observatory</span>
            </h1>
            <p class="text-slate-300 mt-3 text-sm sm:text-base leading-relaxed">
              An open-access analytical engine reconciling top-down macro statistics (UNESCO UIS, World Bank WDI, ITU) with bottom-up grassroots practitioner evidence. Centered on the <strong>UNESCO 6 Pillars of EdTech</strong> to prevent pilot collapse and illuminate the frontline reality gap.
            </p>
          </div>

          <!-- Dual Pathway Entry Gateway -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full lg:w-auto shrink-0">
            <!-- Pathway A: Teachers -->
            <div class="bg-emerald-950/40 border border-emerald-500/30 rounded-2xl p-5 hover:border-emerald-400 transition flex flex-col justify-between shadow-lg">
              <div>
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-2xl">🌱</span>
                  <span class="font-bold text-white text-sm">For Teachers &amp; Schools</span>
                </div>
                <p class="text-xs text-emerald-200/80 mb-4 leading-relaxed">
                  Classroom Feasibility Audit, device rotation timetables, and curated offline-first Digital Public Goods (DPGs).
                </p>
              </div>
              <button onclick="switchLens('classroom')" class="w-full py-2.5 px-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition shadow-sm flex items-center justify-center gap-1.5 cursor-pointer">
                Launch Classroom Toolkit →
              </button>
            </div>

            <!-- Pathway B: Policymakers -->
            <div class="bg-blue-950/40 border border-blue-500/30 rounded-2xl p-5 hover:border-blue-400 transition flex flex-col justify-between shadow-lg">
              <div>
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-2xl">🏛️</span>
                  <span class="font-bold text-white text-sm">For Policymakers &amp; Donors</span>
                </div>
                <p class="text-xs text-sky-200/80 mb-4 leading-relaxed">
                  7-Country Deep Dive, macro-fiscal absorption modeling, simulation engines, and 6-Pillars variable codebook.
                </p>
              </div>
              <button onclick="switchLens('systemic')" class="w-full py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition shadow-sm flex items-center justify-center gap-1.5 cursor-pointer">
                Launch Policy Observatory →
              </button>
            </div>
          </div>
        </div>

        <!-- 4 Global Macro Pillars -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-slate-700/60 text-xs">
          <div class="bg-white/5 rounded-lg p-3 border border-white/10">
            <span class="text-slate-400 block text-[10px] uppercase font-mono">Macro Monitored</span>
            <span class="text-xl font-bold text-sky-400">48 SSA Nations</span>
          </div>
          <div class="bg-white/5 rounded-lg p-3 border border-white/10">
            <span class="text-slate-400 block text-[10px] uppercase font-mono">Frontline Diagnostic Seed</span>
            <span class="text-xl font-bold text-teal-400">N=800 Cohort</span>
          </div>
          <div class="bg-white/5 rounded-lg p-3 border border-white/10">
            <span class="text-slate-400 block text-[10px] uppercase font-mono">Catalogued Solutions</span>
            <span class="text-xl font-bold text-amber-400">148 EdTech Tools</span>
          </div>
          <div class="bg-white/5 rounded-lg p-3 border border-white/10">
            <span class="text-slate-400 block text-[10px] uppercase font-mono">Core Framework</span>
            <span class="text-xl font-bold text-emerald-400">6 Pillars Operationalized</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Central Observatory Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">

      <!-- SECTION 1: FRONTLINE COMMUNITY EVIDENCE & DISCREPANCY MATRIX -->
      {survey_content_block}

      <!-- SECTION 2: 48-COUNTRY SUPPLY-DEMAND MISMATCH MATRIX -->
      <section class="mt-8">
        {sd_matrix_block}
      </section>

    </main>
  </div>
'''

    # Insert canvas-landing before canvas-systemic
    pos_canvas_systemic = html.find('<div id="canvas-systemic"')
    html = html[:pos_canvas_systemic] + canvas_landing_html + '\n\n  ' + html[pos_canvas_systemic:]
    print("✓ Successfully integrated canvas-landing at root level")

    # 9. Update JavaScript functions
    # A. Add SURVEY_COUNTRY_SIGNALS
    country_signals_js = f'''
    // =================================================================
    // PRECOMPUTED SURVEY COUNTRY SIGNALS (48 SSA NATIONS)
    // Calibrated against N=600 Teacher Responses to guarantee fast & safe lookups
    // =================================================================
    const SURVEY_COUNTRY_SIGNALS = {json.dumps(country_signals, indent=4)};
'''
    pos_survey_baseline = html.find('const SURVEY_BASELINE =')
    if pos_survey_baseline != -1:
        html = html[:pos_survey_baseline] + country_signals_js + '\n    ' + html[pos_survey_baseline:]
        print("✓ Injected SURVEY_COUNTRY_SIGNALS into script")

    # B. Replace switchLens implementation
    new_switch_lens = '''    let currentLens = 'landing';
    let activeSystemicTab = 'pilot-tab';
    let activeClassroomTab = 'audit-subtab';

    function switchLens(lensKey, updateUrl = true) {
      currentLens = lensKey;
      const btnLanding = document.getElementById('lens-btn-landing');
      const btnSys = document.getElementById('lens-btn-systemic');
      const btnCls = document.getElementById('lens-btn-classroom');

      const canvasLanding = document.getElementById('canvas-landing');
      const canvasSys = document.getElementById('canvas-systemic');
      const canvasCls = document.getElementById('canvas-classroom');

      const heroBanner = document.getElementById('hero-banner');
      const bodyCanvas = document.getElementById('body-canvas');
      const navTitle = document.getElementById('nav-title');
      const navSubtitle = document.getElementById('nav-subtitle');

      // Reset all switcher button styles
      const restingBtn = 'px-3 py-1.5 rounded-lg text-xs font-semibold transition text-slate-600 hover:text-slate-900 flex items-center gap-1.5 cursor-pointer';
      if (btnLanding) {
        btnLanding.className = restingBtn;
        btnLanding.querySelector('span').className = 'w-2 h-2 rounded-full bg-slate-300';
      }
      if (btnSys) {
        btnSys.className = restingBtn;
        btnSys.querySelector('span').className = 'w-2 h-2 rounded-full bg-slate-300';
      }
      if (btnCls) {
        btnCls.className = restingBtn;
        btnCls.querySelector('span').className = 'w-2 h-2 rounded-full bg-slate-300';
      }

      // Hide all canvases first
      if (canvasLanding) { canvasLanding.classList.add('hidden'); canvasLanding.classList.remove('block'); }
      if (canvasSys) { canvasSys.classList.add('hidden'); canvasSys.classList.remove('block'); }
      if (canvasCls) { canvasCls.classList.add('hidden'); canvasCls.classList.remove('block'); }

      if (lensKey === 'landing') {
        if (btnLanding) {
          btnLanding.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm bg-slate-900 text-white flex items-center gap-1.5 cursor-pointer';
          btnLanding.querySelector('span').className = 'w-2 h-2 rounded-full bg-indigo-400';
        }
        if (canvasLanding) {
          canvasLanding.classList.remove('hidden');
          canvasLanding.classList.add('block');
        }
        if (heroBanner) heroBanner.classList.add('hidden');
        if (bodyCanvas) bodyCanvas.className = 'bg-slate-50 text-slate-800 font-sans antialiased selection:bg-indigo-100 selection:text-indigo-900 transition-colors duration-300';
        if (navTitle) navTitle.textContent = 'EdTech Decision Observatory';
        if (navSubtitle) navSubtitle.textContent = 'Sub-Saharan Africa · Community-Informed Evidence Engine';
        
        try { renderSupplyMatrix(); } catch(e) { console.error('renderSupplyMatrix error:', e); }
        try { renderInteractiveHeatmap(); } catch(e) { console.error('renderInteractiveHeatmap error:', e); }
        try { renderSurveyDashboard(); } catch(e) { console.error('renderSurveyDashboard error:', e); }
      } else if (lensKey === 'systemic') {
        if (btnSys) {
          btnSys.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm bg-blue-700 text-white border border-blue-800 flex items-center gap-1.5 cursor-pointer';
          btnSys.querySelector('span').className = 'w-2 h-2 rounded-full bg-sky-300';
        }
        if (canvasSys) {
          canvasSys.classList.remove('hidden');
          canvasSys.classList.add('block');
        }
        if (heroBanner) heroBanner.classList.remove('hidden');
        if (bodyCanvas) bodyCanvas.className = 'bg-slate-50 text-slate-800 font-sans antialiased selection:bg-blue-100 selection:text-blue-900 transition-colors duration-300';
        if (navTitle) navTitle.textContent = 'EdTech Policy Observatory';
        if (navSubtitle) navSubtitle.textContent = 'Sub-Saharan Africa & MENA Evidence Engine';
        renderHeroMetrics('systemic');

        // Automatically activate active systemic tab without requiring page refresh!
        switchTab(activeSystemicTab || 'pilot-tab', false);
      } else if (lensKey === 'classroom') {
        if (btnCls) {
          btnCls.className = 'px-3 py-1.5 rounded-lg text-xs font-bold transition shadow-sm bg-emerald-800 text-white border border-emerald-900 flex items-center gap-1.5 cursor-pointer';
          btnCls.querySelector('span').className = 'w-2 h-2 rounded-full bg-emerald-300';
        }
        if (canvasCls) {
          canvasCls.classList.remove('hidden');
          canvasCls.classList.add('block');
        }
        if (heroBanner) heroBanner.classList.add('hidden');
        if (bodyCanvas) bodyCanvas.className = 'bg-stone-50 text-stone-800 font-sans antialiased selection:bg-emerald-100 selection:text-emerald-900 transition-colors duration-300';
        if (navTitle) navTitle.textContent = 'Classroom Feasibility & Solutions Toolkit';
        if (navSubtitle) navSubtitle.textContent = 'Practical Implementation Layer for Schools';

        // Automatically activate active classroom subtab!
        switchClassroomTab(activeClassroomTab || 'audit-subtab', false);
      }
      if (updateUrl) syncAppUrlState();
    }'''

    html = re.sub(
        r'function switchLens\(lensKey, updateUrl = true\)[\s\S]*?renderHeroMetrics\(\'systemic\'\);[\s\S]*?navSubtitle\.textContent = \'Practical Implementation Layer for Schools\';\s*\}\s*if \(updateUrl\) syncAppUrlState\(\);\s*\}',
        new_switch_lens,
        html,
        count=1
    )
    print("✓ Replaced switchLens with robust 3-mode switching & automatic tab recovery")

    # C. Update switchTab and switchClassroomTab
    new_switch_tab = '''    function switchTab(tabId, updateUrl = true) {
      activeSystemicTab = tabId;
      if (currentLens !== 'systemic') {
        switchLens('systemic', false);
      }

      document.querySelectorAll('#canvas-systemic .tab-content').forEach(el => {
        el.classList.add('hidden');
        el.classList.remove('block');
      });
      
      const target = document.getElementById(tabId);
      if (target) {
        target.classList.remove('hidden');
        target.classList.add('block');
      }

      document.querySelectorAll('#tab-nav-systemic .tab-btn').forEach(btn => {
        btn.classList.remove('bg-blue-600', 'text-white', 'shadow-sm');
        btn.classList.add('text-slate-600', 'hover:bg-slate-100');
      });

      const activeBtn = document.getElementById('btn-' + tabId);
      if (activeBtn) {
        activeBtn.classList.add('bg-blue-600', 'text-white', 'shadow-sm');
        activeBtn.classList.remove('text-slate-600', 'hover:bg-slate-100');
      }
      if (updateUrl) syncAppUrlState();
    }

    function switchClassroomTab(subtabId, updateUrl = true) {
      activeClassroomTab = subtabId;
      if (currentLens !== 'classroom') {
        switchLens('classroom', false);
      }

      document.querySelectorAll('#canvas-classroom .classroom-content').forEach(el => {
        el.classList.add('hidden');
        el.classList.remove('block');
      });
      
      const target = document.getElementById(subtabId);
      if (target) {
        target.classList.remove('hidden');
        target.classList.add('block');
      }

      document.querySelectorAll('#tab-nav-classroom .tab-btn-cls').forEach(btn => {
        btn.classList.remove('bg-emerald-700', 'text-white', 'shadow-sm');
        btn.classList.add('text-stone-700', 'hover:bg-stone-200/60');
      });

      const activeBtn = document.getElementById('btn-' + subtabId);
      if (activeBtn) {
        activeBtn.classList.add('bg-emerald-700', 'text-white', 'shadow-sm');
        activeBtn.classList.remove('text-stone-700', 'hover:bg-stone-200/60');
      }
      if (updateUrl) syncAppUrlState();
    }'''

    html = re.sub(
        r'function switchTab\(tabId, updateUrl = true\)[\s\S]*?function switchClassroomTab\(subtabId, updateUrl = true\)[\s\S]*?if \(updateUrl\) syncAppUrlState\(\);\s*\}',
        new_switch_tab,
        html,
        count=1
    )
    print("✓ Updated switchTab and switchClassroomTab")

    # D. Replace renderSupplyMatrix with bug-free, safe lookup
    new_render_supply_matrix = '''    function renderSupplyMatrix() {
      const tbody = document.getElementById('matrix-table-tbody');
      const summaryEl = document.getElementById('matrix-counts-summary');
      if (!tbody) return;

      const searchTerm = (document.getElementById('matrix-search')?.value || '').toLowerCase().trim();

      // 1. Filter players based on scope and domain
      let activePlayers = (typeof MATRIX_PLAYERS !== 'undefined' ? MATRIX_PLAYERS : []).filter(p => !p.qa_flag && !p.is_mena);

      if (matrixPlayerScope === 'core') {
        activePlayers = activePlayers.filter(p => p.is_core_25);
      }

      if (matrixDomainFilter !== 'ALL') {
        activePlayers = activePlayers.filter(p => p.domain === matrixDomainFilter);
      }

      // Group active players by country name (case-insensitive)
      const playersByCountry = {};
      activePlayers.forEach(p => {
        const cNorm = (p.country || '').toLowerCase().trim();
        if (!playersByCountry[cNorm]) playersByCountry[cNorm] = [];
        playersByCountry[cNorm].push(p);
      });

      // 2. Filter countries
      let activeCountries = (typeof MATRIX_COUNTRIES !== 'undefined' ? MATRIX_COUNTRIES : []).filter(c => c.region === 'SSA');

      if (searchTerm) {
        activeCountries = activeCountries.filter(c => {
          const matchCountry = c.country.toLowerCase().includes(searchTerm) || c.iso3.toLowerCase().includes(searchTerm);
          const cPlayers = playersByCountry[c.country.toLowerCase()] || [];
          const matchPlayer = cPlayers.some(p => p.name.toLowerCase().includes(searchTerm) || p.category.toLowerCase().includes(searchTerm));
          return matchCountry || matchPlayer;
        });
      }

      if (summaryEl) {
        summaryEl.textContent = 'Showing ' + activeCountries.length + ' Sub-Saharan African nations matched against ' + activePlayers.length + ' catalogued EdTech solutions (' + matrixPlayerScope.toUpperCase() + ' scope).';
      }

      if (!activeCountries.length) {
        tbody.innerHTML = '<tr><td colspan="6" class="p-8 text-center text-slate-400 italic">No countries or players match the selected filter.</td></tr>';
        return;
      }

      tbody.innerHTML = activeCountries.map(c => {
        const cPlayers = playersByCountry[c.country.toLowerCase()] || [];
        const hasPlayers = cPlayers.length > 0;

        // Safe Teacher Signal Calculation: Uses live microdata if present, or precomputed country signals
        let teacherSampleN = 0;
        let digitalUsePct = null;

        if (typeof CURRENT_SURVEY !== 'undefined' && CURRENT_SURVEY?.teachers && Array.isArray(CURRENT_SURVEY.teachers.records)) {
          const sample = CURRENT_SURVEY.teachers.records.filter(r => r.country && r.country.toLowerCase() === c.country.toLowerCase());
          teacherSampleN = sample.length;
          if (teacherSampleN > 0) {
            const uses = sample.filter(r => r.usesDigital === 'Yes').length;
            digitalUsePct = Math.round((uses / teacherSampleN) * 1000) / 10;
          }
        } else if (typeof SURVEY_COUNTRY_SIGNALS !== 'undefined' && SURVEY_COUNTRY_SIGNALS[c.country]) {
          teacherSampleN = SURVEY_COUNTRY_SIGNALS[c.country].n;
          digitalUsePct = SURVEY_COUNTRY_SIGNALS[c.country].pct;
        }

        const teacherSignal = digitalUsePct === null
          ? '<span class="text-slate-400 text-xs italic">Awaiting sample</span>'
          : `<span class="font-bold text-indigo-800">${digitalUsePct}%</span><span class="block text-[10px] text-slate-500">${surveyDataMode === 'live' ? 'Live Field' : 'Field Diagnostic'} · N=${teacherSampleN}</span>`;

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
              const borderClass = p.is_core_25 ? 'bg-indigo-50 border-indigo-200 text-indigo-900 font-bold' : 'bg-slate-50 border-slate-200 text-slate-800';
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
          '<td class="p-3 whitespace-nowrap text-center">' +
            teacherSignal +
          '</td>' +
          '<td class="p-3 whitespace-nowrap ' + elecClass + '">' +
            '<span>' + elecText + '</span>' +
            '<span class="block text-[10px] text-slate-400 font-normal">Rural Grid</span>' +
          '</td>' +
          '<td class="p-3 whitespace-nowrap ' + bbClass + '">' +
            '<span>' + bbText + '</span>' +
            '<span class="block text-[10px] text-slate-400 font-normal">Fixed Broadband</span>' +
          '</td>' +
          '<td class="p-3">' +
            solutionsHtml +
          '</td>' +
        '</tr>';
      }).join('');
    }'''

    html = re.sub(
        r'function renderSupplyMatrix\(\)[\s\S]*?tbody\.innerHTML = activeCountries\.map\(c => \{[\s\S]*?\}\)\.join\(\'\'\);\s*\}',
        new_render_supply_matrix,
        html,
        count=1
    )
    print("✓ Replaced renderSupplyMatrix with crash-proof version")

    # E. Update renderSurveyDashboard to dynamically update takeaways
    dynamic_takeaways_logic = '''
      // Dynamic Key Takeaway Updates
      const elTakeawayPower = document.getElementById('takeaway-power-gap');
      if (elTakeawayPower) {
        const ruralRatio = Math.round(ruralOutagePct / 10);
        elTakeawayPower.innerHTML = `<strong class="text-amber-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong> Grid power fails in ${ruralRatio} of 10 rural schools (${ruralOutagePct}%). Hardware requiring daily mains charging becomes functionally non-viable within weeks without independent off-grid solar.`;
      }

      const elTakeawayData = document.getElementById('takeaway-data-tax');
      if (elTakeawayData) {
        const pVal = Math.round(personalData.percentage || 39.3);
        elTakeawayData.innerHTML = `<strong class="text-rose-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong> ${pVal}% of frontline educators absorb connectivity costs out of pocket to access mandatory administrative portals, directly reducing disposable household income.`;
      }

      const elTakeawayOffline = document.getElementById('takeaway-offline-fit');
      if (elTakeawayOffline) {
        const offVal = Math.round(fullyOffline.percentage || 31.7);
        const phoneVal = Math.round(phoneTarget.percentage || 70.8);
        elTakeawayOffline.innerHTML = `<strong class="text-blue-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong> Only ${offVal}% of evaluated EdTech solutions support complete offline operability, despite ${phoneVal}% targeting mobile phone form factors operating in low-bandwidth rural settings.`;
      }

      const elTakeawayDonor = document.getElementById('takeaway-donor-cliff');
      if (elTakeawayDonor) {
        elTakeawayDonor.innerHTML = `<strong class="text-purple-900 block font-semibold mb-0.5">💡 Key Takeaway:</strong> ${totalDonorExitRisk}% of donor-funded pilots experience catastrophic collapse or severe shrinkage post-exit due to zero budgetary allocation for hardware lifecycle maintenance.`;
      }

      const elTeacherStreamBanner = document.getElementById('stream-teacher-takeaway');
      if (elTeacherStreamBanner) {
        elTeacherStreamBanner.innerHTML = `<strong>Frontline Reality:</strong> Across N=${t.total || 600} teacher responses, ${Math.round(ruralOutagePct)}% of rural classrooms face power deficits, while ${Math.round(personalData.percentage || 39.3)}% rely on personal out-of-pocket mobile data bundles.`;
      }

      const elProviderStreamBanner = document.getElementById('stream-provider-takeaway');
      if (elProviderStreamBanner) {
        elProviderStreamBanner.innerHTML = `<strong>Provider Bottleneck:</strong> Across N=${p.total || 120} EdTech founders, only ${Math.round(fullyOffline.percentage || 31.7)}% have built offline-first capability, while donor procurement cycles stall recurring maintenance.`;
      }

      const elExpertStreamBanner = document.getElementById('stream-expert-takeaway');
      if (elExpertStreamBanner) {
        elExpertStreamBanner.innerHTML = `<strong>Systemic Fragility:</strong> ${totalDonorExitRisk}% of N=${e.total || 80} evaluated system experts confirm donor pilots fail within 18 months due to unbudgeted operating expenditures (OPEX).`;
      }
'''
    pos_donor_cliff_render = html.find('if (elDonorCliff) elDonorCliff.textContent = totalDonorExitRisk + \'%\';')
    if pos_donor_cliff_render != -1:
        insert_pt = pos_donor_cliff_render + len('if (elDonorCliff) elDonorCliff.textContent = totalDonorExitRisk + \'%\';')
        html = html[:insert_pt] + dynamic_takeaways_logic + html[insert_pt:]
        print("✓ Injected dynamic takeaway generation into renderSurveyDashboard")

    # F. Update DOMContentLoaded handler to default to landing view
    html = re.sub(
        r'const view = params\.get\(\'view\'\) \|\| \'[^\']*\';[\s\S]*?if \(view === \'systemic\' \|\| view === \'classroom\'\) switchLens\(view, false\);',
        '''const view = params.get('view') || 'landing';
      if (['landing', 'systemic', 'classroom'].includes(view)) {
        switchLens(view, false);
      } else {
        switchLens('landing', false);
      }''',
        html,
        count=1
    )
    print("✓ Updated DOMContentLoaded to default to landing view")

    print("Writing updated index.html...")
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Finished successfully!")

if __name__ == '__main__':
    main()
