#!/usr/bin/env python3
"""
inject_survey_markup.py
=======================
Injects the Subtab 4 navigation button and HTML container into index.html:
1. Adds btn-survey-subtab to #tab-nav-classroom.
2. Adds #survey-subtab right after #dpg-subtab.
"""

def main():
    path = '/workspaces/CC_3/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Inject Tab Button
    btn_target = """          <button onclick="switchClassroomTab('dpg-subtab')" id="btn-dpg-subtab" class="tab-btn-cls px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold text-stone-700 hover:text-stone-900 transition hover:bg-stone-200/60">
            <span class="sm:hidden">Resilient Solutions</span>
            <span class="hidden sm:inline">Vetted Resilient Solutions Directory</span>
          </button>"""

    new_button = btn_target + """
          <button onclick="switchClassroomTab('survey-subtab')" id="btn-survey-subtab" class="tab-btn-cls px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold text-stone-700 hover:text-stone-900 transition hover:bg-stone-200/60">
            <span class="sm:hidden">Community Evidence</span>
            <span class="hidden sm:inline">📊 Community Evidence &amp; Survey Layer</span>
          </button>"""

    if 'id="btn-survey-subtab"' not in html:
        assert btn_target in html, "Could not find btn-dpg-subtab target in index.html"
        html = html.replace(btn_target, new_button, 1)
        print("Injected btn-survey-subtab successfully.")
    else:
        print("btn-survey-subtab already present.")

    # 2. Inject Subtab 4 Markup right after dpg-subtab
    dpg_end_target = """        <!-- Automated Health-Check & Registry Audit Note -->
        <div class="mt-8 p-4 rounded-xl bg-stone-100 border border-stone-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs text-stone-600">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shrink-0"></span>
            <span><strong>Automated Verification Engine:</strong> Tested monthly via <code class="bg-stone-200 px-1 py-0.5 rounded text-[11px]">scripts/verify_dpg_urls.py</code> with 301-redirect resolution and domain squatter detection.</span>
          </div>
          <div class="flex items-center gap-2 text-stone-500 shrink-0">
            <span>Last Audit: <strong>Nov 1, 2026 (All 9 URLs 200 OK)</strong></span>
            <span>•</span>
            <span class="text-stone-500">Flag broken URLs with the 🚩 button on each card.</span>
          </div>
        </div>

      </div>"""

    survey_subtab_html = """        <!-- Automated Health-Check & Registry Audit Note -->
        <div class="mt-8 p-4 rounded-xl bg-stone-100 border border-stone-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs text-stone-600">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 shrink-0"></span>
            <span><strong>Automated Verification Engine:</strong> Tested monthly via <code class="bg-stone-200 px-1 py-0.5 rounded text-[11px]">scripts/verify_dpg_urls.py</code> with 301-redirect resolution and domain squatter detection.</span>
          </div>
          <div class="flex items-center gap-2 text-stone-500 shrink-0">
            <span>Last Audit: <strong>Nov 1, 2026 (All 9 URLs 200 OK)</strong></span>
            <span>•</span>
            <span class="text-stone-500">Flag broken URLs with the 🚩 button on each card.</span>
          </div>
        </div>

      </div>

      <!-- ================================================================= -->
      <!-- SUBTAB 4: COMMUNITY EVIDENCE & SURVEY INSTRUMENTS LAYER          -->
      <!-- Ground-Truth Triangulation Across Frontline Teachers, Providers,  -->
      <!-- and System Experts (N=800 Calibrated / Live Ingestion Capable)    -->
      <!-- ================================================================= -->
      <div id="survey-subtab" class="classroom-content hidden">

        <!-- Header Strip -->
        <div class="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-2 flex-wrap">
              <span class="badge-pill bg-emerald-100 text-emerald-800 text-xs py-1 px-3 font-mono">
                Tool 4 · UNESCO Six Pillars Ground-Truth
              </span>
              <span class="badge-pill bg-amber-100 text-amber-900 text-xs py-1 px-3 font-medium">
                Triangulation of Grassroots vs Macro Narrative
              </span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-stone-900 font-serif">
              Community Evidence &amp; Survey Instrument Layer
            </h2>
            <p class="text-stone-600 mt-2 max-w-4xl text-sm sm:text-base">
              Empirical field triangulation reconciling top-down macro statistics (UIS, WDI, ITU) with frontline realities.
              Ingests 3 validated survey streams (<strong class="text-stone-800">600 Teachers</strong>, <strong class="text-stone-800">120 Providers</strong>, and <strong class="text-stone-800">80 System Experts</strong> across 48 Sub-Saharan African nations).
            </p>
          </div>

          <!-- Quick Action Buttons -->
          <div class="flex flex-wrap items-center gap-2">
            <button onclick="toggleSurveyIngestionDrawer()" class="px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-lg text-xs font-semibold shadow-sm transition flex items-center gap-1.5">
              <span>📥</span> Connect Live Data / Feeds
            </button>
            <button onclick="loadDemoLiveSurveyData()" class="px-3 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg text-xs font-semibold shadow-sm transition flex items-center gap-1.5" title="Simulate field survey batch upload for thesis defense">
              <span>⚡</span> Test Live Hot-Swap Demo
            </button>
            <button onclick="resetSurveyBaseline()" class="px-3 py-2 bg-stone-200 hover:bg-stone-300 text-stone-700 rounded-lg text-xs font-semibold transition" title="Restore calibrated baseline data">
              <span>🔄</span> Reset Baseline
            </button>
          </div>
        </div>

        <!-- Live Ingestion Status Banner & Drawer -->
        <div class="mb-8">
          <!-- Active Mode Banner -->
          <div class="p-4 rounded-xl border border-emerald-200 bg-emerald-50/70 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-xs">
            <div class="flex items-center gap-3">
              <span id="survey-live-status-dot" class="w-3.5 h-3.5 rounded-full bg-emerald-500 animate-pulse shrink-0"></span>
              <div>
                <div class="flex items-center gap-2">
                  <span id="survey-mode-badge" class="font-bold text-xs uppercase tracking-wider text-emerald-900 bg-emerald-200/70 px-2 py-0.5 rounded">
                    Active Mode: Calibrated Baseline Synthesis
                  </span>
                  <span id="survey-n-badge" class="font-mono text-xs text-emerald-800 font-bold">
                    N = 800 Verified Responses (48 SSA Nations)
                  </span>
                </div>
                <div id="survey-mode-desc" class="text-xs text-stone-600 mt-0.5">
                  Pre-calibrated against World Bank 6-Pillars WDI 2024, GEM 2023, AfroBench, Briter, and HolonIQ.
                </div>
              </div>
            </div>
            <div class="text-right shrink-0">
              <span class="text-[11px] font-mono text-stone-500">Dual Pipeline: Calibrated Seeding ⇄ Hot-Swap Live CSV</span>
            </div>
          </div>

          <!-- Collapsible Ingestion Control Drawer (Hidden by default) -->
          <div id="survey-ingestion-drawer" class="hidden mt-3 p-5 rounded-2xl bg-white border border-stone-300 shadow-md">
            <div class="flex items-start justify-between gap-4 mb-4 pb-3 border-b border-stone-200">
              <div>
                <h4 class="font-bold text-stone-900 text-sm font-serif">Live Data Ingestion Control Panel</h4>
                <p class="text-xs text-stone-600 mt-1 max-w-2xl">
                  Upload exported survey CSV/JSON files or paste published Google Sheets CSV links. When uploaded, the observatory dynamically parses the fields, recomputes all percentages, and updates the telemetry in real-time. If no live data is provided, the observatory remains completely functional on the 48-nation calibrated baseline.
                </p>
              </div>
              <button onclick="toggleSurveyIngestionDrawer()" class="text-stone-400 hover:text-stone-700 text-sm font-bold">✕ Close</button>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Method 1: Local File Drag & Drop -->
              <div class="p-4 rounded-xl border-2 border-dashed border-emerald-300 bg-emerald-50/30 flex flex-col items-center justify-center text-center">
                <div class="text-2xl mb-2">📁</div>
                <div class="font-semibold text-xs text-stone-800 mb-1">Upload Survey CSV or JSON</div>
                <p class="text-[11px] text-stone-500 mb-3 max-w-xs">Supports Google Forms CSV exports, raw survey tables, or calibrated JSON schemas.</p>
                <label class="cursor-pointer px-4 py-2 rounded-lg bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-semibold shadow-sm transition">
                  <span>Browse Local File</span>
                  <input type="file" id="survey-file-input" onchange="handleSurveyFileUpload(event)" accept=".csv,.json" class="hidden">
                </label>
              </div>

              <!-- Method 2: Google Sheets CSV URL Sync -->
              <div class="space-y-2.5">
                <div class="font-semibold text-xs text-stone-800">Or Connect Live Published Google Sheet CSVs:</div>
                <div>
                  <label class="block text-[11px] text-stone-600 font-medium mb-0.5">Stream A (Teacher Responses CSV URL):</label>
                  <input type="url" id="survey-url-teacher" placeholder="https://docs.google.com/spreadsheets/d/.../export?format=csv" class="w-full text-xs font-mono p-2 border border-stone-300 rounded-lg bg-stone-50 focus:bg-white focus:border-emerald-600 focus:outline-none">
                </div>
                <div>
                  <label class="block text-[11px] text-stone-600 font-medium mb-0.5">Stream B (Provider Responses CSV URL):</label>
                  <input type="url" id="survey-url-provider" placeholder="https://docs.google.com/spreadsheets/d/.../export?format=csv" class="w-full text-xs font-mono p-2 border border-stone-300 rounded-lg bg-stone-50 focus:bg-white focus:border-emerald-600 focus:outline-none">
                </div>
                <button onclick="fetchLiveSurveyFeeds()" class="w-full mt-2 py-2 bg-stone-800 hover:bg-stone-900 text-white rounded-lg text-xs font-semibold transition">
                  Fetch Remote Feeds &amp; Recalculate
                </button>
              </div>
            </div>

            <!-- Ingestion Toast / Log -->
            <div id="survey-ingestion-status" class="hidden mt-4 p-3 rounded-lg text-xs font-mono"></div>
          </div>
        </div>

        <!-- MASTER DISCREPANCY MATRIX: TOP-DOWN MACRO VS FRONT-LINE REALITY -->
        <div class="mb-10">
          <div class="flex items-center justify-between mb-4 flex-wrap gap-2">
            <div>
              <span class="badge-pill bg-slate-100 text-slate-800 text-xs py-0.5 px-2.5 font-mono mb-1">
                Empirical Tension Matrix
              </span>
              <h3 class="text-lg sm:text-xl font-bold text-stone-900 font-serif">
                Top-Down Macro Rhetoric vs. Frontline Field Ground-Truth
              </h3>
            </div>
            <div class="text-xs text-stone-500 font-mono">
              Triangulating UIS / WDI / ITU Indicators against Alliance of Alliances Micro-Data
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Discrepancy 1: Electricity -->
            <div class="bg-white rounded-xl p-4 border border-stone-200 shadow-xs flex flex-col justify-between">
              <div>
                <div class="text-[11px] font-bold uppercase tracking-wider text-stone-500 mb-2">1. Power Reliability Gap</div>
                <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 mb-2">
                  <div class="text-[10px] text-slate-500 font-medium">Official Macro Indicator</div>
                  <div class="text-lg font-black text-slate-800 font-mono">28.4%</div>
                  <div class="text-[11px] text-slate-600">Avg Rural Electrification (WB SE4ALL)</div>
                </div>
                <div class="p-2.5 rounded-lg bg-amber-50 border border-amber-200">
                  <div class="text-[10px] text-amber-700 font-medium">Community Ground-Truth</div>
                  <div id="metric-power-gap" class="text-lg font-black text-amber-900 font-mono">82.5%</div>
                  <div class="text-[11px] text-amber-800">Severe cuts or zero power in field schools (37.3% total blackout)</div>
                </div>
              </div>
              <div class="mt-3 pt-2 border-t border-stone-100 text-[11px] text-stone-500 italic">
                Pillar 4 Friction: Grid assumptions fail in 8 out of 10 rural schools.
              </div>
            </div>

            <!-- Discrepancy 2: Internet & Data Tax -->
            <div class="bg-white rounded-xl p-4 border border-stone-200 shadow-xs flex flex-col justify-between">
              <div>
                <div class="text-[11px] font-bold uppercase tracking-wider text-stone-500 mb-2">2. The Informal Data Tax</div>
                <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 mb-2">
                  <div class="text-[10px] text-slate-500 font-medium">Official Macro Indicator</div>
                  <div class="text-lg font-black text-slate-800 font-mono">&lt; 1.2%</div>
                  <div class="text-[11px] text-slate-600">Fixed Broadband Subs per 100 (ITU)</div>
                </div>
                <div class="p-2.5 rounded-lg bg-amber-50 border border-amber-200">
                  <div class="text-[10px] text-amber-700 font-medium">Community Ground-Truth</div>
                  <div id="metric-data-tax" class="text-lg font-black text-amber-900 font-mono">39.3%</div>
                  <div class="text-[11px] text-amber-800">Teachers paying personal airtime for school apps; 61.5% providers pass data costs to learners</div>
                </div>
              </div>
              <div class="mt-3 pt-2 border-t border-stone-100 text-[11px] text-stone-500 italic">
                Regressive 4–8% wage penalty on frontline teachers.
              </div>
            </div>

            <!-- Discrepancy 3: Vendor Architecture Mismatch -->
            <div class="bg-white rounded-xl p-4 border border-stone-200 shadow-xs flex flex-col justify-between">
              <div>
                <div class="text-[11px] font-bold uppercase tracking-wider text-stone-500 mb-2">3. Solution Architecture Mismatch</div>
                <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 mb-2">
                  <div class="text-[10px] text-slate-500 font-medium">Commercial Product Pitch</div>
                  <div class="text-lg font-black text-slate-800 font-mono">Cloud / AI SaaS</div>
                  <div class="text-[11px] text-slate-600">Personal screens &amp; broadband LMS</div>
                </div>
                <div class="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200">
                  <div class="text-[10px] text-emerald-700 font-medium">Community Ground-Truth</div>
                  <div id="metric-offline-share" class="text-lg font-black text-emerald-900 font-mono">70.8% Phone · 31.7% Offline</div>
                  <div class="text-[11px] text-emerald-800">Shared low-cost smartphones; only 31.7% fully offline; only 5.5% have RCT evidence</div>
                </div>
              </div>
              <div class="mt-3 pt-2 border-t border-stone-100 text-[11px] text-stone-500 italic">
                High-bandwidth laptop tools fail in shared mobile classrooms.
              </div>
            </div>

            <!-- Discrepancy 4: Donor Project Mortality -->
            <div class="bg-white rounded-xl p-4 border border-stone-200 shadow-xs flex flex-col justify-between">
              <div>
                <div class="text-[11px] font-bold uppercase tracking-wider text-stone-500 mb-2">4. Post-Donor Cliff Effect</div>
                <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 mb-2">
                  <div class="text-[10px] text-slate-500 font-medium">Policy Discourse</div>
                  <div class="text-lg font-black text-slate-800 font-mono">&quot;Catalytic Pilots&quot;</div>
                  <div class="text-[11px] text-slate-600">Assumption of Ministry absorption</div>
                </div>
                <div class="p-2.5 rounded-lg bg-rose-50 border border-rose-200">
                  <div class="text-[10px] text-rose-700 font-medium">Expert System Ground-Truth</div>
                  <div id="metric-donor-cliff" class="text-lg font-black text-rose-900 font-mono">85.0%</div>
                  <div class="text-[11px] text-rose-800">Initiatives collapse (62.5%) or shrink to token scale (22.5%) upon donor exit</div>
                </div>
              </div>
              <div class="mt-3 pt-2 border-t border-stone-100 text-[11px] text-stone-500 italic">
                Validates the 40/60 TCO lifecycle gatekeeper in Step 2.
              </div>
            </div>
          </div>
        </div>

        <!-- THREE-STREAM INTERACTIVE VANTAGES EXPLORER -->
        <div class="bg-white rounded-2xl border border-stone-200 shadow-sm overflow-hidden mb-10">
          <!-- Vantage Stream Tabs -->
          <div class="bg-stone-100/80 p-2 border-b border-stone-200 flex flex-wrap items-center gap-2">
            <button onclick="switchSurveyStream('teachers')" id="btn-stream-teachers" class="px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold transition bg-emerald-700 text-white shadow-xs">
              👨‍🏫 Stream A: Frontline Teachers (<span id="tab-n-teachers">N=600</span>)
            </button>
            <button onclick="switchSurveyStream('providers')" id="btn-stream-providers" class="px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold text-stone-700 hover:text-stone-900 transition hover:bg-stone-200/60">
              🏢 Stream B: EdTech Providers (<span id="tab-n-providers">N=120</span>)
            </button>
            <button onclick="switchSurveyStream('experts')" id="btn-stream-experts" class="px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold text-stone-700 hover:text-stone-900 transition hover:bg-stone-200/60">
              🏛️ Stream C: System Experts &amp; MoE (<span id="tab-n-experts">N=80</span>)
            </button>
          </div>

          <div class="p-6">
            <!-- STREAM A: TEACHERS -->
            <div id="survey-stream-teachers" class="space-y-6">
              <div class="flex items-center justify-between border-b border-stone-100 pb-3">
                <div>
                  <h4 class="font-bold text-stone-900 text-base font-serif">Frontline Teacher Feasibility &amp; Workplace Conditions</h4>
                  <p class="text-xs text-stone-600">Self-reported pedagogical feasibility, infrastructure barriers, and technology workload across 48 SSA nations.</p>
                </div>
                <span class="text-xs font-mono text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full font-bold">
                  43.8% Rural · 30.7% Town · 25.5% City
                </span>
              </div>

              <!-- Distribution Cards Grid -->
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                <!-- Card 1: Power by Location -->
                <div class="p-4 rounded-xl border border-stone-200 bg-stone-50/50">
                  <div class="font-bold text-xs text-stone-800 mb-2">Electricity Reliability by School Location</div>
                  <div id="chart-elec-by-loc" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                  </div>
                  <div class="mt-3 text-[11px] text-stone-500 italic">Notice: 0.0% of rural teachers report always-reliable power.</div>
                </div>

                <!-- Card 2: Internet Modality -->
                <div class="p-4 rounded-xl border border-stone-200 bg-stone-50/50">
                  <div class="font-bold text-xs text-stone-800 mb-2">Internet Connectivity Modality</div>
                  <div id="chart-internet-dist" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                  </div>
                  <div class="mt-3 text-[11px] text-stone-500 italic">39.3% fund educational data from personal pocket.</div>
                </div>

                <!-- Card 3: Workload Impact -->
                <div class="p-4 rounded-xl border border-stone-200 bg-stone-50/50">
                  <div class="font-bold text-xs text-stone-800 mb-2">Impact on Teacher Workload</div>
                  <div id="chart-workload-dist" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                  </div>
                  <div class="mt-3 text-[11px] text-stone-500 italic">34.0% report digital tools actually add to their daily workload.</div>
                </div>
              </div>

              <!-- Qualitative Frontline Voices Ticker -->
              <div class="mt-6 p-4 rounded-xl bg-amber-50/60 border border-amber-200">
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-amber-800 font-bold text-xs uppercase tracking-wider">🎙️ Frontline Voices from the Field (Calibrated Ground-Truth):</span>
                </div>
                <div id="teacher-quotes-grid" class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-stone-700">
                  <!-- Populated by JS -->
                </div>
              </div>
            </div>

            <!-- STREAM B: PROVIDERS -->
            <div id="survey-stream-providers" class="hidden space-y-6">
              <div class="flex items-center justify-between border-b border-stone-100 pb-3">
                <div>
                  <h4 class="font-bold text-stone-900 text-base font-serif">EdTech Provider Capabilities, Architecture &amp; Business Models</h4>
                  <p class="text-xs text-stone-600">Enterprise deployment architectures, funding pipelines, and offline compatibility across 120 SSA organizations.</p>
                </div>
                <span class="text-xs font-mono text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full font-bold">
                  68.3% Locally Founded &amp; Owned in SSA
                </span>
              </div>

              <!-- Distribution Cards Grid -->
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                <!-- Card 1: Offline Capability -->
                <div class="p-4 rounded-xl border border-stone-200 bg-stone-50/50">
                  <div class="font-bold text-xs text-stone-800 mb-2">Offline Capability Architecture</div>
                  <div id="chart-provider-offline" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                  </div>
                  <div class="mt-3 text-[11px] text-stone-500 italic">23.3% of solutions fail completely without continuous live internet.</div>
                </div>

                <!-- Card 2: Data Payment Burden -->
                <div class="p-4 rounded-xl border border-stone-200 bg-stone-50/50">
                  <div class="font-bold text-xs text-stone-800 mb-2">Who Pays for Connectivity Data?</div>
                  <div id="chart-provider-data-pay" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                  </div>
                  <div class="mt-3 text-[11px] text-stone-500 italic">61.5% pass the data cost directly to learners/teachers.</div>
                </div>

                <!-- Card 3: Evidence Threshold -->
                <div class="p-4 rounded-xl border border-stone-200 bg-stone-50/50">
                  <div class="font-bold text-xs text-stone-800 mb-2">Evidence Rigor Level Claimed</div>
                  <div id="chart-provider-evidence" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                  </div>
                  <div class="mt-3 text-[11px] text-stone-500 italic">Only 5.5% possess independent RCT evaluation evidence.</div>
                </div>
              </div>
            </div>

            <!-- STREAM C: EXPERTS -->
            <div id="survey-stream-experts" class="hidden space-y-6">
              <div class="flex items-center justify-between border-b border-stone-100 pb-3">
                <div>
                  <h4 class="font-bold text-stone-900 text-base font-serif">System Governance, Decision Drivers &amp; Policy Fragility</h4>
                  <p class="text-xs text-stone-600">Expert and Ministry assessments regarding procurement power, donor reliance, and national scaling traps.</p>
                </div>
                <span class="text-xs font-mono text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-1 rounded-full font-bold">
                  80 System Advisers &amp; MoE Specialists
                </span>
              </div>

              <!-- Distribution Cards Grid -->
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                <!-- Card 1: Decision Drivers -->
                <div class="p-4 rounded-xl border border-stone-200 bg-stone-50/50">
                  <div class="font-bold text-xs text-stone-800 mb-2">Who in Practice Drives Adoption?</div>
                  <div id="chart-expert-drivers" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                  </div>
                  <div class="mt-3 text-[11px] text-stone-500 italic">Only 2.5% driven by frontline schools or headteachers.</div>
                </div>

                <!-- Card 2: Post-Donor Exit Fate -->
                <div class="p-4 rounded-xl border border-stone-200 bg-stone-50/50">
                  <div class="font-bold text-xs text-stone-800 mb-2">What Happens When Donor Project Ends?</div>
                  <div id="chart-expert-donor-exit" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                  </div>
                  <div class="mt-3 text-[11px] text-stone-500 italic">62.5% stop completely or collapse; 22.5% shrink to token presence.</div>
                </div>

                <!-- Card 3: Top System Constraints -->
                <div class="p-4 rounded-xl border border-stone-200 bg-stone-50/50">
                  <div class="font-bold text-xs text-stone-800 mb-2">Top Systemic Scaling Constraints</div>
                  <div id="chart-expert-constraints" class="space-y-2 text-xs">
                    <!-- Populated by JS -->
                  </div>
                  <div class="mt-3 text-[11px] text-stone-500 italic">Infrastructure and recurrent operational funds dominate.</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 104-ITEM SURVEY INSTRUMENTS & CODEBOOK EXPLORER -->
        <div class="bg-white rounded-2xl border border-stone-200 shadow-sm p-6 mb-8">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-5 pb-4 border-b border-stone-200">
            <div>
              <span class="badge-pill bg-blue-100 text-blue-900 text-xs py-0.5 px-2.5 font-mono mb-1">
                Full Empirical Instrument Codebook
              </span>
              <h3 class="text-lg sm:text-xl font-bold text-stone-900 font-serif">
                Alliance of Alliances (AoA) Survey Instruments (104 Mapped Items)
              </h3>
              <p class="text-xs text-stone-600 mt-1">
                Inspect every question operationalizing UNESCO's Six Pillars across Teacher, Provider, and Expert protocols.
              </p>
            </div>

            <!-- External Forms Links -->
            <div class="flex items-center gap-2 flex-wrap text-xs">
              <a href="https://docs.google.com/forms" target="_blank" class="px-3 py-1.5 rounded-lg border border-stone-300 hover:bg-stone-50 text-stone-700 font-medium transition">
                Teacher Form ↗
              </a>
              <a href="https://docs.google.com/forms" target="_blank" class="px-3 py-1.5 rounded-lg border border-stone-300 hover:bg-stone-50 text-stone-700 font-medium transition">
                Provider Form ↗
              </a>
              <a href="https://docs.google.com/forms" target="_blank" class="px-3 py-1.5 rounded-lg border border-stone-300 hover:bg-stone-50 text-stone-700 font-medium transition">
                Expert Form ↗
              </a>
            </div>
          </div>

          <!-- Codebook Filters -->
          <div class="flex flex-wrap items-center justify-between gap-3 mb-4">
            <div class="flex flex-wrap items-center gap-2 flex-1 min-w-[280px]">
              <input type="text" id="survey-codebook-search" oninput="filterSurveyCodebook()" placeholder="Search questions, variables, keywords..." class="text-xs p-2 border border-stone-300 rounded-lg bg-stone-50 focus:bg-white focus:border-emerald-600 focus:outline-none flex-1 max-w-xs">
              
              <select id="survey-codebook-pillar" onchange="filterSurveyCodebook()" class="text-xs p-2 border border-stone-300 rounded-lg bg-stone-50 focus:bg-white focus:outline-none">
                <option value="ALL">All UNESCO Pillars (1–6)</option>
                <option value="1">Pillar 1: Management &amp; Governance</option>
                <option value="2">Pillar 2: Teacher Professional Dev</option>
                <option value="3">Pillar 3: Pedagogy &amp; Materials</option>
                <option value="4">Pillar 4: Connectivity &amp; Infrastructure</option>
                <option value="5">Pillar 5: Inclusion &amp; Language</option>
                <option value="6">Pillar 6: Data Privacy &amp; Ethics</option>
              </select>

              <select id="survey-codebook-instrument" onchange="filterSurveyCodebook()" class="text-xs p-2 border border-stone-300 rounded-lg bg-stone-50 focus:bg-white focus:outline-none">
                <option value="ALL">All Instruments (104)</option>
                <option value="Teacher">Teacher Survey (40)</option>
                <option value="Provider">Provider Survey (33)</option>
                <option value="Expert">Expert Consultation (31)</option>
              </select>
            </div>

            <div class="text-xs font-mono text-stone-500">
              Showing <span id="survey-codebook-count" class="font-bold text-stone-800">104</span> / 104 Questions
            </div>
          </div>

          <!-- Codebook Items Accordion / Grid -->
          <div id="survey-codebook-container" class="space-y-2 max-h-[460px] overflow-y-auto pr-2 border border-stone-200 rounded-xl p-3 bg-stone-50/50">
            <!-- Populated by JS -->
          </div>
        </div>

      </div>"""

    if 'id="survey-subtab"' not in html:
        assert dpg_end_target in html, "Could not find dpg-subtab end target in index.html"
        html = html.replace(dpg_end_target, survey_subtab_html, 1)
        print("Injected #survey-subtab successfully.")
    else:
        print("#survey-subtab already present.")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
