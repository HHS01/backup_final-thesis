/*
 * admin1_explorer.js  -  regional (admin-1) map + time series for your dashboard.
 * Framework-agnostic ES module; needs d3 v7 (global `d3`, or pass opts.d3).
 *
 *   import { mountAdmin1Explorer } from "./admin1_explorer.js";
 *   const api = await mountAdmin1Explorer(document.getElementById("conn-map"), {
 *     baseUrl: "/data/dashboard/",          // folder written by build_dashboard_data.py
 *     country: "KEN",                       // optional start country
 *     metric: "download_p50",               // optional start metric
 *     onSelect: (r) => myDashboard.filterTo(r.iso3, r.shapeId),   // hook other panels in here
 *     // for deep links / shared state, spread createExplorerLink(state).options here (see dashboard_state.js)
 *   });
 *   // api.setCountry("GHA"); api.setMetric("download_p50", "layer:literacy"); api.select(shapeId); api.destroy();
 *
 * In React/Vue: call mountAdmin1Explorer inside an effect/onMounted on a ref'd <div>, call api.destroy() on cleanup.
 * Access control is your dashboard's job: serve the bundle folder from behind the same login as the page.
 *
 * Pick a second metric for a bivariate map (e.g. need x connectivity). Darker = higher value.
 * Hatched = few tests (unreliable). Grey = no usable data / not matched with confidence.
 */
const PAL = ["#eff3ff", "#bdd7e7", "#6baed6", "#3182bd", "#08519c"];
// 3x3 bivariate, index = yClass*3 + xClass (x: left->right, y: bottom->top)
const BI = ["#e8e8e8", "#ace4e4", "#5ac8c8", "#dfb0d6", "#a5add3", "#5698b9", "#be64ac", "#8c62aa", "#3b4994"];
const GREY = "#d9d9d9";
const SINCE_LABEL = { "3m": "3 months ago", "6m": "6 months ago", "12m": "a year ago" };
const CHG_COL = { improved: "#1D9E75", worsened: "#D85A30", neutral: "#5F5E5A" };
const MAX_MARKS = 8;
const CSS = `
.a1x{font:14px/1.4 system-ui,sans-serif;color:#1f2933}
.a1x-controls{display:flex;flex-wrap:wrap;gap:.75rem;align-items:end;margin-bottom:.75rem}
.a1x-controls label{display:flex;flex-direction:column;font-size:12px;color:#52606d}
.a1x-controls select,.a1x-controls input{font:inherit;padding:.35rem .5rem;border:1px solid #cbd5e1;border-radius:6px;background:#fff}
.a1x-body{display:flex;flex-wrap:wrap;gap:1rem}
.a1x-map{flex:2 1 360px;min-width:300px}.a1x-side{flex:1 1 240px;min-width:220px}
.a1x-map svg{width:100%;height:auto;min-height:360px;background:#f8fafc;border-radius:8px;border:1px solid #e2e8f0}
.a1x-map path{stroke:#94a3b8;stroke-width:.6;cursor:pointer;transition:stroke .15s,filter .15s}
.a1x-map path:hover{stroke:#0f172a;stroke-width:1.5;filter:brightness(0.93)}
.a1x-map path.sel{stroke:#0284c7;stroke-width:2.5;filter:drop-shadow(0 2px 4px rgba(0,0,0,0.25))}
.a1x-legend{display:flex;gap:2px;align-items:center;margin:.5rem 0;font-size:12px}
.a1x-legend i{display:inline-block;width:26px;height:10px}
.a1x-bi{display:grid;grid-template-columns:repeat(3,18px);gap:1px;margin:.5rem 0}.a1x-bi i{width:18px;height:18px}
.a1x-panel h3{margin:.2rem 0}.a1x-muted{color:#52606d;font-size:12px}.a1x-warn{color:#8a4b00;font-size:12px}
.a1x-foot{margin-top:.75rem;font-size:11px;color:#52606d}
`;

