/*
 * dashboard_state.js - ONE shared state for every panel, mirrored in the URL (deep links).
 * Framework-agnostic ES module, no dependencies.
 *
 *   import { createDashboardState, createExplorerLink } from "./dashboard_state.js";
 *   const state = createDashboardState({ defaults: { link: "need" } });   // reads the URL on creation
 *
 *   // any panel, any framework:
 *   state.subscribe((s, changed, source) => redrawMyChart(s));            // source: "set" | "url"
 *   state.set({ country: "KEN", link: "readiness" });                     // updates URL + notifies everyone
 *   shareButton.href = state.href({ region: "KEN12" });                   // link to an exact view
 *
 *   // the regional explorer (admin1_explorer.js) joins in with three lines:
 *   const link = createExplorerLink(state);
 *   const api = await mountAdmin1Explorer(el, { baseUrl, ...link.options });
 *   link.attach(api);
 *
 * Design notes
 *  - Only keys listed in the schema are read from the URL, and each value is validated (enum or pattern,
 *    max 64 chars). Anything else is ignored, so a crafted link can't inject content. Treat state values as
 *    data: never put them into innerHTML.
 *  - Changing `country` resets `region` (see `resets`). Country/link/perspective changes create browser-history
 *    entries (Back works); region/metric/period changes replace the current entry, so scrubbing a slider
 *    doesn't flood history. Replace-writes are debounced (Safari rate-limits replaceState).
 *  - Unknown URL params (e.g. your router's) are preserved. mode "hash" (default) uses #a=b&c=d; if your
 *    dashboard already uses the hash for routing, pass mode: "search" to use ?a=b&c=d instead.
 *  - `link` (stage of the adoption chain) and `perspective` (audience) values below are PLACEHOLDERS: edit
 *    the enums to match your lenses.
 */
const ID = /^[\w.:-]{1,64}$/;

export const DEFAULT_SCHEMA = {
  country:     { pattern: /^[A-Z]{3}$/, history: "push", resets: ["region"] },
  link:        { enum: ["need", "money", "readiness", "classroom", "verdict"], history: "push" },
  perspective: { enum: ["citizen", "teacher", "treasury", "donor"], history: "push" },
  region:      { pattern: ID, history: "replace" },
  metric:      { pattern: ID, history: "replace" },
  metric2:     { pattern: ID, history: "replace" },
  period:      { pattern: /^\d{4}(-\d{2})?$/, history: "replace" },
  since:       { enum: ["3m", "6m", "12m"], history: "replace" },
};

