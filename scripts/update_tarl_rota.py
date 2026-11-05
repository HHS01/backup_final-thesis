import sys

with open('/workspaces/CC_3/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_marker = '      // 4. Weekly Rota Generator (Station-of-the-Day Mon-Fri)\n      const weeklyTbody = document.getElementById(\'weekly-rota-tbody\');\n      if (weeklyTbody) {\n        const days = ['

pos = html.find(target_marker)
if pos == -1:
    print("Could not find target_marker")
    sys.exit(1)

end_marker = '        weeklyTbody.innerHTML = days.map(d => `'
end_pos = html.find(end_marker, pos)
if end_pos == -1:
    print("Could not find end_marker")
    sys.exit(1)

# Replacement for the days array:
new_days = '''      // 4. Weekly Rota Generator: Aligned with Teaching at the Right Level (TaRL / PAL Network / Tusome)
      // Rotates student cohort device access across the standard daily statutory subject period
      const weeklyTbody = document.getElementById('weekly-rota-tbody');
      if (weeklyTbody) {
        const days = [
          { 
            day: 'Monday', 
            focus: 'Cohort A Priority', 
            s1: `Cohort A (${cohortA})`, 
            s2: `Cohort B (${cohortB})`, 
            s3: `Cohort C (${cohortC})`, 
            anchor: 'Decodables & Number Drills',
            s1Note: currentPedagogyMode === 'solar_radio' ? 'Solar Radio Broadcast' : 'Interactive Tablets',
            s2Note: 'Syllabus Workbook Tasks',
            s3Note: 'Direct Phonics Coaching'
          },
          { 
            day: 'Tuesday', 
            focus: 'Cohort B Priority', 
            s1: `Cohort B (${cohortB})`, 
            s2: `Cohort C (${cohortC})`, 
            s3: `Cohort A (${cohortA})`, 
            anchor: 'Sentence & Math Practice',
            s1Note: currentPedagogyMode === 'solar_radio' ? 'Solar Radio Broadcast' : 'Interactive Tablets',
            s2Note: 'Syllabus Workbook Tasks',
            s3Note: 'Direct Numeracy Coaching'
          },
          { 
            day: 'Wednesday', 
            focus: 'Cohort C Priority', 
            s1: `Cohort C (${cohortC})`, 
            s2: `Cohort A (${cohortA})`, 
            s3: `Cohort B (${cohortB})`, 
            anchor: 'Comprehension & Problem Solving',
            s1Note: currentPedagogyMode === 'solar_radio' ? 'Solar Radio Broadcast' : 'Interactive Tablets',
            s2Note: 'Syllabus Workbook Tasks',
            s3Note: 'Mother-Tongue Fluency'
          },
          { 
            day: 'Thursday', 
            focus: 'Targeted Remediation', 
            s1: `Identified Struggling Learners (${Math.min(digitalSeats, maxCohort)})`, 
            s2: `Independent Practice (${Math.max(0, N - digitalSeats - cohortC)})`, 
            s3: `Micro-Group Remediation (${cohortC})`, 
            anchor: 'Formative Catch-Up Clinic',
            s1Note: 'Guided Practice Software',
            s2Note: 'Peer Pair Review & Scribes',
            s3Note: 'Intensive Diagnostic Check'
          },
          { 
            day: 'Friday', 
            focus: 'Synthesis & Maintenance', 
            s1: `Rapid Relay / Listening Circle (${Math.ceil(N / 2)})`, 
            s2: `Whole-Class Oral Check (${Math.floor(N / 2)})`, 
            s3: `Teacher Exit Tickets & Wrap`, 
            anchor: 'Weekly Exit Check & Solar Recharge',
            s1Note: 'Battery / Solar Top-up & Audio',
            s2Note: 'Slate / Blackboard Sharing',
            s3Note: 'Parent Note / Progress Log'
          }
        ];
'''

# Update the rendering template below it to use s1Note, s2Note, s3Note:
render_start = html.find('        weeklyTbody.innerHTML = days.map(d => `', pos)
render_end = html.find('        `).join(\'\');\n      }', render_start) + len('        `).join(\'\');\n      }')

new_render = '''        weeklyTbody.innerHTML = days.map(d => `
          <tr class="hover:bg-stone-50 transition">
            <td class="p-2.5 font-bold text-stone-900 whitespace-nowrap">
              <span>${d.day}</span>
              <span class="block text-[10px] font-normal text-purple-700 font-semibold">${d.focus}</span>
            </td>
            <td class="p-2.5 text-blue-900 font-medium">
              <span class="px-1.5 py-0.5 rounded bg-blue-50 border border-blue-200 text-blue-800 font-bold">${d.s1}</span>
              <span class="block text-[10px] text-stone-500 mt-0.5">${d.s1Note}</span>
            </td>
            <td class="p-2.5 text-amber-900 font-medium">
              <span class="px-1.5 py-0.5 rounded bg-amber-50 border border-amber-200 text-amber-800 font-bold">${d.s2}</span>
              <span class="block text-[10px] text-stone-500 mt-0.5">${d.s2Note}</span>
            </td>
            <td class="p-2.5 text-emerald-900 font-medium">
              <span class="px-1.5 py-0.5 rounded bg-emerald-50 border border-emerald-200 text-emerald-800 font-bold">${d.s3}</span>
              <span class="block text-[10px] text-stone-500 mt-0.5">${d.s3Note}</span>
            </td>
            <td class="p-2.5 text-center whitespace-nowrap">
              <span class="badge-pill bg-stone-100 text-stone-700 font-mono text-[11px]">${d.anchor}</span>
            </td>
          </tr>
        `).join('');
      }'''

updated_html = html[:pos] + new_days + new_render + html[render_end:]

with open('/workspaces/CC_3/index.html', 'w', encoding='utf-8') as f:
    f.write(updated_html)

print("Successfully replaced Weekly Rota logic with peer-reviewed TaRL model!")