export async function mountAdmin1Explorer(el, opts = {}) {
  const d3 = opts.d3 || globalThis.d3;
  if (!d3) throw new Error("d3 v7 is required (load it globally or pass opts.d3)");
  const base = (opts.baseUrl || "./").replace(/\/?$/, "/");
  const getJson = opts.fetchJson || ((u) => fetch(u).then((r) => { if (!r.ok) throw new Error(`${u}: HTTP ${r.status}`); return r.json(); }));
  const doc = el.ownerDocument;
  if (!doc.getElementById("a1x-css")) {
    const s = doc.createElement("style"); s.id = "a1x-css"; s.textContent = CSS; doc.head.appendChild(s);
  }

  const manifest = await getJson(base + "manifest.json");
  const M = Object.fromEntries(manifest.metrics.map((m) => [m.id, m]));
  const cache = {};
  const st = { country: manifest.countries.some((c) => c.iso3 === opts.country) ? opts.country : manifest.countries[0]?.iso3,
               m1: M[opts.metric] ? opts.metric : manifest.metrics[0]?.id,
               m2: M[opts.metric2] && opts.metric2 !== opts.metric ? opts.metric2 : null, t: 0, sel: null, data: null,
               since: ["3m", "6m", "12m"].includes(opts.since) ? opts.since : null, showAll: false };
  let pendingPeriod = opts.period || null;

  const root = d3.select(el).html("").classed("a1x", true);
  const controls = root.append("div").attr("class", "a1x-controls");
  const body = root.append("div").attr("class", "a1x-body");
  const mapBox = body.append("div").attr("class", "a1x-map");
  const side = body.append("div").attr("class", "a1x-side");
  const panel = side.append("div").attr("class", "a1x-panel");
  const foot = root.append("div").attr("class", "a1x-foot");

  const field = (label, node) => { const l = controls.append("label"); l.append("span").text(label); return l.append(node); };
  const selCountry = field("Country", "select");
  selCountry.selectAll("option").data(manifest.countries).join("option")
    .attr("value", (c) => c.iso3).text((c) => c.name);
  const metricOptions = (sel, withNone) => {
    if (withNone) sel.append("option").attr("value", "").text("None (single map)");
    const kinds = d3.group(manifest.metrics, (m) => m.kind || "other");
    for (const [k, ms] of kinds) sel.append("optgroup").attr("label", k)
      .selectAll("option").data(ms).join("option").attr("value", (m) => m.id).text((m) => m.label);
  };
  const selM1 = field("Show", "select"); metricOptions(selM1, false);
  const selM2 = field("Compare with", "select"); metricOptions(selM2, true);
  const selSince = field("Highlight changes", "select");
  const slider = field("Month", "input").attr("type", "range").attr("min", 0).attr("value", 0);
  const tLabel = controls.append("span").attr("class", "a1x-muted");

  foot.html(
    `<div>${manifest.caveats.map((c) => `<div>• ${c}</div>`).join("")}</div>` +
    `<div style="margin-top:.4rem">${manifest.attribution.join(" ")} Built ${manifest.built.slice(0, 10)}.</div>`);

  const val = (sh, id, i) => { const a = sh.metrics[id]; return !a ? null : a.length === 1 ? a[0] : (a[i] ?? null); };
  const low = (sh, id, i) => { const s = M[id]?.source; return !!(s && sh.low[s] && sh.low[s][i]); };
  const allVals = (id) => Object.values(st.data.series.shapes).flatMap((sh) => (sh.metrics[id] || []).filter((v) => v != null));
  const fmt = (id, v) => v == null ? "no data" : `${v.toFixed(M[id]?.decimals ?? 1)} ${M[id]?.unit || ""}`.trim();

  const changeRecs = () => (st.since && st.data.changes ? (st.data.changes.since[st.since] || []) : []).filter((r) => r.metric === st.m1);
  const per = (p) => (p[0] === p[1] ? p[0] : `${p[0]} to ${p[1]}`);
  function sentence(r) {   // every number comes from the record; nothing is invented here
    const m = M[r.metric] || { label: r.metric };
    if (r.type === "new") return `${m.label}: usable data appeared (${per(r.toPeriods)}); there was none in ${per(r.fromPeriods)}.`;
    if (r.type === "missing") return `${m.label}: ` + (r.reason === "too_few_tests"
      ? `too few tests to report in ${per(r.toPeriods)}.` : `no data in ${per(r.toPeriods)}; there was in ${per(r.fromPeriods)}.`);
    return `${m.label} ${r.direction === "down" ? "fell" : "rose"} from ${fmt(r.metric, r.from)} to ${fmt(r.metric, r.to)} ` +
      `(average of ${per(r.toPeriods)} vs ${per(r.fromPeriods)}). Before the change its monthly values typically stayed ` +
      `between ${fmt(r.metric, r.usual[0])} and ${fmt(r.metric, r.usual[1])}. It is a measured change, not an explanation.`;
  }
  const glyph = (r) => (r.type === "new" ? "+" : r.type === "missing" ? "–" : r.direction === "up" ? "↑" : "↓");

  function rewindGeo(geo) {
    if (!geo || !geo.features) return;
    for (const f of geo.features) {
      if (!f.geometry) continue;
      if (d3.geoArea(f) > 2 * Math.PI) {
        if (f.geometry.type === "Polygon") {
          f.geometry.coordinates.forEach(r => r.reverse());
        } else if (f.geometry.type === "MultiPolygon") {
          f.geometry.coordinates.forEach(poly => poly.forEach(r => r.reverse()));
        }
      }
    }
  }

  async function load(iso3) {
    if (!cache[iso3]) {
      const [geo, series, changes] = await Promise.all([getJson(`${base}${iso3}.geojson`), getJson(`${base}${iso3}.series.json`),
        getJson(`${base}${iso3}.changes.json`).catch(() => null)]);   // changes file is optional
      rewindGeo(geo);
      cache[iso3] = { geo, series, changes };
    }
    st.data = cache[iso3];
  }

  function colourFn() {
    const sh = st.data.series.shapes;
    const v1 = allVals(st.m1);
    if (!st.m2) {
      const q = d3.scaleQuantize().domain(d3.extent(v1)).range(PAL);
      return { fn: (s, i) => { const v = val(s, st.m1, i); return v == null ? GREY : q(v); }, q };
    }
    const terc = (v) => { const a = v.slice().sort(d3.ascending); return [d3.quantile(a, 1 / 3), d3.quantile(a, 2 / 3)]; };
    const t1 = terc(v1), t2 = terc(allVals(st.m2));
    const cls = (v, t) => (v < t[0] ? 0 : v < t[1] ? 1 : 2);
    return { fn: (s, i) => {
      const a = val(s, st.m1, i), b = val(s, st.m2, i);
      return a == null || b == null ? GREY : BI[cls(b, t2) * 3 + cls(a, t1)];
    }, bi: true, sh };
  }

  function legend(c) {
    const box = mapBox.selectAll(".a1x-lg").data([0]).join("div").attr("class", "a1x-lg").html("");
    if (c.bi) {
      box.append("div").attr("class", "a1x-muted")
        .text(`→ ${M[st.m1].label} (low to high)    ↑ ${M[st.m2].label} (low to high)`);
      const g = box.append("div").attr("class", "a1x-bi");
      for (let y = 2; y >= 0; y--) for (let x = 0; x < 3; x++) g.append("i").style("background", BI[y * 3 + x]);
    } else {
      const [lo, hi] = c.q.domain();
      const row = box.append("div").attr("class", "a1x-legend");
      row.append("span").text(fmt(st.m1, lo));
      PAL.forEach((p) => row.append("i").style("background", p));
      row.append("span").text(fmt(st.m1, hi));
    }
  }

  function spark(vals, nat, i, ov = null, w = 240, h = 56) {
    const pts = vals.concat(nat || [], ov ? ov.usual : []).filter((v) => v != null);
    if (vals.length < 2 || !pts.length) return `<div class="a1x-muted">Single value (no time series)</div>`;
    const x = d3.scaleLinear().domain([0, vals.length - 1]).range([4, w - 4]);
    const y = d3.scaleLinear().domain(d3.extent(pts)).nice().range([h - 4, 4]);
    const line = d3.line().defined((v) => v != null).x((v, k) => x(k)).y((v) => y(v));
    const cur = vals[i] != null ? `<circle cx="${x(i)}" cy="${y(vals[i])}" r="3" fill="#08519c"/>` : "";
    const band = ov ? `<rect x="4" width="${w - 8}" y="${y(ov.usual[1])}" height="${Math.max(1, y(ov.usual[0]) - y(ov.usual[1]))}" fill="#9aa5b1" opacity=".2"/>` +
      `<line x1="4" x2="${w - 4}" y1="${y(ov.from)}" y2="${y(ov.from)}" stroke="#9aa5b1" stroke-dasharray="4 3"/>` : "";
    return `<svg width="${w}" height="${h}" role="img" aria-label="trend">${band}` +
      (nat ? `<path d="${line(nat) || ""}" fill="none" stroke="#9aa5b1" stroke-dasharray="3 3"/>` : "") +
      `<path d="${line(vals) || ""}" fill="none" stroke="#08519c" stroke-width="2"/>${cur}</svg>`;
  }

  function changeLegend(recs) {
    const box = mapBox.selectAll(".a1x-cl").data([0]).join("div").attr("class", "a1x-cl a1x-muted").html("");
    if (!st.since) return;
    if (!recs.length) { box.text(`No changes beyond usual variation for this measure, compared with ${SINCE_LABEL[st.since]}.`); return; }
    box.text(`Arrows show the direction of change; green is better, orange is worse. Marked only where the change is beyond a ` +
      `region's usual variation (compared with ${SINCE_LABEL[st.since]}). `);
    if (recs.length > MAX_MARKS) box.append("button").text(st.showAll ? `Show strongest ${MAX_MARKS}` : `Show all ${recs.length}`)
      .on("click", () => { st.showAll = !st.showAll; renderMap(); });
  }

  function renderPanel() {
    const { series } = st.data, sh = series.shapes[st.sel];
    if (!sh) { panel.html(`<div class="a1x-muted">Select a region on the map.</div>`); return; }
    let html = `<h3>${sh.name}</h3>`;
    for (const id of [st.m1, st.m2].filter(Boolean)) {
      const n = sh.n[M[id]?.source]?.[st.t];
      const warn = low(sh, id, st.t) ? `<div class="a1x-warn">Few tests (${n ?? "?"}): treat with caution.</div>`
        : n != null ? `<div class="a1x-muted">Based on ${n} tests</div>` : "";
      const rec = id === st.m1 ? changeRecs().find((r) => r.shapeId === st.sel) : null;
      html += `<div style="margin:.5rem 0"><b>${M[id].label}</b><br>${fmt(id, val(sh, id, st.t))}${warn}` +
        `${spark(sh.metrics[id] || [], series.national[id], st.t, rec && rec.type === "shift" ? rec : null)}` +
        (series.national[id] ? `<div class="a1x-muted">Dashed line: national figure</div>` : "") +
        (rec && rec.type === "shift" ? `<div class="a1x-muted">Grey band: usual range before the change</div>` : "") +
        (rec ? `<div style="margin-top:.4rem">${sentence(rec)}</div>` : "") + `</div>`;
    }
    if (sh.match === null) html += `<div class="a1x-warn">No speed data matched to this region.</div>`;
    else if (!["exact", "normalised", "override"].includes(sh.match))
      html += `<div class="a1x-warn">Region name matched approximately.</div>`;
    panel.html(html);
  }

  function renderMap() {
    const { geo, series } = st.data, c = colourFn();
    tLabel.text(series.periods[st.t] || "");
    const W = 560, H = 520;
    const svg = mapBox.selectAll("svg").data([0]).join("svg")
      .attr("viewBox", `0 0 ${W} ${H}`)
      .attr("width", W)
      .attr("height", H)
      .attr("role", "img").attr("aria-label", "Regional map");
    svg.html(`<defs><pattern id="a1x-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">` +
      `<line x1="0" y1="0" x2="0" y2="6" stroke="#333" stroke-width="1.5" opacity=".45"/></pattern></defs>`);
    const path = d3.geoPath(d3.geoMercator().fitSize([W, H], geo));
    const sid = (f) => f.properties.shapeID;
    svg.selectAll("path.r").data(geo.features).join("path").attr("class", (f) => "r" + (sid(f) === st.sel ? " sel" : ""))
      .attr("d", path).attr("fill", (f) => c.fn(series.shapes[sid(f)], st.t))
      .on("click", (e, f) => api.select(sid(f)))
      .append("title").text((f) => {
        const s = series.shapes[sid(f)];
        const sName = s?.name || f.properties?.shapeName || sid(f);
        return `${sName}: ${fmt(st.m1, val(s, st.m1, st.t))}${st.m2 ? " | " + fmt(st.m2, val(s, st.m2, st.t)) : ""}`;
      });
    svg.selectAll("path.h").data(geo.features.filter((f) => low(series.shapes[sid(f)], st.m1, st.t)))
      .join("path").attr("class", "h").attr("d", path).attr("fill", "url(#a1x-hatch)").style("pointer-events", "none");
    const recs = changeRecs(), shown = st.showAll ? recs : recs.slice(0, MAX_MARKS);
    const feat = Object.fromEntries(geo.features.map((f) => [sid(f), f]));
    const marks = svg.selectAll("g.a1x-chg").data(shown.filter((r) => feat[r.shapeId]))
      .join("g").attr("class", "a1x-chg").style("cursor", "pointer").on("click", (e, r) => api.select(r.shapeId))
      .attr("transform", (r) => { const [x, y] = path.centroid(feat[r.shapeId]); return `translate(${x},${y})`; });
    marks.append("circle").attr("r", 11).attr("fill", (r) => CHG_COL[r.effect || "neutral"]).attr("stroke", "#fff").attr("stroke-width", 1.5);
    marks.append("text").attr("text-anchor", "middle").attr("dy", "0.35em").attr("fill", "#fff").attr("font-size", 13).text(glyph);
    marks.append("title").text((r) => `${series.shapes[r.shapeId]?.name || r.shapeId}: ${sentence(r)}`);
    legend(c); changeLegend(recs); renderPanel();
    opts.onChange?.({ country: st.country, metric: st.m1, metric2: st.m2, period: series.periods[st.t] ?? null, region: st.sel,
      since: st.since });
  }

  async function refresh(resetSel, selId = null) {
    await load(st.country);
    const n = st.data.series.periods.length;
    if (pendingPeriod) { const k = st.data.series.periods.indexOf(pendingPeriod); if (k >= 0) st.t = k; pendingPeriod = null; }
    else if (st.t === 0 && n > 0) { st.t = n - 1; }
    st.t = Math.min(st.t, Math.max(0, n - 1));
    if (resetSel) st.sel = selId && st.data.series.shapes[selId] ? selId : null;
    slider.attr("max", Math.max(0, n - 1)).property("value", st.t).style("display", n > 1 ? null : "none");
    const keys = Object.keys(st.data.changes?.since || {});
    if (st.since && !keys.includes(st.since)) st.since = null;
    selSince.selectAll("option").data([null, ...keys]).join("option").attr("value", (d) => d || "")
      .text((d) => (d ? `vs ${SINCE_LABEL[d] || d}` : "Off"));
    d3.select(selSince.node().parentNode).style("display", keys.length ? null : "none");
    selSince.property("value", st.since || "");
    selCountry.property("value", st.country); selM1.property("value", st.m1); selM2.property("value", st.m2 || "");
    renderMap();
  }

  const api = {
    state: st, manifest,
    setCountry: (c, region = null) => { st.country = c; return refresh(true, region); },
    setMetric: (a, b = null) => { st.m1 = a; st.m2 = b || null; return refresh(false); },
    setSince: (k) => { st.since = k || null; st.showAll = false; selSince.property("value", st.since || ""); renderMap(); },
    setPeriod: (i) => { st.t = i; slider.property("value", i); renderMap(); },
    setPeriodLabel: (label) => { const k = st.data.series.periods.indexOf(label); if (k >= 0 && k !== st.t) api.setPeriod(k); },
    select: (id, { silent = false } = {}) => { st.sel = id; renderMap(); if (!silent) opts.onSelect?.({ iso3: st.country,
      shapeId: id, name: st.data.series.shapes[id]?.name }); },
    destroy: () => { root.html("").classed("a1x", false); },
  };
  selCountry.on("change", (e) => api.setCountry(e.target.value));
  selM1.on("change", (e) => api.setMetric(e.target.value, st.m2));
  selM2.on("change", (e) => api.setMetric(st.m1, e.target.value));
  selSince.on("change", (e) => api.setSince(e.target.value));
  slider.on("input", (e) => api.setPeriod(+e.target.value));
  await refresh(true, opts.region);
  return api;
}