export function createDashboardState({ schema = DEFAULT_SCHEMA, defaults = {}, mode = "hash",
                                       debounceMs = 150, win = globalThis.window } = {}) {
  const keys = Object.keys(schema);
  const listeners = new Set();
  let timer = null;

  const clean = (k, v) => {
    if (v == null) return "";
    v = String(v).slice(0, 64);
    const s = schema[k];
    if (s.enum) return s.enum.includes(v) ? v : "";
    return s.pattern && s.pattern.test(v) ? v : "";
  };
  const readParams = () => new URLSearchParams(
    mode === "hash" ? win.location.hash.replace(/^#/, "") : win.location.search.replace(/^\?/, ""));
  const parse = () => {
    const p = readParams(), s = {};
    for (const k of keys) s[k] = clean(k, p.get(k)) || (defaults[k] ?? "");
    return s;
  };
  const urlFor = (s) => {
    const p = readParams();
    for (const k of keys) { p.delete(k); if (s[k] && s[k] !== (defaults[k] ?? "")) p.set(k, s[k]); }
    const qs = p.toString(), { pathname, search, hash } = win.location;
    return mode === "hash" ? pathname + search + (qs ? "#" + qs : "") : pathname + (qs ? "?" + qs : "") + hash;
  };

  let state = parse();
  const notify = (changed, source) => {
    const snap = Object.freeze({ ...state });
    for (const fn of [...listeners]) fn(snap, changed, source);
  };
  const writeUrl = (push) => {
    clearTimeout(timer); timer = null;
    if (push) { win.history.pushState(null, "", urlFor(state)); return; }
    timer = setTimeout(() => { timer = null; win.history.replaceState(null, "", urlFor(state)); }, debounceMs);
  };

  function set(patch, { replace = false } = {}) {
    const next = { ...state }, changed = [];
    for (const k of Object.keys(patch)) {
      if (!(k in schema)) continue;
      const v = clean(k, patch[k]);
      if (v !== next[k]) { next[k] = v; changed.push(k); }
    }
    for (const k of [...changed]) for (const r of schema[k].resets || []) {
      if (!(r in patch) && next[r] !== (defaults[r] ?? "")) { next[r] = defaults[r] ?? ""; changed.push(r); }
    }
    if (!changed.length) return false;
    state = next;
    writeUrl(!replace && changed.some((k) => schema[k].history === "push"));
    notify(changed, "set");
    return true;
  }

  const onUrl = () => {
    clearTimeout(timer); timer = null;
    const next = parse(), changed = keys.filter((k) => next[k] !== state[k]);
    if (!changed.length) return;
    state = next;
    notify(changed, "url");
  };
  win.addEventListener("popstate", onUrl);
  win.addEventListener("hashchange", onUrl);

  return {
    get: () => Object.freeze({ ...state }),
    set,
    subscribe(fn, { immediate = false } = {}) {
      listeners.add(fn);
      if (immediate) fn(Object.freeze({ ...state }), keys, "init");
      return () => listeners.delete(fn);
    },
    href(patch = {}) {
      const next = { ...state };
      for (const k of Object.keys(patch)) if (k in schema) next[k] = clean(k, patch[k]);
      for (const k of Object.keys(patch)) for (const r of schema[k]?.resets || []) if (!(r in patch)) next[r] = "";
      return win.location.origin + urlFor(next);
    },
    flush() { if (timer) { clearTimeout(timer); timer = null; win.history.replaceState(null, "", urlFor(state)); } },
    destroy() {
      clearTimeout(timer);
      win.removeEventListener("popstate", onUrl); win.removeEventListener("hashchange", onUrl);
      listeners.clear();
    },
  };
}

/* Connects admin1_explorer.js to the shared state (both directions, without echo loops). */
export function createExplorerLink(state) {
  let api = null, syncing = false, mounted = false, unsub = null;
  const s0 = state.get();
  const options = {
    country: s0.country || undefined, metric: s0.metric || undefined, metric2: s0.metric2 || undefined,
    region: s0.region || undefined, period: s0.period || undefined, since: s0.since || undefined,
    onChange: (c) => {                      // explorer -> state
      if (syncing) return;
      state.set({ country: c.country, metric: c.metric, metric2: c.metric2 || "",
                  period: c.period || "", region: c.region || "", since: c.since || "" }, { replace: !mounted });
    },
  };

  async function apply(s) {                 // state -> explorer
    if (!api) return;
    const man = api.manifest, cur = api.state;
    const okMetric = (id) => !!id && man.metrics.some((m) => m.id === id);
    syncing = true;
    try {
      if (s.country && s.country !== cur.country && man.countries.some((c) => c.iso3 === s.country)) {
        await api.setCountry(s.country, s.region || null);
      } else if ((s.region || null) !== (cur.sel || null)) {
        api.select(s.region || null, { silent: true });
      }
      if (okMetric(s.metric) && (s.metric !== cur.m1 || (okMetric(s.metric2) ? s.metric2 : null) !== cur.m2)) {
        await api.setMetric(s.metric, okMetric(s.metric2) ? s.metric2 : null);
      }
      if (s.period) api.setPeriodLabel(s.period);
      if ((s.since || null) !== (cur.since || null)) api.setSince(s.since || null);
    } finally { syncing = false; }
  }

  return {
    options,
    attach(a) { api = a; mounted = true; unsub = state.subscribe((s) => apply(s)); return () => unsub && unsub(); },
  };
}
