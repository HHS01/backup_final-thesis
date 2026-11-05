import sys

with open('/workspaces/CC_3/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '// =================================================================\n    // TOOL 2: DYNAMIC CLASS CROWDING & ROTATION PLANNER'
end_marker = '// =================================================================\n    // TOOL 3: VETTED LIVING DPG DIRECTORY RENDERER'

start = html.find(start_marker)
end = html.find(end_marker)

if start == -1 or end == -1:
    print(f"Error: markers not found (start={start}, end={end})")
    sys.exit(1)

upgraded_js = '''// =================================================================
    // TOOL 2: DYNAMIC CLASS CROWDING & ROTATION PLANNER (UPGRADED)
    // Modes: standard | relay | solar_radio
    // Views: single | weekly
    // =================================================================
    let pairingMode = 2; // 2 = Paired learning (default), 1 = Solo
    let currentPedagogyMode = 'standard'; // 'standard' | 'relay' | 'solar_radio'
    let currentRotaView = 'single'; // 'single' | 'weekly'

    function setPedagogyMode(mode) {
      currentPedagogyMode = mode;
      const btnStandard = document.getElementById('btn-pedagogy-standard');
      const btnRelay = document.getElementById('btn-pedagogy-relay');
      const btnSolar = document.getElementById('btn-pedagogy-solar');
      const pairingContainer = document.getElementById('pairing-mode-container');

      [btnStandard, btnRelay, btnSolar].forEach(btn => {
        if (!btn) return;
        btn.className = 'py-2 px-2.5 rounded-lg border font-medium text-left sm:text-center transition bg-white border-stone-200 text-stone-600 hover:bg-stone-50';
      });

      if (mode === 'standard' && btnStandard) {
        btnStandard.className = 'py-2 px-2.5 rounded-lg border font-bold text-left sm:text-center transition bg-emerald-50 border-emerald-600 text-emerald-800';
        if (pairingContainer) pairingContainer.classList.remove('hidden');
      } else if (mode === 'relay' && btnRelay) {
        btnRelay.className = 'py-2 px-2.5 rounded-lg border font-bold text-left sm:text-center transition bg-emerald-50 border-emerald-600 text-emerald-800';
        if (pairingContainer) pairingContainer.classList.remove('hidden');
      } else if (mode === 'solar_radio' && btnSolar) {
        btnSolar.className = 'py-2 px-2.5 rounded-lg border font-bold text-left sm:text-center transition bg-emerald-50 border-emerald-600 text-emerald-800';
        if (pairingContainer) pairingContainer.classList.add('hidden');
      }

      updateRotationPlanner();
    }

    function setRotaView(view) {
      currentRotaView = view;
      const btnSingle = document.getElementById('btn-view-single');
      const btnWeekly = document.getElementById('btn-view-weekly');
      const singleView = document.getElementById('planner-single-view');
      const weeklyView = document.getElementById('planner-weekly-view');

      if (view === 'single') {
        if (btnSingle) btnSingle.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-stone-900 text-white shadow-sm transition';
        if (btnWeekly) btnWeekly.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-white border border-stone-200 text-stone-700 hover:bg-stone-50 transition flex items-center gap-1.5';
        if (singleView) singleView.classList.remove('hidden');
        if (weeklyView) weeklyView.classList.add('hidden');
      } else {
        if (btnWeekly) btnWeekly.className = 'px-3 py-1.5 rounded-lg text-xs font-bold bg-purple-900 text-white shadow-sm transition flex items-center gap-1.5';
        if (btnSingle) btnSingle.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-white border border-stone-200 text-stone-700 hover:bg-stone-50 transition';
        if (weeklyView) weeklyView.classList.remove('hidden');
        if (singleView) singleView.classList.add('hidden');
      }
      updateRotationPlanner();
    }

    function setPairingMode(mode) {
      pairingMode = mode;
      const btnPair = document.getElementById('btn-mode-pair');
      const btnSolo = document.getElementById('btn-mode-solo');
      if (mode === 2) {
        btnPair.className = 'py-2 px-3 rounded-lg border font-bold text-center transition bg-emerald-50 border-emerald-600 text-emerald-800';
        btnSolo.className = 'py-2 px-3 rounded-lg border font-medium text-center transition bg-white border-stone-200 text-stone-600 hover:bg-stone-50';
      } else {
        btnSolo.className = 'py-2 px-3 rounded-lg border font-bold text-center transition bg-emerald-50 border-emerald-600 text-emerald-800';
        btnPair.className = 'py-2 px-3 rounded-lg border font-medium text-center transition bg-white border-stone-200 text-stone-600 hover:bg-stone-50';
      }
      updateRotationPlanner();
    }

    function updateRotationPlanner() {
      const N = parseInt(document.getElementById('input-students').value) || 50;
      const D = parseInt(document.getElementById('input-devices').value) || 5;
      const T = parseInt(document.getElementById('input-minutes').value) || 45;

      document.getElementById('slider-val-students').textContent = N + ' Pupils';
      document.getElementById('slider-val-devices').textContent = D + (currentPedagogyMode === 'solar_radio' ? ' Radios / Audio Kits' : ' Tablets');
      document.getElementById('slider-val-minutes').textContent = T + ' Minutes';

      // 1. Precise 3-Cohort Balancing
      const cohortA = Math.ceil(N / 3);
      const cohortB = Math.round((N - cohortA) / 2);
      const cohortC = N - cohortA - cohortB;
      const maxCohort = Math.max(cohortA, cohortB, cohortC);

      // 2. Capacity & Deficit / Coverage Calculation
      let digitalSeats = D * pairingMode;
      if (currentPedagogyMode === 'solar_radio') {
        digitalSeats = D * 8; // A single solar radio or audio hub easily serves 6-8 students in a focused cluster
      }

      const ratio = (N / D).toFixed(1);
      const ratioBadge = document.getElementById('calc-ratio-badge');
      if (ratioBadge) {
        if (currentPedagogyMode === 'solar_radio') {
          ratioBadge.className = 'badge-pill bg-purple-100 text-purple-800 font-mono text-xs';
          ratioBadge.textContent = `Solar Audio: ${D} Unit(s) covers ~${Math.min(cohortA, digitalSeats)} / ${cohortA} in Listening Cohort`;
        } else if (currentPedagogyMode === 'relay') {
          ratioBadge.className = 'badge-pill bg-blue-100 text-blue-800 font-mono text-xs';
          ratioBadge.textContent = `Relay Cadence: ${D} Shared Device(s) passing in ${Math.max(4, Math.floor((T - 10) / 6))}m micro-shifts`;
        } else {
          if (digitalSeats >= maxCohort) {
            ratioBadge.className = 'badge-pill bg-emerald-100 text-emerald-800 font-mono text-xs';
            ratioBadge.textContent = `Ratio ${ratio}:1 • 100% Covered (${pairingMode === 2 ? 'Paired' : 'Solo'})`;
          } else {
            const deficit = maxCohort - digitalSeats;
            ratioBadge.className = 'badge-pill bg-amber-100 text-amber-800 font-mono text-xs';
            ratioBadge.textContent = `Ratio ${ratio}:1 • Deficit: ${deficit} Scribes (${pairingMode === 2 ? 'Paired' : 'Solo'})`;
          }
        }
      }

      // Station Card Titles & Styling
      const cardS1 = document.getElementById('card-station1');
      const cardS2 = document.getElementById('card-station2');
      const cardS3 = document.getElementById('card-station3');
      const s1Title = document.getElementById('station1-title');
      const s2Title = document.getElementById('station2-title');
      const s3Title = document.getElementById('station3-title');
      const s1Summary = document.getElementById('station1-summary');
      const s2Summary = document.getElementById('station2-summary');
      const s3Summary = document.getElementById('station3-summary');
      const footerNote = document.getElementById('pedagogy-footer-note');

      if (currentPedagogyMode === 'solar_radio') {
        if (s1Title) s1Title.innerHTML = '📻 Station 1: Solar Audio / Broadcast Hub';
        if (s2Title) s2Title.innerHTML = '📝 Station 2: Active Guided Note-Taking';
        if (s3Title) s3Title.innerHTML = '👩‍🏫 Station 3: Teacher Direct Synthesis';
        if (s1Summary) s1Summary.textContent = `${cohortA} pupils clustered around ${D} solar/battery audio player(s) listening to vetted curriculum radio broadcast (e.g. Ubongo Kids or Taifa Radio).`;
        if (s2Summary) s2Summary.textContent = `${cohortB} pupils completing structured comprehension workbooks linked to audio broadcast topics.`;
        if (s3Summary) s3Summary.textContent = `${cohortC} pupils working directly with teacher for pronunciation check, vocabulary interrogation, and formative oral checks.`;
        if (footerNote) footerNote.textContent = 'Broadcast Protocol: Zero cellular/airtime burden; resilient to electrical grid outages.';
      } else if (currentPedagogyMode === 'relay') {
        if (s1Title) s1Title.innerHTML = '🏃 Station 1: Device Relay & Timed Task';
        if (s2Title) s2Title.innerHTML = '🤝 Station 2: Peer Review & Scribe Team';
        if (s3Title) s3Title.innerHTML = '👩‍🏫 Station 3: Teacher Remediation & Diagnostic';
        if (s1Summary) s1Summary.textContent = `${D} devices cycle through student pairs within Cohort A (${cohortA} pupils) every ${Math.max(4, Math.floor((T - 10) / 6))} minutes for rapid drill/interactive quiz tasks.`;
        if (s2Summary) s2Summary.textContent = `${cohortB} pupils working in pairs verifying math steps or sentence writing before receiving next device relay.`;
        if (s3Summary) s3Summary.textContent = `${cohortC} pupils receiving intensive teacher phonics or foundational numeracy coaching.`;
        if (footerNote) footerNote.textContent = 'Device Relay Protocol: Passing physical hardware at timed intervals solves extreme hardware shortages.';
      } else {
        if (s1Title) s1Title.innerHTML = '💻 Station 1: Digital Lab';
        if (s2Title) s2Title.innerHTML = '👥 Station 2: Collaborative Small Groups';
        if (s3Title) s3Title.innerHTML = '👩‍🏫 Station 3: Teacher Direct Focus';
        if (s1Summary) {
          if (digitalSeats >= cohortA) {
            s1Summary.textContent = `${cohortA} pupils (${pairingMode === 2 ? Math.ceil(cohortA / 2) + ' pairs' : cohortA + ' solo'}) completing interactive digital learning modules.`;
          } else {
            const seated = digitalSeats;
            const scribes = cohortA - seated;
            s1Summary.textContent = `${seated} pupils on tablets + ${scribes} peer scribes/recorders in 3-student trios.`;
          }
        }
        if (s2Summary) s2Summary.textContent = `${cohortB} pupils in small peer groups solving syllabus workbook problems.`;
        if (s3Summary) s3Summary.textContent = `${cohortC} pupils working directly with the teacher for literacy remediation & phonics.`;
        if (footerNote) footerNote.textContent = 'Standard Rotation: Balanced 3-cohort synchronous cycle with zero pupil idle time.';
      }

      // 3. Timetable Timing Calculation (5m Priming + 3 equal rotations + 5m Synthesis)
      const usableTime = T - 10;
      const timePerRotation = Math.max(6, Math.floor(usableTime / 3));

      // Timetable generation
      const slotsContainer = document.getElementById('timetable-slots');
      let html = '';

      let curMin = 0;
      html += `
        <div class="flex items-center gap-3 p-2.5 rounded-lg bg-stone-100 border border-stone-200">
          <span class="font-mono font-bold text-stone-700 w-16">00–05m</span>
          <span class="font-semibold text-stone-800">Whole-Class Priming:</span>
          <span class="text-stone-600">Teacher introduces lesson concept and assigns Cohort A (${cohortA}), Cohort B (${cohortB}), and Cohort C (${cohortC}).</span>
        </div>
      `;
      curMin = 5;

      const rotations = [
        { rot: 1, s1: `Cohort A (${cohortA})`, s2: `Cohort B (${cohortB})`, s3: `Cohort C (${cohortC})` },
        { rot: 2, s1: `Cohort C (${cohortC})`, s2: `Cohort A (${cohortA})`, s3: `Cohort B (${cohortB})` },
        { rot: 3, s1: `Cohort B (${cohortB})`, s2: `Cohort C (${cohortC})`, s3: `Cohort A (${cohortA})` }
      ];

      const s1Label = currentPedagogyMode === 'solar_radio' ? 'Solar Audio Post' : (currentPedagogyMode === 'relay' ? 'Device Relay' : 'Tablets');
      const s2Label = currentPedagogyMode === 'solar_radio' ? 'Comprehension Sheet' : 'Workbook';
      const s3Label = 'Teacher Direct Focus';

      rotations.forEach(r => {
        const nextMin = curMin + timePerRotation;
        html += `
          <div class="flex flex-wrap items-center justify-between p-2.5 rounded-lg bg-emerald-50/50 border border-emerald-200/80">
            <div class="flex items-center gap-2">
              <span class="font-mono font-bold text-emerald-800 w-16">${String(curMin).padStart(2, '0')}–${String(nextMin).padStart(2, '0')}m</span>
              <span class="font-bold text-stone-900">Rotation ${r.rot} (${timePerRotation} mins):</span>
            </div>
            <div class="flex items-center gap-2 text-[11px] mt-1 sm:mt-0">
              <span class="px-2 py-0.5 rounded bg-blue-100 text-blue-800 font-semibold">${r.s1} · ${s1Label}</span>
              <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-semibold">${r.s2} · ${s2Label}</span>
              <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-semibold">${r.s3} · ${s3Label}</span>
            </div>
          </div>
        `;
        curMin = nextMin;
      });

      html += `
        <div class="flex items-center gap-3 p-2.5 rounded-lg bg-stone-100 border border-stone-200">
          <span class="font-mono font-bold text-stone-700 w-16">${String(curMin).padStart(2, '0')}–${String(T).padStart(2, '0')}m</span>
          <span class="font-semibold text-stone-800">Whole-Class Synthesis:</span>
          <span class="text-stone-600">${T - curMin}-minute oral reflection, peer exit tickets, and homework prompt.</span>
        </div>
      `;

      if (slotsContainer) slotsContainer.innerHTML = html;

      // 4. Weekly Rota Generator (Station-of-the-Day Mon-Fri)
      const weeklyTbody = document.getElementById('weekly-rota-tbody');
      if (weeklyTbody) {
        const days = [
          { day: 'Monday', focus: 'Foundational Literacy', s1: `Cohort A (${cohortA})`, s2: `Cohort B (${cohortB})`, s3: `Cohort C (${cohortC})`, anchor: 'Phonics & Decodables' },
          { day: 'Tuesday', focus: 'Numeracy & Calculations', s1: `Cohort B (${cohortB})`, s2: `Cohort C (${cohortC})`, s3: `Cohort A (${cohortA})`, anchor: 'Mental Math & Drills' },
          { day: 'Wednesday', focus: 'Mother-Tongue / Local Context', s1: `Cohort C (${cohortC})`, s2: `Cohort A (${cohortA})`, s3: `Cohort B (${cohortB})`, anchor: 'Storytelling & Fluency' },
          { day: 'Thursday', focus: 'STEM & Science Curiosity', s1: `Cohort A (${cohortA})`, s2: `Cohort B (${cohortB})`, s3: `Cohort C (${cohortC})`, anchor: 'Simulations / Practical' },
          { day: 'Friday', focus: 'Formative Review & Assessment', s1: `Cohort B + C (Relay)`, s2: `All Cohorts (Peer Review)`, s3: `Cohort A + Remediation`, anchor: 'Weekly Mastery Check' }
        ];

        weeklyTbody.innerHTML = days.map(d => `
          <tr class="hover:bg-stone-50 transition">
            <td class="p-2.5 font-bold text-stone-900 whitespace-nowrap">
              <span>${d.day}</span>
              <span class="block text-[10px] font-normal text-stone-500">${d.focus}</span>
            </td>
            <td class="p-2.5 text-blue-900 font-medium">
              <span class="px-1.5 py-0.5 rounded bg-blue-50 border border-blue-200 text-blue-800 font-bold">${d.s1}</span>
              <span class="block text-[10px] text-stone-500 mt-0.5">${currentPedagogyMode === 'solar_radio' ? 'Radio Lesson Segment' : 'Digital Station'}</span>
            </td>
            <td class="p-2.5 text-amber-900 font-medium">
              <span class="px-1.5 py-0.5 rounded bg-amber-50 border border-amber-200 text-amber-800 font-bold">${d.s2}</span>
              <span class="block text-[10px] text-stone-500 mt-0.5">Peer Exercises</span>
            </td>
            <td class="p-2.5 text-emerald-900 font-medium">
              <span class="px-1.5 py-0.5 rounded bg-emerald-50 border border-emerald-200 text-emerald-800 font-bold">${d.s3}</span>
              <span class="block text-[10px] text-stone-500 mt-0.5">Teacher Coaching</span>
            </td>
            <td class="p-2.5 text-center whitespace-nowrap">
              <span class="badge-pill bg-stone-100 text-stone-700 font-mono text-[11px]">${d.anchor}</span>
            </td>
          </tr>
        `).join('');
      }

      // Update print meta elements
      const printMeta = document.getElementById('planner-print-meta');
      if (printMeta) {
        printMeta.textContent = `${N} Pupils • ${D} ${currentPedagogyMode === 'solar_radio' ? 'Audio Units' : 'Devices'} (${ratio}:1 ratio) • ${T} Mins • Mode: ${currentPedagogyMode.toUpperCase()} • View: ${currentRotaView.toUpperCase()}`;
      }
    }

    function printPlannerTimetable() {
      document.body.classList.add('print-mode-planner');
      window.print();
    }
    window.addEventListener('afterprint', () => {
      document.body.classList.remove('print-mode-planner');
    });

    '''

new_html = html[:start] + upgraded_js + html[end:]
with open('/workspaces/CC_3/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Successfully injected upgraded Rotation Planner JS into index.html!")
