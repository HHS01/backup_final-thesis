/*
 * EdTech Traceability Observatory (v2)
 * Page-by-page drill-down with persistent left Depth Rail,
 * dedicated Overview / Macro / Meso / Micro pages, context chip, and drill cards.
 */
import { createDashboardState, createExplorerLink } from "../../js/dashboard_state.js";
import { mountAdmin1Explorer } from "../../js/admin1_explorer.js";

const ID = /^[\w.:-]{1,64}$/;
const LIVE = new Set(["explorer", "module", "iframe"]);

// Lens alias mapper for backwards compatibility
const LENS_MAP = {
  need: "learning",
  readiness: "infrastructure",
  money: "fiscal",
  classroom: "pilot"
};

export async function boot(opts = {}) {
  const win = opts.win || window;
  const doc = opts.doc || win.document;
  const d3 = opts.d3 || win.d3 || globalThis.d3;
  const getJson = opts.fetchJson || ((u) => fetch(u).then((r) => { if (!r.ok) throw new Error(`${u}: HTTP ${r.status}`); return r.json(); }));
  const registry = await getJson(opts.registryUrl || "./registry.json");
  const bundle = new URL(registry.bundleUrl || "./", doc.baseURI).href.replace(/\/?$/, "/");
  const schoolDataUrl = new URL(registry.schoolDataUrl || "../../out/dashboard/", doc.baseURI).href.replace(/\/?$/, "/");
  const manifest = await getJson(bundle + "manifest.json").catch(() => null);

  let status;
  try {
    status = await getJson(registry.dataStatusUrl);
  } catch {
    status = { mode: "demo", note: "No data-status file found; labelled as demo by default." };
  }

  const h = (tag, attrs = {}, ...kids) => {
    const el = doc.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === "class") el.className = v;
      else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
      else el.setAttribute(k, v === true ? "" : v);
    }
    for (const kid of kids.flat()) {
      if (kid != null) el.append(kid.nodeType ? kid : doc.createTextNode(String(kid)));
    }
    return el;
  };
  const $ = (id) => doc.getElementById(id);

  // ---------------------------------------------------------------- state
  const levelIds = registry.levels.map((l) => l.id);
  const lensIds = registry.lenses.map((l) => l.id);

  const schema = {
    country: { pattern: /^[A-Z]{3}$/, history: "push", resets: ["region", "site"] },
    level:   { enum: levelIds, history: "replace" },
    lens:    { enum: [...lensIds, ...Object.keys(LENS_MAP)], history: "push" },
    region:  { pattern: ID, history: "replace", resets: ["site"] },
    site:    { pattern: ID, history: "replace" },
    metric:  { pattern: ID, history: "replace" },
    metric2: { pattern: ID, history: "replace" },
    period:  { pattern: /^\d{4}(-\d{2})?$/, history: "replace" },
    since:   { enum: ["3m", "6m", "12m"], history: "replace" },
  };

  const defaults = { level: "overview", lens: lensIds[0], ...(registry.defaults || {}) };
  const state = createDashboardState({ schema, defaults, mode: "search", win });

  // Map legacy lens values
  const curLens = state.get().lens;
  if (LENS_MAP[curLens]) {
    state.set({ lens: LENS_MAP[curLens] }, { replace: true });
  }

  if (!state.get().country && manifest?.countries?.length) {
    state.set({ country: manifest.countries[0].iso3 }, { replace: true });
  }

  // ---------------------------------------------------------------- data helpers
  const seriesCache = {};
  const seriesFor = (iso3) => (seriesCache[iso3] ||= getJson(`${bundle}${iso3}.series.json`).catch(() => null));
  const metricsById = Object.fromEntries((manifest?.metrics || []).map((m) => [m.id, m]));

  const panelsFor = (level, lens) => registry.panels.filter((p) =>
    p.enabled !== false && p.level === level && (p.lenses === "all" || (p.lenses || []).includes(lens) || (p.lenses || []).includes("all"))
  );

  // ---------------------------------------------------------------- actions
  function setLevel(id) {
    if (state.get().level === id) return;
    state.set({ level: id });
    const canvas = $("page-canvas");
    if (canvas) canvas.scrollIntoView?.({ behavior: "smooth", block: "start" });
  }

  function setLens(id) {
    if (state.get().lens === id) return;
    state.set({ lens: id });
  }

  win.setDashboardLevel = setLevel;
  win.setDashboardLens = setLens;

  // ---------------------------------------------------------------- spine setup
  const countrySel = $("country-select");
  if (countrySel) {
    countrySel.replaceChildren();
    for (const c of manifest?.countries || []) {
      countrySel.append(h("option", { value: c.iso3 }, `${c.name} (${c.iso3})`));
    }
    countrySel.value = state.get().country || "KEN";
    countrySel.addEventListener("change", (e) => state.set({ country: e.target.value }));
  }

  // Lens Buttons in Spine
  const lensRow = $("lens-row");
  if (lensRow) {
    lensRow.replaceChildren();
    for (const ln of registry.lenses) {
      const btn = h("button", {
        type: "button",
        class: "lens-tab-btn",
        "data-lens": ln.id,
        onclick: () => setLens(ln.id)
      },
        ln.icon ? h("span", { class: "mr-1 text-xs" }, ln.icon) : null,
        h("span", {}, ln.shortLabel || ln.label)
      );
      lensRow.append(btn);
    }
  }

  // Tools Menu
  const toolsList = $("tools-list");
  if (toolsList) {
    toolsList.replaceChildren();
    for (const t of registry.tools || []) {
      toolsList.append(
        h("li", {},
          h("a", { href: t.href || "#", target: t.target || "_blank", class: "block p-2 rounded-lg hover:bg-slate-100 transition" },
            h("strong", { class: "block text-xs font-bold text-slate-900" }, t.label + " ↗"),
            h("p", { class: "text-[11px] text-slate-500 mt-0.5 leading-tight" }, [t.for, t.note].filter(Boolean).join(" · "))
          )
        )
      );
    }
  }

  const tag = $("data-tag");
  if (tag) {
    tag.textContent = status.mode === "real" ? "Live Telemetry" : "Calibrated Demo";
    if (status.note) tag.title = status.note;
  }

  // ---------------------------------------------------------------- LEFT DEPTH RAIL
  async function renderDepthRail() {
    const railNav = $("depth-nodes");
    if (!railNav) return;

    const s = state.get();
    const series = s.country ? await seriesFor(s.country) : null;
    const countryName = manifest?.countries?.find(c => c.iso3 === s.country)?.name || s.country;
    const regionName = s.region ? (series?.shapes?.[s.region]?.name || s.region) : null;
    const siteName = s.site || null;

    const levelOrder = ["overview", "macro", "meso", "micro"];
    const curIdx = levelOrder.indexOf(s.level) >= 0 ? levelOrder.indexOf(s.level) : 0;

    const nodeMeta = {
      overview: { label: "0 · Overview", badge: "Matrix Grid", sub: "All Scales" },
      macro:    { label: "1 · Macro",    badge: countryName,    sub: "National Context" },
      meso:     { label: "2 · Meso",     badge: regionName || (curIdx >= 2 ? "All Regions" : "not chosen yet"), sub: "Regional Spatial" },
      micro:    { label: "3 · Micro",    badge: siteName || (curIdx >= 3 ? "Frontline Sites" : "not chosen yet"), sub: "Classroom Ground" }
    };

    const newChildren = [];
    levelOrder.forEach((lvl, idx) => {
      const isCurrent = lvl === s.level;
      const isPassed = idx < curIdx;
      const isFuture = idx > curIdx;
      const meta = nodeMeta[lvl];

      const nodeBtn = h("button", {
        type: "button",
        class: `depth-node-card w-full text-left p-2.5 rounded-xl border transition cursor-pointer flex flex-col gap-1 ${
          isCurrent
            ? "border-emerald-600 bg-emerald-50/80 shadow-xs ring-2 ring-emerald-600/30"
            : isPassed
              ? "border-slate-300 bg-slate-50 hover:bg-slate-100"
              : "border-dashed border-slate-200 bg-white/60 hover:bg-slate-50 text-slate-400"
        }`,
        onclick: () => setLevel(lvl)
      },
        h("div", { class: "flex items-center justify-between w-full" },
          h("div", { class: "flex items-center gap-1.5" },
            h("span", {
              class: `w-2.5 h-2.5 rounded-full inline-block ${
                isCurrent
                  ? "bg-emerald-600 ring-4 ring-emerald-100 animate-pulse"
                  : isPassed
                    ? "bg-emerald-700"
                    : "border border-slate-300 bg-white"
              }`
            }),
            h("strong", { class: `text-xs font-bold ${isCurrent ? 'text-emerald-950 font-black' : isPassed ? 'text-slate-800' : 'text-slate-400'}` },
              meta.label
            )
          ),
          h("span", { class: "text-[9px] font-mono font-semibold text-slate-400" },
            lvl === "overview" ? "Grid" : registry.levels.find(l => l.id === lvl)?.scale || ""
          )
        ),
        h("div", { class: "pl-4" },
          h("span", {
            class: `text-[11px] font-bold inline-block px-1.5 py-0.2 rounded ${
              isCurrent
                ? "bg-emerald-200/70 text-emerald-900"
                : isPassed
                  ? "bg-slate-200 text-slate-700"
                  : "text-slate-400 italic"
            }`
          }, meta.badge),
          h("p", { class: "text-[10px] text-slate-400 leading-tight mt-0.5" }, meta.sub)
        )
      );

      newChildren.push(nodeBtn);
    });

    railNav.replaceChildren(...newChildren);
  }

  // ---------------------------------------------------------------- mount panels
  async function mountPanel(p, host) {
    const ctx = { state, registry, manifest, d3, getJson, bundleUrl: bundle, schoolDataUrl, doc };
    if (p.kind === "explorer") {
      if (!d3) {
        host.append(h("p", { class: "p-4 text-xs text-amber-800 bg-amber-50 rounded-lg" }, "d3 library failed to load; the map requires it."));
        return null;
      }
      const link = createExplorerLink(state);
      const api = await mountAdmin1Explorer(host, {
        d3,
        baseUrl: bundle,
        schoolDataUrl: bundle,
        fetchJson: getJson,
        ...link.options
      });
      const detach = link.attach(api);
      return () => { detach(); api.destroy(); };
    }
    if (p.kind === "module") {
      const mod = await import(new URL(p.module, import.meta.url).href);
      const ret = await mod.default(host, ctx);
      return typeof ret === "function" ? ret : ret?.destroy || null;
    }
    if (p.kind === "iframe") {
      host.append(h("iframe", { src: p.src, title: p.title, loading: "lazy", class: "w-full min-h-[30rem] rounded-xl border border-slate-200" }));
      return null;
    }
    host.append(h("p", { class: "p-4 text-xs text-slate-500 italic" }, p.note || "Planned widget."));
    return null;
  }

  // ---------------------------------------------------------------- MAIN PAGE CANVAS RENDERER
  let activeDestroyers = [];

  async function renderPageCanvas() {
    for (const f of activeDestroyers) {
      try { f(); } catch { /* ignore */ }
    }
    activeDestroyers = [];

    const canvas = $("page-canvas");
    if (!canvas) return;
    canvas.replaceChildren();

    const s = state.get();
    const curLevel = registry.levels.find((l) => l.id === s.level) || registry.levels[0];
    const curLensObj = registry.lenses.find((ln) => ln.id === s.lens) || registry.lenses[0];
    const series = s.country ? await seriesFor(s.country) : null;
    const countryName = manifest?.countries?.find(c => c.iso3 === s.country)?.name || s.country;
    const regionName = s.region ? (series?.shapes?.[s.region]?.name || s.region) : null;

    // Context Chip
    const contextChip = h("div", { class: "flex items-center gap-2 text-xs text-slate-500 bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 w-fit" },
      h("span", { class: "font-semibold text-slate-400" }, "inside:"),
      h("strong", { class: "text-slate-800" }, countryName),
      regionName ? h("span", { class: "text-slate-400" }, "›") : null,
      regionName ? h("strong", { class: "text-emerald-700" }, regionName) : null,
      s.site ? h("span", { class: "text-slate-400" }, "›") : null,
      s.site ? h("span", { class: "text-slate-600" }, s.site) : null
    );
    canvas.append(contextChip);

    // =========================================================================
    // PAGE 0 · OVERVIEW (Levels-by-Lenses Grid)
    // =========================================================================
    if (s.level === "overview") {
      const header = h("header", { class: "border-b border-slate-100 pb-3" },
        h("div", { class: "flex items-center gap-2 mb-1" },
          h("span", { class: "text-[10px] font-extrabold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-900 text-white" }, "Entry Matrix"),
          h("span", { class: "text-xs text-slate-500 font-medium" }, "Levels × Lenses Overview")
        ),
        h("h2", { class: "text-2xl font-black text-slate-900" }, "0 · Overview: Cross-Scale Traceability Matrix"),
        h("p", { class: "text-sm text-slate-600 mt-1 max-w-3xl" },
          "Click any cell in the grid below to drill directly into that analytical scale and lens. Cells marked with dashed borders indicate data gaps awaiting verified open records."
        )
      );
      canvas.append(header);

      const matrixGrid = h("div", { class: "space-y-4 my-2" });
      const gridLevels = registry.levels.filter(l => l.id !== "overview");

      for (const lv of gridLevels) {
        const row = h("div", { class: "bg-slate-50 border border-slate-200 rounded-2xl p-4 shadow-2xs" },
          h("div", { class: "flex items-baseline justify-between mb-3 border-b border-slate-200/80 pb-2" },
            h("div", { class: "flex items-center gap-2" },
              h("span", { class: "text-xs font-mono font-bold px-2 py-0.5 rounded bg-slate-200 text-slate-700" }, lv.scale),
              h("h3", { class: "text-base font-black text-slate-900" }, lv.label),
              h("span", { class: "text-xs text-slate-500 hidden sm:inline" }, `— ${lv.scope}`)
            ),
            h("button", {
              type: "button",
              class: "text-xs font-bold text-emerald-700 hover:text-emerald-800 hover:underline cursor-pointer",
              onclick: () => setLevel(lv.id)
            }, `Open ${lv.shortLabel} Page →`)
          ),
          h("div", { class: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3" },
            registry.lenses.map(ln => {
              const panels = panelsFor(lv.id, ln.id);
              const gap = (registry.gaps || []).find(g => g.level === lv.id && g.lens === ln.id);
              const hasData = panels.length > 0;

              return h("div", {
                class: `p-3 rounded-xl border transition cursor-pointer flex flex-col justify-between min-h-[6.5rem] ${
                  hasData
                    ? "bg-white border-slate-200 hover:border-emerald-600 hover:shadow-xs"
                    : "border-dashed border-slate-300 bg-slate-100/50 hover:bg-slate-100 text-slate-400"
                }`,
                onclick: () => {
                  state.set({ level: lv.id, lens: ln.id });
                }
              },
                h("div", {},
                  h("div", { class: "flex items-center justify-between text-[11px] mb-1 font-bold" },
                    h("span", { class: hasData ? "text-slate-800" : "text-slate-400" }, `${ln.icon || ""} ${ln.shortLabel}`),
                    h("span", { class: `text-[9px] px-1.5 py-0.2 rounded font-bold uppercase ${hasData ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'}` },
                      hasData ? "Measured" : "Gap"
                    )
                  ),
                  h("p", { class: "text-xs font-semibold leading-snug line-clamp-2 " + (hasData ? "text-slate-700" : "text-slate-400 italic") },
                    hasData ? panels[0].title : `Not measured yet: ${gap?.wouldFill || "Field data pending"}`
                  )
                ),
                h("span", { class: "text-[10px] font-bold text-emerald-700 mt-2 block" },
                  hasData ? "View Telemetry →" : "Explore Gap →"
                )
              );
            })
          )
        );
        matrixGrid.append(row);
      }
      canvas.append(matrixGrid);

      // Bottom Drill Card for Overview
      const drillCards = h("div", { class: "grid grid-cols-1 sm:grid-cols-2 gap-3 mt-4 pt-4 border-t border-slate-200" },
        h("div", { class: "p-4 rounded-xl border border-slate-200 bg-slate-50 text-xs text-slate-500" },
          h("strong", { class: "block font-bold text-slate-700 mb-1" }, "Ground-Truth Participation"),
          h("p", {}, "Field surveys calibrate the classroom reality. Use the top ribbon to submit observations via KoboToolbox.")
        ),
        h("button", {
          type: "button",
          class: "p-4 rounded-xl border border-emerald-600 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-xs transition cursor-pointer text-left flex items-center justify-between",
          onclick: () => setLevel("macro")
        },
          h("div", {},
            h("span", { class: "block text-[10px] uppercase tracking-wider text-emerald-200" }, "↓ Go deeper"),
            h("strong", { class: "text-sm block text-white" }, "Open Level 1: Macro Page")
          ),
          h("span", { class: "text-lg" }, "➔")
        )
      );
      canvas.append(drillCards);
      return;
    }

    // =========================================================================
    // PAGES 1, 2, 3: MACRO, MESO, MICRO (Single Page Per Level)
    // =========================================================================
    const header = h("header", { class: "border-b border-slate-100 pb-3" },
      h("div", { class: "flex items-center gap-2 mb-1" },
        h("span", { class: "text-[10px] font-extrabold uppercase tracking-wider px-2 py-0.5 rounded-full bg-slate-900 text-white" },
          curLevel.optic || "Optical Depth"
        ),
        h("span", { class: "text-xs font-mono font-bold text-slate-500" },
          `Scale ${curLevel.scale}`
        ),
        h("span", { class: "text-xs font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800" },
          `Perspective: ${curLensObj.label}`
        )
      ),
      h("h2", { class: "text-2xl font-black text-slate-900" },
        `${curLevel.label}: ${curLevel.scope}`
      ),
      h("p", { class: "text-sm text-slate-600 mt-1 max-w-3xl" },
        curLevel.blurb || ""
      )
    );
    canvas.append(header);

    // Query and Render Panels
    const panels = panelsFor(curLevel.id, curLensObj.id);
    const panelContainer = h("div", { class: "space-y-6 my-2" });

    if (!panels.length) {
      const gap = (registry.gaps || []).find((g) => g.level === curLevel.id && g.lens === curLensObj.id);
      panelContainer.append(
        h("div", { class: "border-2 border-dashed border-slate-300 rounded-2xl p-8 text-center bg-slate-50/60 space-y-2" },
          h("span", { class: "text-3xl block" }, "🔍"),
          h("strong", { class: "block text-base font-bold text-slate-800" },
            `Not Measured Yet: ${curLensObj.label} at ${curLevel.label}`
          ),
          gap?.wouldFill ? h("p", { class: "text-xs text-slate-600 max-w-lg mx-auto" }, `What would fill this gap: ${gap.wouldFill}`) : null,
          h("div", { class: "pt-2 flex justify-center gap-2" },
            h("button", {
              type: "button",
              class: "px-3 py-1.5 bg-slate-200 hover:bg-slate-300 text-slate-800 text-xs font-bold rounded-lg transition cursor-pointer",
              onclick: () => setLevel("overview")
            }, "View Cross-Scale Matrix"),
            h("button", {
              type: "button",
              class: "px-3 py-1.5 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-lg transition cursor-pointer",
              onclick: () => setLens("infrastructure")
            }, "Switch to Infrastructure Reality")
          )
        )
      );
    } else {
      for (const p of panels) {
        const host = h("div", { class: "panel-content mt-3" });
        const card = h("article", { class: "bg-slate-50/80 border border-slate-200 rounded-2xl p-5 shadow-2xs", "data-panel": p.id },
          h("header", { class: "flex items-baseline justify-between border-b border-slate-200 pb-2 mb-2" },
            h("h3", { class: "text-base font-bold text-slate-900" }, p.title),
            h("span", { class: "text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider bg-emerald-100 text-emerald-800" },
              p.status || "active"
            )
          ),
          host,
          p.source ? h("footer", { class: "mt-3 pt-2 border-t border-dashed border-slate-200 text-[11px] text-slate-500" },
            `Data Provenance: ${p.source}`
          ) : null
        );
        panelContainer.append(card);

        try {
          const d = await mountPanel(p, host);
          if (d) activeDestroyers.push(d);
        } catch (err) {
          host.replaceChildren(h("p", { class: "p-3 bg-rose-50 text-rose-700 text-xs rounded-lg" }, "Widget error: " + err.message));
        }
      }
    }
    canvas.append(panelContainer);

    // =========================================================================
    // BOTTOM DRILL CARDS ("↓ Go deeper" & "↑ Back up")
    // =========================================================================
    const drillCards = h("div", { class: "grid grid-cols-1 sm:grid-cols-2 gap-4 mt-6 pt-5 border-t border-slate-200" });

    if (curLevel.id === "macro") {
      drillCards.append(
        h("div", { class: "p-4 rounded-xl border border-slate-200 bg-slate-50 text-xs text-slate-500 flex flex-col justify-center" },
          h("span", { class: "text-[10px] uppercase font-bold text-slate-400" }, "↑ Top Level"),
          h("strong", { class: "text-sm text-slate-700 font-bold" }, "Level 1: Macro is the highest scale"),
          h("button", {
            type: "button",
            class: "text-emerald-700 font-bold hover:underline text-left mt-1 cursor-pointer",
            onclick: () => setLevel("overview")
          }, "⮌ Back to Overview Matrix")
        ),
        h("button", {
          type: "button",
          class: "p-4 rounded-xl border border-emerald-600 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-xs transition cursor-pointer text-left flex items-center justify-between",
          onclick: () => setLevel("meso")
        },
          h("div", {},
            h("span", { class: "block text-[10px] uppercase tracking-wider text-emerald-200" }, "↓ Go deeper"),
            h("strong", { class: "text-sm block text-white" }, "Level 2: Meso (Regional Disparities & Maps)")
          ),
          h("span", { class: "text-xl font-bold" }, "➔")
        )
      );
    } else if (curLevel.id === "meso") {
      const regTxt = regionName ? `in ${regionName}` : "Across Schools";
      drillCards.append(
        h("button", {
          type: "button",
          class: "p-4 rounded-xl border border-slate-300 bg-white hover:bg-slate-50 text-slate-800 font-bold text-xs shadow-2xs transition cursor-pointer text-left flex items-center justify-between",
          onclick: () => setLevel("macro")
        },
          h("div", {},
            h("span", { class: "block text-[10px] uppercase tracking-wider text-slate-400" }, "↑ Back up"),
            h("strong", { class: "text-sm block text-slate-800" }, "Level 1: Macro (National Overview)")
          ),
          h("span", { class: "text-lg text-slate-400" }, "⬆")
        ),
        h("button", {
          type: "button",
          class: "p-4 rounded-xl border border-emerald-600 bg-emerald-700 hover:bg-emerald-800 text-white font-bold text-xs shadow-xs transition cursor-pointer text-left flex items-center justify-between",
          onclick: () => setLevel("micro")
        },
          h("div", {},
            h("span", { class: "block text-[10px] uppercase tracking-wider text-emerald-200" }, "↓ Go deeper"),
            h("strong", { class: "text-sm block text-white" }, `Level 3: Micro (${regTxt})`)
          ),
          h("span", { class: "text-xl font-bold" }, "➔")
        )
      );
    } else if (curLevel.id === "micro") {
      drillCards.append(
        h("button", {
          type: "button",
          class: "p-4 rounded-xl border border-slate-300 bg-white hover:bg-slate-50 text-slate-800 font-bold text-xs shadow-2xs transition cursor-pointer text-left flex items-center justify-between",
          onclick: () => setLevel("meso")
        },
          h("div", {},
            h("span", { class: "block text-[10px] uppercase tracking-wider text-slate-400" }, "↑ Back up"),
            h("strong", { class: "text-sm block text-slate-800" }, "Level 2: Meso (Regional Spatial View)")
          ),
          h("span", { class: "text-lg text-slate-400" }, "⬆")
        ),
        h("div", { class: "p-4 rounded-xl border border-slate-200 bg-slate-50 text-xs text-slate-500 flex flex-col justify-center" },
          h("span", { class: "text-[10px] uppercase font-bold text-slate-400" }, "Frontline Micro Limit"),
          h("strong", { class: "text-sm text-slate-700 font-bold" }, "Ground-level classroom reality reached"),
          h("p", { class: "text-[11px] text-slate-500 mt-0.5" }, "Giga synthetic records + UNESCO AoA field testimonies.")
        )
      );
    }

    canvas.append(drillCards);
  }

  // ---------------------------------------------------------------- RIGHT TRACE PANEL (VERTICAL CROSS-SECTION)
  let traceToken = 0;
  async function renderTrace() {
    const token = ++traceToken;
    const s = state.get();
    const box = $("trace");
    if (!box) return;

    const series = s.country ? await seriesFor(s.country) : null;
    if (token !== traceToken) return;
    box.replaceChildren();

    const mid = s.metric || manifest?.metrics?.[0]?.id || "download_p50";
    const m = metricsById[mid] || { label: "Download Speed", unit: "Mbps", decimals: 1, source: "M-Lab" };

    if (!series) {
      box.append(
        h("h3", { class: "font-black text-sm text-slate-900" }, "Vertical Traceability HUD"),
        h("p", { class: "text-xs text-slate-400 mt-1" }, "No regional measurements found for this economy.")
      );
      return;
    }

    let idx = s.period ? series.periods.indexOf(s.period) : -1;
    if (idx < 0) idx = series.periods.length - 1;

    const shape = s.region ? series.shapes[s.region] : null;
    const val = (v) => (v == null ? null : v);

    const rows = [
      {
        level: "macro",
        label: "National Mean",
        scale: "1:1M",
        value: val(series.national?.[mid]?.[idx]),
        optic: "Macro Level",
        instrument: "Instrument A: M-Lab Speed Tests"
      },
      {
        level: "meso",
        label: shape ? shape.name : "Regional Scale",
        scale: "1:50k",
        value: shape ? val(shape.metrics?.[mid]?.[idx]) : undefined,
        optic: shape ? "Meso Level" : "Select Region on Map",
        instrument: "Instrument A: Sub-National M-Lab"
      },
      {
        level: "micro",
        label: "Frontline Site",
        scale: "1:1",
        value: null,
        text: "0.8 Mbps (Field Avg)",
        optic: "Micro Ground",
        instrument: "Instrument B: Giga Schoolhouse Meter"
      }
    ];

    const max = Math.max(...rows.map((r) => r.value ?? 0), 0) || 1;
    const fmt = (v) => `${Number(v).toFixed(m.decimals ?? 1)} ${m.unit || ""}`.trim();

    box.append(
      h("div", { class: "flex items-center justify-between border-b border-slate-100 pb-2 mb-2" },
        h("h3", { class: "font-black text-xs text-slate-900 uppercase tracking-wider" }, "Vertical Cross-Section"),
        h("span", { class: "text-[9px] font-extrabold uppercase px-1.5 py-0.5 rounded bg-slate-100 text-slate-700" }, "Trace HUD")
      ),
      h("p", { class: "text-[11px] text-slate-500 mb-3" }, `${m.label} cascading across scales:`),
      h("ul", { class: "space-y-2.5 my-3" }, rows.map((r) => {
        const none = r.value == null;
        const text = r.value === undefined ? "select a region" : none ? (r.text || "no data") : fmt(r.value);
        const isCurrent = s.level === r.level;
        return h("li", {
          class: `p-2.5 rounded-xl border transition ${isCurrent ? 'border-emerald-600 bg-emerald-50/70 shadow-xs' : 'border-slate-200 bg-slate-50'}`
        },
          h("div", { class: "flex items-center justify-between text-xs" },
            h("span", { class: "font-bold text-slate-800" }, `${r.label} `),
            h("span", { class: none ? "text-slate-400 font-mono" : "text-emerald-700 font-bold font-mono" }, text)
          ),
          h("div", { class: "w-full bg-slate-200 rounded-full h-1.5 mt-1.5 overflow-hidden" },
            none ? null : h("div", { class: "bg-emerald-600 h-full rounded-full transition-all duration-300", style: `width:${Math.max(4, (r.value / max) * 100)}%` })
          ),
          h("div", { class: "flex justify-between text-[10px] text-slate-400 mt-1" },
            h("span", { class: "truncate max-w-[11rem]" }, r.instrument),
            h("span", { class: "font-mono font-bold" }, r.scale)
          )
        );
      })),
      h("dl", { class: "grid grid-cols-2 gap-1 text-[11px] border-t border-slate-100 pt-3 my-2" },
        h("dt", { class: "text-slate-500" }, "Primary Metric:"),
        h("dd", { class: "text-right font-medium text-slate-800 truncate" }, m.label),
        h("dt", { class: "text-slate-500" }, "Period:"),
        h("dd", { class: "text-right font-mono font-medium text-slate-800" }, series.periods[idx] || "Latest"),
        h("dt", { class: "text-slate-500" }, "Samples:"),
        h("dd", { class: "text-right font-medium text-slate-800" }, shape?.n?.[m.source]?.[idx] != null ? `${shape.n[m.source][idx]} tests` : "National")
      ),
      h("div", { class: "space-y-1.5 pt-2" },
        h("button", {
          type: "button",
          class: "w-full px-3 py-1.5 bg-slate-100 hover:bg-slate-200 border border-slate-300 rounded-lg text-xs font-bold text-slate-800 transition cursor-pointer",
          onclick: () => openTable(series, mid, m, shape)
        }, "📊 View Full Period Table")
      )
    );
  }

  function openTable(series, mid, m, shape) {
    const dlg = $("table-dialog");
    const body = $("table-body");
    body.replaceChildren(
      h("h3", { class: "text-base font-bold text-slate-900 mb-2" }, `${m.label} Historical Time-Series`),
      h("div", { class: "overflow-x-auto max-h-80 border border-slate-200 rounded-xl" },
        h("table", { class: "w-full text-xs text-left" },
          h("thead", { class: "bg-slate-100 text-slate-700 font-bold sticky top-0" },
            h("tr", {},
              h("th", { class: "p-2 border-b" }, "Period"),
              h("th", { class: "p-2 border-b text-right" }, `National (${series.national?.iso3 || "Country"})`),
              shape ? h("th", { class: "p-2 border-b text-right" }, shape.name) : null
            )
          ),
          h("tbody", {}, series.periods.map((per, i) =>
            h("tr", { class: "border-b border-slate-100 hover:bg-slate-50" },
              h("td", { class: "p-2 font-mono" }, per),
              h("td", { class: "p-2 text-right font-mono font-semibold" }, series.national?.[mid]?.[i] ?? "–"),
              shape ? h("td", { class: "p-2 text-right font-mono text-emerald-700 font-semibold" }, shape.metrics?.[mid]?.[i] ?? "–") : null
            )
          ))
        )
      )
    );
    if (typeof dlg.showModal === "function") dlg.showModal(); else dlg.setAttribute("open", "");
  }

  // ---------------------------------------------------------------- spine updater
  async function updateSpine(s) {
    if (countrySel && countrySel.value !== s.country && s.country) {
      countrySel.value = s.country;
    }

    if (lensRow) {
      for (const b of lensRow.children) {
        const lnId = b.getAttribute("data-lens");
        const isActive = lnId === s.lens;
        b.setAttribute("aria-pressed", String(isActive));
        if (isActive) {
          b.className = "lens-tab-btn px-2.5 py-1 rounded-md text-xs font-bold bg-slate-900 text-white shadow-xs transition cursor-pointer";
        } else {
          b.className = "lens-tab-btn px-2.5 py-1 rounded-md text-xs font-semibold text-slate-600 hover:text-slate-900 hover:bg-slate-200 transition cursor-pointer";
        }
      }
    }
  }

  // ---------------------------------------------------------------- wiring
  state.subscribe((s, changed) => {
    updateSpine(s);
    renderDepthRail();
    if (changed.some((k) => ["level", "lens", "country", "region"].includes(k))) {
      renderPageCanvas();
    }
    if (changed.some((k) => ["country", "region", "metric", "period", "level"].includes(k))) {
      renderTrace();
    }
  });

  await updateSpine(state.get());
  await renderDepthRail();
  await renderPageCanvas();
  await renderTrace();

  return { state, registry, destroy: () => state.destroy() };
}
