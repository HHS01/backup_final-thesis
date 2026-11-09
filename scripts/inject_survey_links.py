with open('/workspaces/backup_final-thesis/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add an anchor point and quick survey launch buttons
if 'id="survey-portal-anchor"' not in html:
    html = html.replace(
        '<div class="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm mb-8" id="triangulation-heatmap-section">',
        '<div id="survey-portal-anchor"></div>\n        <div class="bg-white rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm mb-8" id="triangulation-heatmap-section">'
    )
    # Update link in heatmap
    html = html.replace('href="#survey-portal-anchor"', 'href="./Teacher_Diagnostic_Survey.html" target="_blank"')

with open('/workspaces/backup_final-thesis/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated survey navigation links in index.html!")
