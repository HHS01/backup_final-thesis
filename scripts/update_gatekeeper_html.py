import sys

with open('/workspaces/CC_3/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# -------------------------------------------------------------
# 1. Update Title & Description in Subtab 1
# -------------------------------------------------------------
old_header = '''      <!-- SUBTAB 1: 7-ITEM FEASIBILITY PRE-FLIGHT AUDIT -->
      <div id="audit-subtab" class="classroom-content block">
        <div class="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <span class="badge-pill bg-emerald-100 text-emerald-800 mb-2">Pre-Deployment Practicality Check</span>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-stone-900 font-serif">EdTech Readiness Check</h2>
            <p class="text-stone-600 mt-1 max-w-3xl text-sm sm:text-base">
              A 2-minute diagnostic for classroom teachers, school heads, and community committees before adopting incoming digital tools or donor hardware.
            </p>
          </div>'''

new_header = '''      <!-- SUBTAB 1: UNIFIED DUAL-STAKEHOLDER GATEKEEPER & RESOLUTION MEMO -->
      <div id="audit-subtab" class="classroom-content block">
        <div class="mb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <div class="flex items-center gap-2 mb-2">
              <span class="badge-pill bg-emerald-100 text-emerald-800 text-xs">Community Governance &amp; Gatekeeping</span>
              <span class="badge-pill bg-blue-100 text-blue-800 text-xs">Pillars 1, 3 &amp; 4</span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-stone-900 font-serif">Dual-Stakeholder Gatekeeping Screener</h2>
            <p class="text-stone-600 mt-1 max-w-3xl text-sm sm:text-base">
              Unified pre-flight audit combining <strong>Stream A: Teacher Pedagogical Feasibility</strong> with <strong>Stream B: SMC / Community Governance &amp; Safeguarding</strong>. Generates an evidence-backed statutory resolution memorandum with explicit rejection rationales before adopting donor hardware or incoming apps.
            </p>
          </div>'''

if old_header not in html:
    print("Error: old_header not found!")
    sys.exit(1)

html = html.replace(old_header, new_header)

# -------------------------------------------------------------
# 2. Add Section Dividers and Stream B (SMC Questions 8-11)
# -------------------------------------------------------------
q7_end_marker = '''                <div>
                  <span class="font-bold text-rose-900 block">Isolated Drill (-3 pts)</span>
                  <span class="text-stone-600 text-xs">Students in silent screen-staring with algorithmic tracking.</span>
                </div>
              </label>
            </div>
          </div>

        </div>'''

stream_b_html = '''                <div>
                  <span class="font-bold text-rose-900 block">Isolated Drill (-3 pts)</span>
                  <span class="text-stone-600 text-xs">Students in silent screen-staring with algorithmic tracking.</span>
                </div>
              </label>
            </div>
          </div>

          <!-- STREAM B: SMC / COMMUNITY GOVERNANCE & SAFEGUARDING DIVIDER -->
          <div class="pt-6 mt-6 border-t-2 border-stone-200">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
              <div>
                <span class="badge-pill bg-purple-100 text-purple-800 text-xs mb-1 inline-block">Stream B · Statutory Community Governance</span>
                <h3 class="text-lg sm:text-xl font-bold text-stone-900 font-serif">School Management Committee (SMC) &amp; PTA Safeguarding Scorecard</h3>
                <p class="text-xs text-stone-600">
                  Statutory oversight mandated by National Basic Education Acts (e.g. Kenya Basic Education Act §55, Nigeria UBE Act, Ghana GES). Protects school budgets and pupil welfare against the 85% Pilot Graveyard.
                </p>
              </div>
              <span class="text-xs font-mono text-purple-700 font-semibold bg-purple-50 px-2.5 py-1 rounded-lg border border-purple-200">4 Community Checkpoints</span>
            </div>
          </div>

          <!-- Question 8: 40/60 Lifecycle Budget -->
          <div class="pb-5 border-b border-stone-100">
            <div class="flex items-center justify-between mb-3">
              <label class="text-sm sm:text-base font-bold text-stone-900 flex items-center gap-2">
                <span class="w-6 h-6 rounded-full bg-purple-100 text-purple-800 text-xs font-bold inline-flex items-center justify-center">8</span>
                <span>The 40/60 Lifecycle Rule (Maintenance &amp; TCO) <sup class="text-purple-700 font-mono text-[11px]">[8]</sup></span>
              </label>
              <div class="relative inline-block">
                <span class="tooltip-trigger cursor-pointer text-xs font-bold text-stone-400 hover:text-stone-700 bg-stone-100 w-5 h-5 rounded-full inline-flex items-center justify-center">?</span>
                <div class="tooltip-box absolute right-0 z-30 w-72 p-2.5 text-xs bg-stone-900 text-stone-200 rounded-lg shadow-xl -mt-1 font-normal leading-relaxed">
                  UNESCO DTC Benchmark: Capital procurement (hardware) accounts for only 40% of Total Cost of Ownership. 60% must be ring-fenced for battery replacement, screen repairs, charging infrastructure, and secure storage over 36 months.
                </div>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-emerald-500 hover:bg-emerald-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q8" value="3" checked onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-stone-900 block">Fully Endowed (+3 pts)</span>
                  <span class="text-stone-600 text-xs">Donor/grant includes ring-fenced 3-year repair fund &amp; certified local technician retainer.</span>
                </div>
              </label>
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-emerald-500 hover:bg-emerald-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q8" value="1" onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-stone-900 block">Partial Warranty (+1 pt)</span>
                  <span class="text-stone-600 text-xs">12-month manufacturer replacement only; post-year-1 maintenance falls on PTA levies.</span>
                </div>
              </label>
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-rose-400 hover:bg-rose-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q8" value="-5" onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-rose-900 block">CapEx-Only Drop (-5 pts)</span>
                  <span class="text-stone-600 text-xs">Unfunded hardware gift. First cracked screen or dead battery turns units into bricks.</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Question 9: Child Data Privacy & Commercialization -->
          <div class="pb-5 border-b border-stone-100">
            <div class="flex items-center justify-between mb-3">
              <label class="text-sm sm:text-base font-bold text-stone-900 flex items-center gap-2">
                <span class="w-6 h-6 rounded-full bg-purple-100 text-purple-800 text-xs font-bold inline-flex items-center justify-center">9</span>
                <span>Child Data Privacy &amp; Commercialization Safeguard <sup class="text-purple-700 font-mono text-[11px]">[9]</sup></span>
              </label>
              <div class="relative inline-block">
                <span class="tooltip-trigger cursor-pointer text-xs font-bold text-stone-400 hover:text-stone-700 bg-stone-100 w-5 h-5 rounded-full inline-flex items-center justify-center">?</span>
                <div class="tooltip-box absolute right-0 z-30 w-72 p-2.5 text-xs bg-stone-900 text-stone-200 rounded-lg shadow-xl -mt-1 font-normal leading-relaxed">
                  African Union Data Protection Convention (Malabo) &amp; Kenya Data Protection Act 2019: Prohibits unconsented collection of biometric, facial, phone, or location telemetry from minors.
                </div>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-emerald-500 hover:bg-emerald-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q9" value="3" checked onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-stone-900 block">Strict Privacy (+3 pts)</span>
                  <span class="text-stone-600 text-xs">Zero ad trackers; local pseudonymous offline IDs; no child phone numbers or photos harvested.</span>
                </div>
              </label>
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-emerald-500 hover:bg-emerald-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q9" value="1" onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-stone-900 block">School-Managed (+1 pt)</span>
                  <span class="text-stone-600 text-xs">Cloud account required, but governed by signed institutional data-sharing covenant.</span>
                </div>
              </label>
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-rose-400 hover:bg-rose-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q9" value="-4" onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-rose-900 block">Predatory / Ads (-4 pts)</span>
                  <span class="text-stone-600 text-xs">Contains third-party commercial SDKs, in-app advertising, or compulsory parent phone tracking.</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Question 10: Community Device Security & Overnight Custody -->
          <div class="pb-5 border-b border-stone-100">
            <div class="flex items-center justify-between mb-3">
              <label class="text-sm sm:text-base font-bold text-stone-900 flex items-center gap-2">
                <span class="w-6 h-6 rounded-full bg-purple-100 text-purple-800 text-xs font-bold inline-flex items-center justify-center">10</span>
                <span>Physical Custody, Theft Prevention &amp; Safe Storage <sup class="text-purple-700 font-mono text-[11px]">[10]</sup></span>
              </label>
              <div class="relative inline-block">
                <span class="tooltip-trigger cursor-pointer text-xs font-bold text-stone-400 hover:text-stone-700 bg-stone-100 w-5 h-5 rounded-full inline-flex items-center justify-center">?</span>
                <div class="tooltip-box absolute right-0 z-30 w-72 p-2.5 text-xs bg-stone-900 text-stone-200 rounded-lg shadow-xl -mt-1 font-normal leading-relaxed">
                  In rural and informal peri-urban schools lacking perimeter security, unattended digital hardware creates severe burglary vulnerability. An SMC custody pact is required.
                </div>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-emerald-500 hover:bg-emerald-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q10" value="3" checked onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-stone-900 block">Reinforced Custody (+3 pts)</span>
                  <span class="text-stone-600 text-xs">Padlocked steel charging trunk + security-guarded staff room + community watch pact.</span>
                </div>
              </label>
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-emerald-500 hover:bg-emerald-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q10" value="1" onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-stone-900 block">Standard Lockup (+1 pt)</span>
                  <span class="text-stone-600 text-xs">Locked headteacher cabinet; no night guard or insurance coverage.</span>
                </div>
              </label>
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-rose-400 hover:bg-rose-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q10" value="-3" onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-rose-900 block">Exposed / Unsecured (-3 pts)</span>
                  <span class="text-stone-600 text-xs">No reinforced locks, steel grilles, or safe room; high risk of opportunistic theft.</span>
                </div>
              </label>
            </div>
          </div>

          <!-- Question 11: Teacher Non-Displacement & Professional Dignity -->
          <div>
            <div class="flex items-center justify-between mb-3">
              <label class="text-sm sm:text-base font-bold text-stone-900 flex items-center gap-2">
                <span class="w-6 h-6 rounded-full bg-purple-100 text-purple-800 text-xs font-bold inline-flex items-center justify-center">11</span>
                <span>Teacher Non-Displacement &amp; Professional Dignity <sup class="text-purple-700 font-mono text-[11px]">[11]</sup></span>
              </label>
              <div class="relative inline-block">
                <span class="tooltip-trigger cursor-pointer text-xs font-bold text-stone-400 hover:text-stone-700 bg-stone-100 w-5 h-5 rounded-full inline-flex items-center justify-center">?</span>
                <div class="tooltip-box absolute right-0 z-30 w-72 p-2.5 text-xs bg-stone-900 text-stone-200 rounded-lg shadow-xl -mt-1 font-normal leading-relaxed">
                  International Labour Organization (ILO) &amp; Education International: Technology must augment the teacher's professional autonomy, not reduce them to robotic screen proctors or script-readers.
                </div>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-emerald-500 hover:bg-emerald-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q11" value="3" checked onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-stone-900 block">Augmenting (+3 pts)</span>
                  <span class="text-stone-600 text-xs">Empowers teacher with diagnostic insights, leaving pedagogical pacing in their control.</span>
                </div>
              </label>
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-emerald-500 hover:bg-emerald-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q11" value="1" onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-stone-900 block">Supplementary (+1 pt)</span>
                  <span class="text-stone-600 text-xs">Self-paced student practice during designated library or afternoon remedial hours.</span>
                </div>
              </label>
              <label class="flex items-start gap-2.5 p-3 rounded-xl border border-stone-200 hover:border-rose-400 hover:bg-rose-50/20 cursor-pointer transition text-xs sm:text-sm">
                <input type="radio" name="audit_q11" value="-3" onchange="calculateAudit()" class="text-purple-600 focus:ring-purple-500 mt-0.5">
                <div>
                  <span class="font-bold text-rose-900 block">Displacing / Scripted (-3 pts)</span>
                  <span class="text-stone-600 text-xs">Scripted tablet lessons that bypass teacher judgment or treat teachers as screen minders.</span>
                </div>
              </label>
            </div>
          </div>

        </div>'''

if q7_end_marker not in html:
    print("Error: q7_end_marker not found!")
    sys.exit(1)

html = html.replace(q7_end_marker, stream_b_html)

# -------------------------------------------------------------
# 3. Update Citations block to include citations [8], [9], [10], [11]
# -------------------------------------------------------------
old_citations = '''            <div><strong class="text-stone-900">[6] Administrative Double Entry:</strong> World Bank SABER-ICT Policy Analysis; Piper, B. et al. (2018) <em>Teacher Time on Task and Instructional Practice in Sub-Saharan Africa</em> (RTI International).</div>
            <div><strong class="text-stone-900">[7] Pedagogical Purpose:</strong> Biesta, Gert (2010). <em>Good Education in an Age of Measurement: Ethics, Politics, Democracy</em>. Paradigm Publishers / Routledge.</div>'''

new_citations = '''            <div><strong class="text-stone-900">[6] Administrative Double Entry:</strong> World Bank SABER-ICT Policy Analysis; Piper, B. et al. (2018) <em>Teacher Time on Task and Instructional Practice in Sub-Saharan Africa</em> (RTI International).</div>
            <div><strong class="text-stone-900">[7] Pedagogical Purpose:</strong> Biesta, Gert (2010). <em>Good Education in an Age of Measurement: Ethics, Politics, Democracy</em>. Paradigm Publishers / Routledge.</div>
            <div><strong class="text-stone-900">[8] The 40/60 Lifecycle Rule (TCO):</strong> UNESCO Digital Transformation Collaborative (DTC, 2024); World Bank EdTech Total Cost of Ownership Modeling Guidelines.</div>
            <div><strong class="text-stone-900">[9] Child Safeguarding &amp; Minor Privacy:</strong> African Union Convention on Cyber Security and Personal Data Protection (Malabo Convention); Human Rights Watch (2022) <em>"How Dare They Peep into My Private Life?"</em>.</div>
            <div><strong class="text-stone-900">[10] SMC Asset Governance &amp; Community Custody:</strong> Kenya Basic Education Act (2013, §55-59 SMC statutory responsibilities); World Bank Decentralized School Management Empirical Reviews.</div>
            <div><strong class="text-stone-900">[11] Teacher Professional Dignity:</strong> International Labour Organization (ILO) &amp; UNESCO (1966/2021) <em>Recommendations concerning the Status of Teachers in the Digital Era</em>.</div>'''

if old_citations not in html:
    print("Error: old_citations not found!")
    sys.exit(1)

html = html.replace(old_citations, new_citations)

# -------------------------------------------------------------
# 4. Update Printable Memorandum Card with Explicit Rejection Rationales & Dual Sign-Off
# -------------------------------------------------------------
old_verdict_header = '''              <!-- Print-Only Memorandum Header -->
              <div class="print-header hidden pb-3 mb-4 border-b border-stone-200">
                <div class="flex items-center justify-between">
                  <div>
                    <h2 class="text-xl font-bold text-stone-900">EdTech Feasibility &amp; Practicality Memorandum</h2>
                    <p class="text-xs text-stone-500">School Pre-Deployment Diagnostic Assessment • Classroom Decision Record</p>
                  </div>
                  <div class="text-right text-xs text-stone-400">
                    <div id="memo-date" class="font-medium text-stone-600"></div>
                    <div>Observatory Practicality Toolkit</div>
                  </div>
                </div>
              </div>'''

new_verdict_header = '''              <!-- Print-Only Memorandum Header -->
              <div class="print-header hidden pb-3 mb-4 border-b-2 border-stone-800">
                <div class="flex items-center justify-between">
                  <div>
                    <span class="text-[10px] font-bold uppercase tracking-widest text-stone-500 block">Official Statutory School Decision Record</span>
                    <h2 class="text-xl font-bold text-stone-900">Joint Teacher Screener &amp; SMC Resolution Memorandum</h2>
                    <p class="text-xs text-stone-600">Issued pursuant to School Management Committee Governance Guidelines &amp; UNESCO Six Pillars Architecture</p>
                  </div>
                  <div class="text-right text-xs text-stone-500">
                    <div id="memo-date" class="font-bold text-stone-800"></div>
                    <div class="text-[10px] font-mono text-stone-400">Ref: SMC-GATE-2026/DOC</div>
                  </div>
                </div>
              </div>'''

if old_verdict_header not in html:
    print("Error: old_verdict_header not found!")
    sys.exit(1)

html = html.replace(old_verdict_header, new_verdict_header)

old_print_footer = '''            <!-- Print Memorandum Sign-off (Visible only in Print) -->
            <div class="print-footer hidden pt-4 mt-6 border-t border-stone-200 text-xs text-stone-500">
              <div class="flex justify-between items-center">
                <span>EdTech Co-Design Observatory — Pre-Deployment Practicality Diagnostic</span>
                <span class="italic">School Decision Record</span>
              </div>
            </div>'''

new_print_footer = '''            <!-- Rejection Rationale / Adoption Condition Resolution Box -->
            <div id="audit-resolution-box" class="p-3.5 rounded-xl bg-stone-50 border border-stone-200 text-xs mt-3">
              <!-- Populated dynamically by calculateAudit() -->
            </div>

            <!-- Print Memorandum Dual Sign-off (Visible in Print & Memo) -->
            <div class="print-footer hidden pt-5 mt-6 border-t-2 border-stone-300 text-xs text-stone-700">
              <div class="mb-3">
                <span class="font-bold uppercase tracking-wider text-[11px] text-stone-600 block mb-1">Dual-Stakeholder Statutory Certification &amp; School Seal:</span>
                <p class="text-[11px] text-stone-500 leading-tight">
                  By signing below, the Lead Frontline Teacher confirms pedagogical and operational feasibility, and the SMC Chairperson / Headteacher ratifies asset stewardship, child data safeguarding, and recurrent maintenance funding compliance.
                </p>
              </div>
              <div class="grid grid-cols-2 gap-8 pt-4">
                <div class="border-t border-stone-400 pt-2">
                  <div class="font-bold text-stone-900">Lead Teacher / Department Head</div>
                  <div class="text-[10px] text-stone-500">Name &amp; Signature · Date: _________________</div>
                  <div class="text-[10px] italic text-stone-400 mt-1">Pedagogical Feasibility Certification</div>
                </div>
                <div class="border-t border-stone-400 pt-2">
                  <div class="font-bold text-stone-900">SMC Chairperson / Headteacher</div>
                  <div class="text-[10px] text-stone-500">Name, Signature &amp; Official School Stamp · Date: _________________</div>
                  <div class="text-[10px] italic text-stone-400 mt-1">Community Asset &amp; Safeguarding Ratification</div>
                </div>
              </div>
              <div class="flex justify-between items-center pt-4 mt-4 border-t border-stone-200 text-[10px] text-stone-400">
                <span>EdTech Co-Design Observatory · Component B Decision-Support Deliverable</span>
                <span>UniTO Master in ICT4D · Academic Year 2025–2026</span>
              </div>
            </div>'''

if old_print_footer not in html:
    print("Error: old_print_footer not found!")
    sys.exit(1)

html = html.replace(old_print_footer, new_print_footer)

with open('/workspaces/CC_3/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully updated Subtab 1 HTML structure for Dual-Stakeholder Gatekeeping!")
