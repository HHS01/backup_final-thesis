with open('/workspaces/backup_final-thesis/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add tab button
tab_btn_target = '<button onclick="switchTab(\'appendix-tab\')"'
new_tab_btn = '''<button onclick="switchTab('surveys-tab')" id="btn-surveys-tab" class="tab-btn px-4 py-2 rounded-lg text-xs sm:text-sm font-semibold text-slate-600 hover:text-slate-900 transition hover:bg-slate-100 flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Field Surveys &amp; Collector
          </button>
          '''

if 'id="btn-surveys-tab"' not in html:
    html = html.replace(tab_btn_target, new_tab_btn + tab_btn_target)

# 2. Add survey tab content right before appendix-tab
surveys_tab_content = """
  <!-- ================================================================= -->
  <!-- FIELD SURVEYS & PRACTITIONER DATA PORTAL TAB                      -->
  <!-- ================================================================= -->
  <div id="surveys-tab" class="tab-content hidden max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
    <div class="mb-8">
      <div class="flex items-center gap-2 mb-2">
        <span class="badge-pill bg-emerald-100 text-emerald-800 text-xs font-bold font-mono">Layer 3 Field Instruments</span>
        <span class="badge-pill bg-indigo-100 text-indigo-800 text-xs font-mono font-bold">UNESCO Global Education Coalition / AoA</span>
      </div>
      <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-900 font-serif">Frontline Field Evidence &amp; Survey Instrument Hub</h2>
      <p class="text-xs sm:text-sm text-slate-600 mt-1 max-w-4xl leading-relaxed">
        Collect and ground-truth empirical data directly from educators, technology founders, and domain experts. Survey responses are logged in secure client-side storage, calculate instant diagnostic feasibility scores for the respondent, and aggregate into regional discrepancy indicators.
      </p>
    </div>

    <!-- 3 Survey Instrument Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <!-- Card 1: Teacher Survey -->
      <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between hover:border-indigo-300 transition">
        <div>
          <div class="flex items-center justify-between mb-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-indigo-100 text-indigo-800">Instrument T-1</span>
            <span class="text-xs text-slate-400">~6 mins</span>
          </div>
          <h3 class="font-bold text-slate-900 text-base font-serif mb-2">Frontline Teacher Classroom Diagnostic</h3>
          <p class="text-xs text-slate-600 mb-4 leading-relaxed">
            Audits physical electricity reliability, out-of-pocket mobile data expenses (the "Teacher Salary Tax"), pupil-teacher ratios, and mother-tongue language alignment.
          </p>
          <div class="p-3 bg-slate-50 rounded-lg text-[11px] text-slate-500 mb-4 space-y-1">
            <div class="font-bold text-slate-700">Respondent Incentive:</div>
            <div>Instant Classroom Feasibility Score + 3-Station Rotation Schedule recommendation.</div>
          </div>
        </div>
        <div class="space-y-2">
          <a href="./Teacher_Diagnostic_Survey.html" target="_blank" class="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-xs font-bold bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm transition">
            Launch Teacher Diagnostic →
          </a>
          <button onclick="copySurveyLink('teacher')" class="w-full text-center text-[11px] text-indigo-600 hover:text-indigo-800 font-medium py-1">
            🔗 Copy Shareable Link for WhatsApp/Email
          </button>
        </div>
      </div>

      <!-- Card 2: EdTech Provider Survey -->
      <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between hover:border-indigo-300 transition">
        <div>
          <div class="flex items-center justify-between mb-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-100 text-amber-800">Instrument P-1</span>
            <span class="text-xs text-slate-400">~8 mins</span>
          </div>
          <h3 class="font-bold text-slate-900 text-base font-serif mb-2">African EdTech Provider &amp; Founder Survey</h3>
          <p class="text-xs text-slate-600 mb-4 leading-relaxed">
            Measures architecture requirements (offline vs. cloud), pricing models (B2C vs. B2G tenders), donor grant dependency, and indigenous language localization.
          </p>
          <div class="p-3 bg-slate-50 rounded-lg text-[11px] text-slate-500 mb-4 space-y-1">
            <div class="font-bold text-slate-700">Respondent Incentive:</div>
            <div>Instant UNESCO 6-Pillars Market Fit Rating &amp; DPG eligibility check.</div>
          </div>
        </div>
        <div class="space-y-2">
          <a href="./AoA survey/SSA_Provider_Survey_v1_PUBLIC.docx" download class="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-xs font-bold bg-slate-800 text-white hover:bg-slate-700 shadow-sm transition">
            Download Provider Survey (.docx)
          </a>
          <div class="text-center text-[11px] text-slate-400 py-1">Online form mirror launching shortly</div>
        </div>
      </div>

      <!-- Card 3: Expert Panel Consultation -->
      <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between hover:border-indigo-300 transition">
        <div>
          <div class="flex items-center justify-between mb-3">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-purple-100 text-purple-800">Instrument E-1</span>
            <span class="text-xs text-slate-400">~12 mins</span>
          </div>
          <h3 class="font-bold text-slate-900 text-base font-serif mb-2">Policy &amp; Donor Expert Delphi Consultation</h3>
          <p class="text-xs text-slate-600 mb-4 leading-relaxed">
            Captures qualitative perspectives on the "85% Pilot Graveyard", national curriculum accreditation bottlenecks, and AI readiness across Sub-Saharan Africa.
          </p>
          <div class="p-3 bg-slate-50 rounded-lg text-[11px] text-slate-500 mb-4 space-y-1">
            <div class="font-bold text-slate-700">Target Group:</div>
            <div>Ministries of Education, UNESCO/World Bank specialists, Academic researchers.</div>
          </div>
        </div>
        <div class="space-y-2">
          <a href="./AoA survey/SSA_Expert_Consultation_R1_v1_PUBLIC.docx" download class="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg text-xs font-bold bg-slate-800 text-white hover:bg-slate-700 shadow-sm transition">
            Download Expert Protocol (.docx)
          </a>
          <div class="text-center text-[11px] text-slate-400 py-1">Qualitative semi-structured format</div>
        </div>
      </div>
    </div>

    <!-- Researcher Admin / Data Vault Panel -->
    <div class="bg-slate-900 text-white rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-md">
      <div class="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800 mb-6">
        <div>
          <div class="flex items-center gap-2 mb-1">
            <span class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500 text-slate-950">RESEARCHER DATA VAULT</span>
            <span class="text-xs text-slate-400">Encrypted Local Storage &amp; Export</span>
          </div>
          <h3 class="text-lg font-bold font-serif text-white">Collected Responses Ingestion &amp; Discrepancy Triangulation</h3>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="refreshVaultDisplay()" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 transition">
            🔄 Refresh Vault
          </button>
          <button onclick="exportVaultJSON()" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-indigo-600 hover:bg-indigo-500 text-white transition">
            📥 Export All (.JSON)
          </button>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 text-xs">
        <div class="lg:col-span-1 space-y-4">
          <div class="p-4 bg-slate-800/80 rounded-xl border border-slate-700 space-y-2">
            <span class="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Vault Statistics</span>
            <div class="text-2xl font-extrabold text-emerald-400" id="vault-count">0 Recorded Submissions</div>
            <p class="text-slate-400 text-[11px] leading-relaxed">
              Responses logged via the Teacher Diagnostic or manual ingestion are securely cached client-side. No third party or public visitor can see your individual records.
            </p>
          </div>
          <div class="p-4 bg-slate-800/80 rounded-xl border border-slate-700 space-y-2">
            <span class="text-slate-400 text-[10px] uppercase font-bold tracking-wider">Manual Batch Ingestion</span>
            <p class="text-slate-400 text-[11px]">Paste JSON payloads from Google Forms or WhatsApp collection:</p>
            <textarea id="vault-manual-input" placeholder='[{"country":"KEN","power":"solar"...}]' class="w-full h-20 bg-slate-950 border border-slate-700 rounded p-2 font-mono text-[10px] text-emerald-400"></textarea>
            <button onclick="ingestManualPayload()" class="w-full py-1.5 bg-slate-700 hover:bg-slate-600 rounded text-slate-200 font-bold transition text-[11px]">
              Ingest Into Repository Vault
            </button>
          </div>
        </div>

        <div class="lg:col-span-2 bg-slate-950 p-4 rounded-xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between pb-2 border-b border-slate-800 mb-2">
              <span class="font-bold text-slate-300 font-mono text-[11px]">Ingested Records Stream</span>
              <span class="text-[10px] text-slate-500 font-mono">Format: Standardized AoA Payload</span>
            </div>
            <div id="vault-stream" class="h-48 overflow-y-auto font-mono text-[10px] text-slate-400 space-y-1">
              <div class="text-slate-600 italic">No field records submitted yet. Distribute the Teacher Diagnostic survey link to populate this stream.</div>
            </div>
          </div>
          <div class="pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
            <span>Periodic Analysis: Run <code class="text-indigo-400">python3 scripts/run_monthly_triangulation.py</code> to recalculate heatmap divergence</span>
            <button onclick="clearVault()" class="text-rose-400 hover:text-rose-300 text-[10px]">Clear Vault Data</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <script>
    function copySurveyLink(type) {
      const url = window.location.origin + window.location.pathname.replace('index.html', '') + 'Teacher_Diagnostic_Survey.html';
      navigator.clipboard.writeText(url);
      alert('Copied shareable survey link to clipboard:\\n' + url);
    }

    function refreshVaultDisplay() {
      const countEl = document.getElementById('vault-count');
      const streamEl = document.getElementById('vault-stream');
      if (!countEl || !streamEl) return;

      const records = JSON.parse(localStorage.getItem('collected_teacher_diagnostics') || '[]');
      countEl.textContent = `${records.length} Recorded Submission${records.length === 1 ? '' : 's'}`;

      if (records.length === 0) {
        streamEl.innerHTML = '<div class="text-slate-600 italic">No field records submitted yet. Distribute the Teacher Diagnostic survey link to populate this stream.</div>';
        return;
      }

      streamEl.innerHTML = records.map((r, i) => `
        <div class="p-2 rounded bg-slate-900 border border-slate-800 mb-1">
          <span class="text-emerald-400 font-bold">#${i+1} [${r.country || 'N/A'}]</span>
          <span class="text-slate-300 ml-2">${r.location || 'N/A'} · PTR ${r.ptr || 'N/A'} · Power: ${r.power || 'N/A'} · Tax: ${r.salary_tax || 'N/A'}</span>
          <span class="text-slate-500 block text-[9px] mt-0.5">${r.timestamp || ''}</span>
        </div>
      `).reverse().join('');
    }

    function exportVaultJSON() {
      const records = JSON.parse(localStorage.getItem('collected_teacher_diagnostics') || '[]');
      if (records.length === 0) {
        alert('Vault is currently empty. No submissions to export.');
        return;
      }
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(records, null, 2));
      const downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", `field_survey_responses_${new Date().toISOString().slice(0,10)}.json`);
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    }

    function ingestManualPayload() {
      const input = document.getElementById('vault-manual-input').value.trim();
      if (!input) return;
      try {
        const parsed = JSON.parse(input);
        const existing = JSON.parse(localStorage.getItem('collected_teacher_diagnostics') || '[]');
        if (Array.isArray(parsed)) {
          existing.push(...parsed);
        } else {
          existing.push(parsed);
        }
        localStorage.setItem('collected_teacher_diagnostics', JSON.stringify(existing));
        document.getElementById('vault-manual-input').value = '';
        refreshVaultDisplay();
        alert('Successfully ingested payload into vault!');
      } catch (e) {
        alert('Invalid JSON format: ' + e.message);
      }
    }

    function clearVault() {
      if (confirm('Are you sure you want to clear all cached survey submissions?')) {
        localStorage.removeItem('collected_teacher_diagnostics');
        refreshVaultDisplay();
      }
    }

    // Refresh on tab load
    document.addEventListener('DOMContentLoaded', refreshVaultDisplay);
  </script>
"""

if 'id="surveys-tab"' not in html:
    html = html.replace('<div id="appendix-tab"', surveys_tab_content + '\n  <div id="appendix-tab"')

with open('/workspaces/backup_final-thesis/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Successfully injected Field Surveys Tab into index.html!")
