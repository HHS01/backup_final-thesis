import sys

with open('/workspaces/CC_3/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '// =================================================================\n    // TOOL 1: FEASIBILITY PRE-FLIGHT AUDIT ENGINE'
end_marker = '// =================================================================\n    // TOOL 2: DYNAMIC CLASS CROWDING & ROTATION PLANNER'

start = html.find(start_marker)
end = html.find(end_marker)

if start == -1 or end == -1:
    print(f"Error: markers not found (start={start}, end={end})")
    sys.exit(1)

new_audit_js = '''// =================================================================
    // TOOL 1: UNIFIED DUAL-STAKEHOLDER GATEKEEPER & RESOLUTION ENGINE
    // Stream A: Teacher Pedagogical Feasibility (Q1-Q7)
    // Stream B: SMC / Community Governance & Safeguarding (Q8-Q11)
    // =================================================================
    function calculateAudit() {
      // Stream A: Teacher Feasibility
      const q1 = parseInt(document.querySelector('input[name="audit_q1"]:checked')?.value || 0);
      const q2 = parseInt(document.querySelector('input[name="audit_q2"]:checked')?.value || 0);
      const q3 = parseInt(document.querySelector('input[name="audit_q3"]:checked')?.value || 0);
      const q4 = parseInt(document.querySelector('input[name="audit_q4"]:checked')?.value || 0);
      const q5 = parseInt(document.querySelector('input[name="audit_q5"]:checked')?.value || 0);
      const q6 = parseInt(document.querySelector('input[name="audit_q6"]:checked')?.value || 0);
      const q7 = parseInt(document.querySelector('input[name="audit_q7"]:checked')?.value || 0);

      // Stream B: SMC / Community Governance
      const q8 = parseInt(document.querySelector('input[name="audit_q8"]:checked')?.value || 0);
      const q9 = parseInt(document.querySelector('input[name="audit_q9"]:checked')?.value || 0);
      const q10 = parseInt(document.querySelector('input[name="audit_q10"]:checked')?.value || 0);
      const q11 = parseInt(document.querySelector('input[name="audit_q11"]:checked')?.value || 0);

      const streamAScore = q1 + q2 + q3 + q4 + q5 + q6 + q7;
      const streamBScore = q8 + q9 + q10 + q11;
      const totalScore = streamAScore + streamBScore;

      const scoreNum = document.getElementById('audit-score-num');
      const scoreBar = document.getElementById('audit-score-bar');
      const badge = document.getElementById('verdict-badge');
      const card = document.getElementById('verdict-card');
      const strengthsBox = document.getElementById('audit-strengths-box');
      const flagsBox = document.getElementById('audit-flags-box');
      const resolutionBox = document.getElementById('audit-resolution-box');
      const memoDateEl = document.getElementById('memo-date');

      if (memoDateEl) {
        memoDateEl.textContent = new Date().toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
      }

      if (scoreNum) scoreNum.textContent = (totalScore > 0 ? '+' : '') + totalScore;

      // Scale: -37 (worst) to +32 (best) -> 69 pt range
      const pct = Math.max(5, Math.min(100, Math.round(((totalScore + 37) / 69) * 100)));
      if (scoreBar) scoreBar.style.width = pct + '%';

      // Critical Red Flag Gatekeepers
      const isDataRedFlag = (q3 === -5);
      const isPowerRedFlag = (q2 === -3);
      const isTcoRedFlag = (q8 === -5);
      const isPrivacyRedFlag = (q9 === -4);

      // Explicit Rejection Rationales (Gatekeeping Triggers)
      const rejectionTriggers = [];
      if (isDataRedFlag) {
        rejectionTriggers.push({
          stakeholder: 'Frontline Teachers',
          pillar: 'Pillar 3 (Cost & Sustainability)',
          clause: 'Informal Salary Tax Breach',
          rationale: 'Rejected: Solution imposes recurring personal airtime data bundle costs on teachers (violating the 4-8% salary threshold).'
        });
      }
      if (isPowerRedFlag) {
        rejectionTriggers.push({
          stakeholder: 'School Administration',
          pillar: 'Pillar 2 (Infrastructure)',
          clause: 'Daily Grid Failure Vulnerability',
          rationale: 'Rejected: Tool requires continuous grid connectivity in an un-electrified classroom without solar/offline caching.'
        });
      }
      if (isTcoRedFlag) {
        rejectionTriggers.push({
          stakeholder: 'SMC / PTA Committee',
          pillar: 'Pillar 3 (Lifecycle Sustainability)',
          clause: '40/60 Lifecycle Deficit (Pilot Graveyard Trigger)',
          rationale: 'Rejected: Unfunded capital hardware drop with zero ring-fenced maintenance/screen replacement budget (guarantees abandonment within 12 months).'
        });
      }
      if (isPrivacyRedFlag) {
        rejectionTriggers.push({
          stakeholder: 'SMC / Community Custodians',
          pillar: 'Pillar 6 (Data & Governance)',
          clause: 'Minor Exploitation & Malabo Convention Breach',
          rationale: 'Rejected: Software includes third-party ad tracking or harvests student/parent personal identifiers without statutory safeguards.'
        });
      }
      if (q1 === -3) {
        rejectionTriggers.push({
          stakeholder: 'Headteacher / Teachers',
          pillar: 'Pillar 1 (Leadership & Curriculum)',
          clause: 'Unaccredited Curriculum Penalty',
          rationale: 'Rejected: Unvetted external software risks government school inspectorate sanctions for diverting approved syllabus hours.'
        });
      }

      // Collect Strengths & Working Conditions
      const strengths = [];
      const flags = [];

      // Q1: Curriculum
      if (q1 === 3) strengths.push({ stream: 'Teacher', title: 'Curriculum Accreditation', text: 'Officially accredited by National Curriculum Body (e.g. KICD / REB).' });
      else if (q1 === 1) flags.push({ level: 'amber', stream: 'Teacher', text: 'Curriculum: Aligned with syllabus topics, but lacks official ministry sign-off.' });
      else if (q1 === -3) flags.push({ level: 'rose', stream: 'Teacher', text: 'Curriculum Risk: Unaccredited tool risks inspectorate sanctions during school audits.' });

      // Q2: Power
      if (q2 === 3) strengths.push({ stream: 'Teacher', title: 'Energy & Power', text: 'Daily dependable grid electricity or solar micro-grid available on-site.' });
      else if (q2 === 1) flags.push({ level: 'amber', stream: 'Teacher', text: 'Power: Intermittent school electricity — requires weekly scheduled charging routines.' });
      else if (q2 === -3) flags.push({ level: 'rose', stream: 'Teacher', text: 'Critical Power Block: No school electricity — requires off-site battery hauling or solar backup.' });

      // Q3: Data
      if (q3 === 3) strengths.push({ stream: 'Teacher', title: 'Data & Connectivity', text: '100% offline local Wi-Fi cache or school-funded connection (zero teacher data cost).' });
      else if (q3 === 2) flags.push({ level: 'amber', stream: 'Teacher', text: 'Connectivity: Dependent on telecom zero-rating — verify active whitelist coverage.' });
      else if (q3 === -5) flags.push({ level: 'rose', stream: 'Teacher', text: 'Critical Airtime Tax: Teachers/students must buy personal data bundles (high resistance risk).' });

      // Q4: Class crowding
      if (q4 === 3) strengths.push({ stream: 'Teacher', title: 'Classroom Density', text: 'Adequate 1:1 or 2:1 pair-learning ratio in classroom.' });
      else if (q4 === 1) flags.push({ level: 'amber', stream: 'Teacher', text: 'Class Crowding: High ratio (3:1 to 6:1) — pair with the 3-Station Scheduler below.' });
      else if (q4 === -3) flags.push({ level: 'rose', stream: 'Teacher', text: 'Device Bottleneck: Over 10:1 ratio without structured rotation will cause chaotic lessons.' });

      // Q5: Language
      if (q5 === 3) strengths.push({ stream: 'Teacher', title: 'Linguistic & Cultural Fit', text: 'Full mother-tongue alignment with localized cultural scenarios.' });
      else if (q5 === 1) flags.push({ level: 'amber', stream: 'Teacher', text: 'Language: Bilingual scaffolding present, but early learners will need oral translation.' });
      else if (q5 === -3) flags.push({ level: 'rose', stream: 'Teacher', text: 'Language Barrier: Monolingual tool with poor AI comprehension in regional mother tongues.' });

      // Q6: Admin double entry
      if (q6 === 2) strengths.push({ stream: 'Teacher', title: 'Administrative Workflow', text: 'Automatically exports to official school/government term sheets (zero double entry).' });
      else if (q6 === 1) flags.push({ level: 'amber', stream: 'Teacher', text: 'Reporting: Self-contained tool; does not integrate into government grade ledgers.' });
      else if (q6 === -2) flags.push({ level: 'rose', stream: 'Teacher', text: 'Double Bookkeeping: Adds 30–60 mins daily manual transcription into paper registers.' });

      // Q7: Pedagogical purpose
      if (q7 === 3) strengths.push({ stream: 'Teacher', title: 'Pedagogical Purpose', text: 'Fosters collaborative peer dialogue, group problem-solving & learner agency (Biesta balance).' });
      else if (q7 === 1) flags.push({ level: 'amber', stream: 'Teacher', text: 'Pedagogy: Drill software requires teacher-led offline reflection to ensure active learning.' });
      else if (q7 === -3) flags.push({ level: 'rose', stream: 'Teacher', text: 'Pedagogy Risk: Passive screen-staring lacking collaborative discussion or learner agency.' });

      // Stream B SMC items:
      // Q8: 40/60 Lifecycle
      if (q8 === 3) strengths.push({ stream: 'SMC', title: 'Lifecycle Sustainability', text: '3-year ring-fenced maintenance endowment and local repair technician retainer in place.' });
      else if (q8 === 1) flags.push({ level: 'amber', stream: 'SMC', text: 'Maintenance: 12-month manufacturer warranty only; post-year-1 repairs will pressure PTA budget.' });
      else if (q8 === -5) flags.push({ level: 'rose', stream: 'SMC', text: 'Critical TCO Gap: CapEx hardware gift with zero maintenance budget (Pilot Graveyard risk).' });

      // Q9: Child Data Privacy
      if (q9 === 3) strengths.push({ stream: 'SMC', title: 'Child Data Safeguarding', text: 'Zero commercial trackers; local pseudonymous offline IDs; compliant with Malabo Convention.' });
      else if (q9 === 1) flags.push({ level: 'amber', stream: 'SMC', text: 'Data Governance: Cloud student accounts require signed institutional privacy covenant.' });
      else if (q9 === -4) flags.push({ level: 'rose', stream: 'SMC', text: 'Commercial Exploitation Risk: Ad SDKs or student phone harvesting detected.' });

      // Q10: Custody & Physical Storage
      if (q10 === 3) strengths.push({ stream: 'SMC', title: 'Asset Protection', text: 'Padlocked steel charging trunks in secured room backed by community watch pact.' });
      else if (q10 === 1) flags.push({ level: 'amber', stream: 'SMC', text: 'Physical Storage: Standard cabinet lockup; lacks night guard or burglary insurance.' });
      else if (q10 === -3) flags.push({ level: 'rose', stream: 'SMC', text: 'Security Vulnerability: No reinforced locks or safe room; extreme risk of opportunistic burglary.' });

      // Q11: Teacher Dignity & Autonomy
      if (q11 === 3) strengths.push({ stream: 'SMC', title: 'Teacher Professional Dignity', text: 'Augments teacher autonomy with diagnostic tools; upholds ILO/UNESCO teaching standards.' });
      else if (q11 === 1) flags.push({ level: 'amber', stream: 'SMC', text: 'Teacher Role: Supplementary software; minimal professional development provided.' });
      else if (q11 === -3) flags.push({ level: 'rose', stream: 'SMC', text: 'Pedagogical De-skilling: Scripted screen lessons relegate teachers to passive minders.' });

      // Render Dynamic Strengths Box
      if (strengthsBox) {
        if (strengths.length === 0) {
          strengthsBox.innerHTML = `
            <div class="text-stone-500 italic text-xs flex items-center gap-1.5">
              <span>No baseline operational enablers verified across Teacher and SMC checkpoints.</span>
            </div>`;
        } else {
          strengthsBox.innerHTML = `
            <div class="font-bold text-emerald-950 text-xs mb-1.5 flex items-center justify-between">
              <span class="flex items-center gap-1.5">
                <svg class="w-4 h-4 text-emerald-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                <span>Verified Working Conditions (${strengths.length} of 11 Checkpoints):</span>
              </span>
              <span class="text-[10px] font-mono text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded">Teacher: +${streamAScore} | SMC: +${streamBScore}</span>
            </div>
            <ul class="space-y-1.5 text-xs">
              ${strengths.map(s => `
                <li class="flex items-start gap-1.5 text-emerald-950">
                  <span class="text-emerald-600 font-bold shrink-0">✓</span>
                  <span><span class="text-[10px] font-bold px-1 rounded ${s.stream === 'SMC' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'} mr-1">${s.stream}</span><strong class="font-semibold text-emerald-900">${s.title}:</strong> ${s.text}</span>
                </li>
              `).join('')}
            </ul>`;
        }
      }

      // Render Dynamic Flags
      if (flagsBox) {
        if (flags.length === 0) {
          flagsBox.innerHTML = `
            <div class="text-emerald-800 font-medium flex items-center gap-1.5 text-xs">
              <svg class="w-4 h-4 text-emerald-600 shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
              <span>Zero Operational Friction Detected: Passes both Teacher and SMC gatekeeping standards.</span>
            </div>`;
        } else {
          flagsBox.innerHTML = `
            <div class="font-bold text-stone-900 text-xs mb-1.5 flex items-center gap-1.5">
              <span class="text-amber-600 font-bold shrink-0">⚠️</span>
              <span>Identified Friction Points &amp; Governance Constraints (${flags.length}):</span>
            </div>
            <ul class="space-y-1.5 text-xs">
              ${flags.map(f => `
                <li class="flex items-start gap-1.5 ${f.level === 'rose' ? 'text-rose-800 font-semibold' : 'text-stone-700'}">
                  <span class="${f.level === 'rose' ? 'text-rose-600' : 'text-amber-600'} font-bold shrink-0">${f.level === 'rose' ? '⛔' : '⚠️'}</span>
                  <span><span class="text-[10px] font-bold px-1 rounded ${f.stream === 'SMC' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'} mr-1">${f.stream}</span>${f.text}</span>
                </li>
              `).join('')}
            </ul>`;
        }
      }

      // Render Explicit Resolution & Rejection Rationale Box
      if (resolutionBox) {
        if (rejectionTriggers.length > 0) {
          resolutionBox.className = 'p-4 rounded-xl bg-rose-50 border-2 border-rose-300 text-xs mt-3';
          resolutionBox.innerHTML = `
            <div class="flex items-center gap-2 mb-2 text-rose-900 font-bold text-sm">
              <span class="text-lg">🛑</span>
              <span>SMC Statutory Resolution: VETO / REJECTION DIRECTIVE</span>
            </div>
            <p class="text-rose-800 mb-3 leading-relaxed">
              Pursuant to School Management Committee mandate, this technology deployment is <strong>REJECTED</strong> in its current form due to ${rejectionTriggers.length} statutory breach(es). The school declines physical acceptance or signed delivery receipt until the following formal conditions are rectified:
            </p>
            <div class="space-y-2">
              ${rejectionTriggers.map((t, idx) => `
                <div class="p-2.5 rounded bg-white border border-rose-200">
                  <div class="flex items-center justify-between text-[11px] font-bold text-rose-900 mb-0.5">
                    <span>${idx + 1}. ${t.clause} [${t.pillar}]</span>
                    <span class="text-[10px] font-mono uppercase bg-rose-100 text-rose-800 px-1.5 py-0.5 rounded">${t.stakeholder}</span>
                  </div>
                  <p class="text-stone-700 text-[11px] leading-tight">${t.rationale}</p>
                </div>
              `).join('')}
            </div>
          `;
        } else if (totalScore >= 16) {
          resolutionBox.className = 'p-4 rounded-xl bg-emerald-50 border-2 border-emerald-300 text-xs mt-3';
          resolutionBox.innerHTML = `
            <div class="flex items-center gap-2 mb-1.5 text-emerald-950 font-bold text-sm">
              <span class="text-lg">✅</span>
              <span>SMC Statutory Resolution: RATIFIED FOR CLASSROOM DEPLOYMENT</span>
            </div>
            <p class="text-emerald-900 leading-relaxed">
              The Joint Teacher &amp; SMC Review confirms that the proposed solution satisfies statutory curriculum accreditation, child data privacy (Malabo Convention), zero teacher airtime taxation, and ring-fenced lifecycle maintenance. Authorized for pilot implementation.
            </p>
          `;
        } else {
          resolutionBox.className = 'p-4 rounded-xl bg-amber-50 border-2 border-amber-300 text-xs mt-3';
          resolutionBox.innerHTML = `
            <div class="flex items-center gap-2 mb-1.5 text-amber-950 font-bold text-sm">
              <span class="text-lg">⚠️</span>
              <span>SMC Statutory Resolution: CONDITIONAL ADOPTION WITH MANDATORY CO-DESIGN</span>
            </div>
            <p class="text-amber-900 leading-relaxed">
              No fatal red flags detected, but moderate friction points exist across classroom density or maintenance reserves. Recommended to adopt strictly in paired rotational mode alongside the 3-Station Scheduler.
            </p>
          `;
        }
      }

      // Verdict Card Styling
      const hasFatalBreach = (rejectionTriggers.length > 0);
      if (card && badge && scoreBar) {
        if (!hasFatalBreach && totalScore >= 16) {
          card.className = 'lg:col-span-8 bg-white rounded-2xl p-6 sm:p-8 border-2 border-emerald-600 shadow-sm transition-all flex flex-col justify-between';
          badge.className = 'badge-pill bg-emerald-100 text-emerald-800 text-xs py-1 px-3 mt-1 inline-block';
          badge.textContent = 'GREEN LIGHT: Dual-Certified Ready';
          scoreBar.className = 'bg-emerald-600 h-3 rounded-full transition-all duration-300';
        } else if (!hasFatalBreach && totalScore >= 5) {
          card.className = 'lg:col-span-8 bg-white rounded-2xl p-6 sm:p-8 border-2 border-amber-500 shadow-sm transition-all flex flex-col justify-between';
          badge.className = 'badge-pill bg-amber-100 text-amber-800 text-xs py-1 px-3 mt-1 inline-block';
          badge.textContent = 'AMBER LIGHT: Conditional Co-Design';
          scoreBar.className = 'bg-amber-500 h-3 rounded-full transition-all duration-300';
        } else {
          card.className = 'lg:col-span-8 bg-white rounded-2xl p-6 sm:p-8 border-2 border-rose-600 shadow-sm transition-all flex flex-col justify-between';
          badge.className = 'badge-pill bg-rose-100 text-rose-800 text-xs py-1 px-3 mt-1 inline-block';
          badge.textContent = hasFatalBreach ? 'RED LIGHT: SMC Veto / Statutory Rejection' : 'RED LIGHT: High Risk of Abandonment';
          scoreBar.className = 'bg-rose-600 h-3 rounded-full transition-all duration-300';
        }
      }
    }

    function resetAuditForm() {
      const qNames = ['audit_q1','audit_q2','audit_q3','audit_q4','audit_q5','audit_q6','audit_q7','audit_q8','audit_q9','audit_q10','audit_q11'];
      qNames.forEach(name => {
        const radios = document.querySelectorAll(`input[name="${name}"]`);
        radios.forEach((r, idx) => {
          r.checked = (idx === 0);
        });
      });
      calculateAudit();
    }

    '''

new_html = html[:start] + new_audit_js + html[end:]
with open('/workspaces/CC_3/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Successfully injected Unified Dual-Stakeholder Gatekeeper JS into index.html!")
