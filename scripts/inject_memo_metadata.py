with open('/workspaces/CC_3/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '''        <!-- Diagnostic Questions Container (Full Width with Horizontal Card Layout) -->
        <div class="bg-white rounded-2xl p-6 sm:p-8 border border-stone-200 shadow-sm space-y-6 mb-8">
          
          <!-- Question 1 -->'''

meta_strip = '''        <!-- Incoming Proposal Metadata Strip (Context & Accountability) -->
        <div class="bg-stone-100 rounded-2xl p-5 sm:p-6 border border-stone-200 shadow-sm mb-6">
          <div class="flex items-center justify-between pb-3 mb-3 border-b border-stone-200">
            <span class="text-xs font-bold uppercase tracking-wider text-stone-600 flex items-center gap-1.5">
              <span>📋</span> Incoming Proposal Audit Record (Optional / Informational)
            </span>
            <span class="text-[11px] text-stone-500 font-mono">Prints directly on resolution memo</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            <div>
              <label class="block font-bold text-stone-700 mb-1">Target School / Community:</label>
              <input type="text" id="meta-school-name" placeholder="e.g. Kibera Primary / St. Jude SMC" oninput="syncAuditMeta()" class="w-full px-2.5 py-1.5 rounded-lg border border-stone-300 bg-white text-stone-900 focus:ring-1 focus:ring-emerald-500 text-xs">
            </div>
            <div>
              <label class="block font-bold text-stone-700 mb-1">Tool / Vendor / Hardware:</label>
              <input type="text" id="meta-tool-name" placeholder="e.g. Donor Tablet Pilot / Literacy App" oninput="syncAuditMeta()" class="w-full px-2.5 py-1.5 rounded-lg border border-stone-300 bg-white text-stone-900 focus:ring-1 focus:ring-emerald-500 text-xs">
            </div>
            <div>
              <label class="block font-bold text-stone-700 mb-1">Sponsoring Body / Donor:</label>
              <input type="text" id="meta-donor-name" placeholder="e.g. Bilateral Donor / Private Foundation" oninput="syncAuditMeta()" class="w-full px-2.5 py-1.5 rounded-lg border border-stone-300 bg-white text-stone-900 focus:ring-1 focus:ring-emerald-500 text-xs">
            </div>
            <div>
              <label class="block font-bold text-stone-700 mb-1">Lead Reviewer / Role:</label>
              <input type="text" id="meta-reviewer-name" placeholder="e.g. Head of Science / SMC Chair" oninput="syncAuditMeta()" class="w-full px-2.5 py-1.5 rounded-lg border border-stone-300 bg-white text-stone-900 focus:ring-1 focus:ring-emerald-500 text-xs">
            </div>
          </div>
        </div>

        <!-- Diagnostic Questions Container (Full Width with Horizontal Card Layout) -->
        <div class="bg-white rounded-2xl p-6 sm:p-8 border border-stone-200 shadow-sm space-y-6 mb-8">
          
          <!-- Question 1 -->'''

if target not in html:
    print("Error: target not found!")
    exit(1)

html = html.replace(target, meta_strip)

# Now inject the printed metadata block inside the print header in the verdict card
print_header_target = '''                    <div id="memo-date" class="font-bold text-stone-800"></div>
                    <div class="text-[10px] font-mono text-stone-400">Ref: SMC-GATE-2026/DOC</div>
                  </div>
                </div>
              </div>'''

new_print_header = '''                    <div id="memo-date" class="font-bold text-stone-800"></div>
                    <div class="text-[10px] font-mono text-stone-400">Ref: SMC-GATE-2026/DOC</div>
                  </div>
                </div>
                <!-- Dynamic Audit Metadata Strip in Print -->
                <div id="print-meta-docket" class="mt-3 pt-2 border-t border-stone-200 grid grid-cols-4 gap-2 text-[11px] text-stone-700">
                  <div><strong>School:</strong> <span id="print-school-val" class="font-mono text-stone-900">General Public School</span></div>
                  <div><strong>Tool / Hardware:</strong> <span id="print-tool-val" class="font-mono text-stone-900">Incoming EdTech Proposal</span></div>
                  <div><strong>Sponsor / Donor:</strong> <span id="print-donor-val" class="font-mono text-stone-900">External Entity</span></div>
                  <div><strong>Reviewer:</strong> <span id="print-reviewer-val" class="font-mono text-stone-900">Joint Teacher/SMC Panel</span></div>
                </div>
              </div>'''

if print_header_target not in html:
    print("Error: print_header_target not found!")
    exit(1)

html = html.replace(print_header_target, new_print_header)

# Inject syncAuditMeta() function into the JS
js_marker = 'function calculateAudit() {'
js_addition = '''function syncAuditMeta() {
      const school = document.getElementById('meta-school-name')?.value.trim() || 'General Public School';
      const tool = document.getElementById('meta-tool-name')?.value.trim() || 'Incoming EdTech Proposal';
      const donor = document.getElementById('meta-donor-name')?.value.trim() || 'External Entity';
      const reviewer = document.getElementById('meta-reviewer-name')?.value.trim() || 'Joint Teacher/SMC Panel';

      const pSchool = document.getElementById('print-school-val');
      const pTool = document.getElementById('print-tool-val');
      const pDonor = document.getElementById('print-donor-val');
      const pReviewer = document.getElementById('print-reviewer-val');

      if (pSchool) pSchool.textContent = school;
      if (pTool) pTool.textContent = tool;
      if (pDonor) pDonor.textContent = donor;
      if (pReviewer) pReviewer.textContent = reviewer;
    }

    function calculateAudit() {'''

if js_marker not in html:
    print("Error: js_marker not found!")
    exit(1)

html = html.replace(js_marker, js_addition, 1)

with open('/workspaces/CC_3/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully injected Metadata Strip and print synchronization into index.html!")
