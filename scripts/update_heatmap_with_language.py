import re
import json

with open('/workspaces/backup_final-thesis/data/processed/interactive_triangulation_heatmap.json') as f:
    heatmap_data = json.load(f)

json_str = json.dumps(heatmap_data, indent=2)

with open('/workspaces/backup_final-thesis/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the table header to include Language
old_thead = '''                  <th class="py-3 px-3 text-center">Governance Paradox<br><span class="text-[9px] font-sans font-normal text-slate-500">Edu Satisfaction vs School Grid</span></th>
                  <th class="py-3 px-3 text-center">Pillar 3: Cash Precarity<br><span class="text-[9px] font-sans font-normal text-slate-500">AB Lived Income Shortage</span></th>
                  <th class="py-3 px-3 text-center bg-slate-100">Layer 3: Practitioner<br><span class="text-[9px] font-sans font-normal text-slate-500">AoA Field Diagnostic</span></th>'''

new_thead = '''                  <th class="py-3 px-3 text-center">Pillar 5: Language &amp; AI<br><span class="text-[9px] font-sans font-normal text-slate-500">15% Supply vs Home Dialects</span></th>
                  <th class="py-3 px-3 text-center">Governance Paradox<br><span class="text-[9px] font-sans font-normal text-slate-500">Edu Satisfaction vs School Grid</span></th>
                  <th class="py-3 px-3 text-center">Pillar 3: Cash Precarity<br><span class="text-[9px] font-sans font-normal text-slate-500">AB Lived Income Shortage</span></th>
                  <th class="py-3 px-3 text-center bg-slate-100">Layer 3: Practitioner<br><span class="text-[9px] font-sans font-normal text-slate-500">AoA Field Diagnostic</span></th>'''

if old_thead in html:
    html = html.replace(old_thead, new_thead)

# Update the script section to inject the new dataset and linguistic column renderer
old_script_block = 'const heatmapData = '
pos = html.find('const heatmapData = ')
if pos != -1:
    end_script = html.find('</script>', pos)
    new_script_body = f"""const heatmapData = {json_str};

        function renderInteractiveHeatmap() {{
          const tbody = document.getElementById('interactive-heatmap-body');
          if (!tbody) return;
          tbody.innerHTML = '';

          heatmapData.forEach(c => {{
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-50/80 transition-colors border-b border-slate-100';

            let html = `
              <td class="py-3 px-4">
                <div class="font-bold text-slate-900 flex items-center gap-1.5">
                  <span class="text-base">${{c.flag}}</span> ${{c.name}}
                </div>
                <div class="text-[10px] text-slate-400 font-mono">${{c.sample_size_ab ? 'N=' + c.sample_size_ab.toLocaleString() + ' (AB R10)' : c.note}}</div>
              </td>
            `;

            function getCellHTML(dimKey, dim) {{
              if (!dim || (dim.gap === null && dim.field_val === null)) {{
                return `<td class="py-2.5 px-3 text-center text-slate-300 font-mono text-[11px]">—</td>`;
              }}
              if (dimKey === 'practitioner_audit') {{
                return `
                  <td class="py-2.5 px-3 text-center bg-slate-50">
                    <span onclick="selectHeatmapCell('${{c.iso3}}', '${{dimKey}}')" class="cursor-pointer inline-flex items-center gap-1 px-2 py-1 rounded bg-slate-200 text-slate-600 font-mono text-[10px] font-bold hover:bg-slate-300 transition">
                      <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                      Pending N
                    </span>
                  </td>
                `;
              }}
              if (dimKey === 'economic_precarity') {{
                const val = dim.field_val;
                const color = val > 80 ? 'bg-rose-100 text-rose-800 border-rose-200' : (val > 60 ? 'bg-amber-100 text-amber-800 border-amber-200' : 'bg-emerald-100 text-emerald-800 border-emerald-200');
                return `
                  <td class="py-2.5 px-3 text-center">
                    <button onclick="selectHeatmapCell('${{c.iso3}}', '${{dimKey}}')" class="px-2 py-1 rounded border font-mono font-bold text-[11px] ${{color}} hover:ring-2 hover:ring-indigo-400 transition">
                      ${{val}}%
                    </button>
                  </td>
                `;
              }}
              if (dimKey === 'linguistic') {{
                return `
                  <td class="py-2.5 px-3 text-center">
                    <button onclick="selectHeatmapCell('${{c.iso3}}', '${{dimKey}}')" class="px-2 py-1 rounded border font-mono text-[11px] bg-red-100 text-red-900 border-red-300 font-bold hover:ring-2 hover:ring-indigo-400 transition" title="Linguistic exclusion gap">
                      ${{dim.gap}}pp
                    </button>
                  </td>
                `;
              }}

              const gap = dim.gap;
              let bg = 'bg-slate-100 text-slate-700 border-slate-200';
              let sign = gap > 0 ? '+' : '';
              if (dimKey === 'electricity') {{
                if (gap < -15) bg = 'bg-rose-100 text-rose-900 border-rose-300 font-bold';
                else if (gap < -5) bg = 'bg-amber-100 text-amber-900 border-amber-300';
                else bg = 'bg-emerald-100 text-emerald-800 border-emerald-200';
              }} else if (dimKey === 'internet') {{
                if (Math.abs(gap) > 20) bg = 'bg-indigo-100 text-indigo-900 border-indigo-300 font-bold';
                else if (Math.abs(gap) > 10) bg = 'bg-amber-100 text-amber-800 border-amber-200';
                else bg = 'bg-emerald-100 text-emerald-800 border-emerald-200';
              }} else if (dimKey === 'gov_paradox') {{
                if (gap > 30) bg = 'bg-purple-100 text-purple-900 border-purple-300 font-bold';
                else if (gap > 15) bg = 'bg-blue-100 text-blue-900 border-blue-200';
                else bg = 'bg-slate-100 text-slate-700 border-slate-200';
              }} else if (dimKey === 'rural_grid') {{
                if (Math.abs(gap) > 20) bg = 'bg-orange-100 text-orange-900 border-orange-300';
                else bg = 'bg-slate-100 text-slate-700 border-slate-200';
              }}

              return `
                <td class="py-2.5 px-3 text-center">
                  <button onclick="selectHeatmapCell('${{c.iso3}}', '${{dimKey}}')" class="px-2 py-1 rounded border font-mono text-[11px] ${{bg}} hover:ring-2 hover:ring-indigo-400 transition" title="Click to view drilldown">
                    ${{sign}}${{gap}}pp
                  </button>
                </td>
              `;
            }}

            html += getCellHTML('electricity', c.dimensions.electricity);
            html += getCellHTML('rural_grid', c.dimensions.rural_grid);
            html += getCellHTML('internet', c.dimensions.internet);
            html += getCellHTML('linguistic', c.dimensions.linguistic);
            html += getCellHTML('gov_paradox', c.dimensions.gov_paradox);
            html += getCellHTML('economic_precarity', c.dimensions.economic_precarity);
            html += getCellHTML('practitioner_audit', c.dimensions.practitioner_audit);

            tr.innerHTML = html;
            tbody.appendChild(tr);
          }});
        }}

        function selectHeatmapCell(iso3, dimKey) {{
          const c = heatmapData.find(x => x.iso3 === iso3);
          if (!c) return;
          const dim = c.dimensions[dimKey];
          if (!dim) return;

          document.getElementById('drilldown-country').textContent = `${{c.flag}} ${{c.name}} (${{c.iso3}})`;
          document.getElementById('drilldown-badge').textContent = dim.name.toUpperCase();
          document.getElementById('drilldown-title').textContent = `${{c.name}}: ${{dim.name}} Divergence`;
          
          document.getElementById('drilldown-macro-val').textContent = dim.macro_val !== null ? `${{dim.macro_val}}${{dim.unit}}` : 'N/A';
          document.getElementById('drilldown-macro-src').textContent = dim.macro_src || '—';

          document.getElementById('drilldown-field-val').textContent = dim.field_val !== null ? `${{dim.field_val}}${{dim.unit}}` : 'Pending Field Data';
          document.getElementById('drilldown-field-src').textContent = dim.field_src || '—';

          const gapText = dim.gap !== null ? (dim.gap > 0 ? `+${{dim.gap}}pp Gap` : `${{dim.gap}}pp Gap`) : (dimKey === 'economic_precarity' ? `${{dim.field_val}}% Stress Rate` : 'Awaiting Collection');
          document.getElementById('drilldown-gap-val').textContent = gapText;
          document.getElementById('drilldown-desc').textContent = dim.desc || '';

          const card = document.getElementById('heatmap-drilldown-card');
          card.classList.add('ring-2', 'ring-indigo-500');
          setTimeout(() => card.classList.remove('ring-2', 'ring-indigo-500'), 800);
        }}

        document.addEventListener('DOMContentLoaded', () => {{
          renderInteractiveHeatmap();
        }});
        if (document.readyState === 'complete' || document.readyState === 'interactive') {{
          renderInteractiveHeatmap();
        }}
"""
    html = html[:pos] + new_script_body + html[end_script:]

with open('/workspaces/backup_final-thesis/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html with language and AI token tax column in interactive heatmap!")
