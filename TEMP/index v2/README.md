# Vertical traceability dashboard (v2)

This is a separate dashboard; the existing root `index.html` is unchanged. The page links national and regional M-Lab measurements to a clearly labelled synthetic school-level placeholder panel.

## Run locally
From the repository root:
```
python3 -m http.server 8000
# open http://localhost:8000/TEMP/index%20v2/
```
The dashboard uses `out/dashboard/` for the M-Lab bundle and `TEMP/giga_synthetic/` for generated school placeholders. D3 is loaded from a pinned CDN, so the regional map needs an internet connection.

## How it is organised
- `registry.json`: levels, lenses, panels, gaps, tools, entry points, data paths, and limits text.
- `app.js`: spine (country, breadcrumb, level stepper, lens row, tools, data tag), three stacked bands, trace rail, methods.
- `panels/`: country-level snapshot and school-level synthetic demo modules.
- State lives in the query string (`?country=KEN&level=meso&lens=readiness&region=...`), so views are shareable; `#hash` is free for in-page anchors.
- `styles.css`: tokens. "Paper" (official/planned) = serif, italic, dashed, warm grey (`.is-paper`, `.mark-paper`). "Ground" (measured) = sans, tabular numbers, solid, teal (`.is-ground`, `.mark-ground`).

## Add or port a widget
1. Add an entry to `panels` in `registry.json` (`level`, `lenses` or `"all"`, `title`, `source`).
2. `kind: "stub"` while it is not ported. Then either:
   - `kind: "module"`: write `panels/my_widget.js` exporting `default function mount(host, ctx)`, or
   - `kind: "iframe"`: embed an existing standalone page as a stopgap (your own pages only).
3. A level/lens with no panel shows "Not measured yet"; add a `gaps` entry to say what would fill it.

## Data status
Create `data_status.json` next to the bundle (see `data_status.example.json`): `demo`, `none`, or `real`. If the file is missing the page shows "Demo data".

Synthetic records, generated with `make_synthetic_giga.py`, are for layout and plumbing tests only. Replace them with verified Giga data only after API access and schema validation; never interpret their values as real school conditions.
