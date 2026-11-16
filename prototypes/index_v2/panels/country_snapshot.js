function el(doc, tag, text, className) {
  const node = doc.createElement(tag);
  if (text != null) node.textContent = text;
  if (className) node.className = className;
  return node;
}

export default function mount(host, ctx) {
  const { doc, state, manifest, getJson, bundleUrl } = ctx;
  const cache = new Map();
  let requestId = 0;

  async function render(s) {
    const id = ++requestId;
    host.replaceChildren(el(doc, "p", "Loading national connectivity telemetry…", "text-xs text-slate-400 p-4"));
    
    try {
      let promise = cache.get(s.country);
      if (!promise) {
        promise = getJson(`${bundleUrl}${s.country}.series.json`);
        cache.set(s.country, promise);
      }
      const series = await promise;
      if (id !== requestId) return;
      if (!series) throw new Error("No series data available");

      const periodIndex = series.periods.length - 1;
      const period = series.periods[periodIndex] || "Latest";
      const countryObj = manifest?.countries?.find(c => c.iso3 === s.country);
      const countryName = countryObj?.name || s.country;

      // Extract metrics
      const dP50 = series.national?.download_p50?.[periodIndex];
      const dP25 = series.national?.download_p25?.[periodIndex];
      const latP50 = series.national?.latency_p50?.[periodIndex];
      const uP50 = series.national?.upload_p50?.[periodIndex];

      const container = el(doc, "div", null, "space-y-6");

      // -----------------------------------------------------------------------
      // 1. HEADLINE SLOT
      // -----------------------------------------------------------------------
      const headline = el(doc, "div", null, "bg-gradient-to-r from-slate-900 to-slate-800 text-white rounded-2xl p-5 shadow-sm");
      headline.append(
        el(doc, "span", "Executive Infrastructure Telemetry · Level 1 Macro", "text-[10px] font-extrabold uppercase tracking-wider text-emerald-400 block mb-1"),
        el(doc, "h3", `National Bandwidth Asymmetry: ${countryName} (${period})`, "text-lg sm:text-xl font-black text-white"),
        el(doc, "p", `Voluntary public M-Lab speed tests reveal national median throughput of ${dP50 ? Number(dP50).toFixed(1) + ' Mbps' : 'N/A'}, while 25% of users experience severe bottleneck speeds below ${dP25 ? Number(dP25).toFixed(1) + ' Mbps' : 'N/A'}. This creates severe friction for simultaneous classroom streaming.`, "text-xs text-slate-300 mt-2 leading-relaxed")
      );
      container.append(headline);

      // -----------------------------------------------------------------------
      // 2. PRIMARY VISUALISATION: PAPER VS. GROUND COMPARISON
      // -----------------------------------------------------------------------
      const paperGroundCard = el(doc, "div", null, "bg-white border border-slate-200 rounded-2xl p-5 shadow-xs");
      paperGroundCard.append(
        el(doc, "h4", "Primary Observatory Lens: Paper Ambition vs. Ground Reality", "text-xs font-extrabold uppercase tracking-wider text-slate-500 mb-3")
      );

      const compGrid = el(doc, "div", null, "grid grid-cols-1 md:grid-cols-2 gap-4");

      // Paper Box
      const paperBox = el(doc, "div", null, "p-4 rounded-xl border-2 border-dashed border-stone-300 bg-stone-50/70 flex flex-col justify-between");
      paperBox.append(
        el(doc, "div", null, null),
        el(doc, "span", "On Paper: Statutory & Planning Target", "text-[10px] font-extrabold uppercase tracking-wider text-stone-600 block mb-1"),
        el(doc, "div", "Universal 4G Digital Schools", "text-xl font-serif italic text-stone-800 font-bold"),
        el(doc, "p", "National ICT Masterplan assumes high-speed broadband availability across all accredited basic education centers by 2030.", "text-xs text-stone-600 mt-2 leading-normal"),
        el(doc, "div", "Paper Claim: 96% Cellular Coverage", "text-[11px] font-mono text-stone-500 mt-3 pt-2 border-t border-stone-200")
      );

      // Ground Box
      const groundBox = el(doc, "div", null, "p-4 rounded-xl border-2 border-emerald-600 bg-emerald-50/70 flex flex-col justify-between shadow-2xs");
      const dValStr = dP50 ? `${Number(dP50).toFixed(1)} Mbps` : "N/A";
      groundBox.append(
        el(doc, "div", null, null),
        el(doc, "span", "On Ground: Empirical Measured Speed", "text-[10px] font-extrabold uppercase tracking-wider text-emerald-800 block mb-1"),
        el(doc, dValStr, "text-2xl font-mono font-black text-emerald-950"),
        el(doc, `Median ground throughput across voluntary speed tests. The bottom quartile experiences ${dP25 ? Number(dP25).toFixed(1) + ' Mbps' : 'N/A'}, rendering cloud video delivery non-viable in rural county schools without offline caching.`, "text-xs text-emerald-900 mt-2 leading-normal"),
        el(doc, `Ground Reality: Median Latency ${latP50 ? Number(latP50).toFixed(0) + ' ms' : 'N/A'}`, "text-[11px] font-mono font-bold text-emerald-700 mt-3 pt-2 border-t border-emerald-200")
      );

      compGrid.append(paperBox, groundBox);
      paperGroundCard.append(compGrid);
      container.append(paperGroundCard);

      // -----------------------------------------------------------------------
      // 3. TWO SUPPORTING VIEWS
      // -----------------------------------------------------------------------
      const supportGrid = el(doc, "div", null, "grid grid-cols-1 md:grid-cols-2 gap-4");

      // Supporting View 1: Telemetry KPI Cards
      const cardA = el(doc, "div", null, "bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between");
      cardA.append(
        el(doc, "h4", "Supporting View 1: M-Lab Bandwidth Distribution", "text-xs font-bold uppercase tracking-wider text-slate-500 mb-3")
      );

      const kpiList = el(doc, "div", null, "space-y-3");
      const makeKpi = (label, val, unit, barPct, color) => {
        const item = el(doc, "div", null, "bg-slate-50 p-2.5 rounded-xl border border-slate-100");
        const top = el(doc, "div", null, "flex justify-between items-center text-xs");
        top.append(el(doc, "span", label, "text-slate-600 font-medium"), el(doc, "strong", `${val} ${unit}`, "font-mono font-bold text-slate-900"));
        const barWrap = el(doc, "div", null, "w-full bg-slate-200 rounded-full h-1.5 mt-2 overflow-hidden");
        const bar = el(doc, "div", null, `h-full rounded-full ${color}`);
        bar.style.width = `${Math.min(100, Math.max(5, barPct))}%`;
        barWrap.append(bar);
        item.append(top, barWrap);
        return item;
      };

      kpiList.append(
        makeKpi("Download Speed (P50 Median)", dP50 ? Number(dP50).toFixed(1) : "–", "Mbps", dP50 ? (dP50 / 40) * 100 : 20, "bg-emerald-600"),
        makeKpi("Lower Quartile (P25 Bottleneck)", dP25 ? Number(dP25).toFixed(1) : "–", "Mbps", dP25 ? (dP25 / 40) * 100 : 10, "bg-amber-600"),
        makeKpi("Round-Trip Network Latency", latP50 ? Number(latP50).toFixed(0) : "–", "ms", latP50 ? Math.min(100, (latP50 / 150) * 100) : 30, "bg-indigo-600")
      );
      cardA.append(kpiList);
      cardA.append(el(doc, "p", "Higher latency (>60ms) and low P25 indicate severe packet loss on cellular towers outside capital centers.", "text-[11px] text-slate-400 mt-3 pt-2 border-t border-slate-100"));

      // Supporting View 2: Classroom Consequence Feasibility Audit
      const cardB = el(doc, "div", null, "bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between");
      cardB.append(
        el(doc, "h4", "Supporting View 2: Classroom Consequence Audit", "text-xs font-bold uppercase tracking-wider text-slate-500 mb-3")
      );

      const streamsSupported = dP50 ? Math.max(1, Math.floor(dP50 / 3.5)) : 2;
      const pupilsPerStream = Math.round(400 / streamsSupported);

      const auditBox = el(doc, "div", null, "space-y-2.5");
      const stat1 = el(doc, "div", null, "p-3 bg-amber-50/80 border border-amber-200 rounded-xl");
      stat1.append(
        el(doc, "span", "Max Concurrent 720p Video Streams:", "text-[11px] text-amber-800 font-bold block"),
        el(doc, `${streamsSupported} Simultaneous Video Feeds`, "text-lg font-black text-amber-950 font-mono mt-0.5"),
        el(doc, `For an entire primary school of 400 pupils, this bandwidth forces ~${pupilsPerStream} pupils per stream, making individual 1:1 online device instruction mathematically impossible.`, "text-[11px] text-amber-900 mt-1 leading-snug")
      );

      const stat2 = el(doc, "div", null, "p-3 bg-slate-50 border border-slate-200 rounded-xl");
      stat2.append(
        el(doc, "span", "Recommended Pedagogical Architecture:", "text-[11px] text-slate-600 font-bold block"),
        el(doc, "Offline Sneakernet / Local Wi-Fi Hotspots", "text-sm font-black text-slate-900 mt-0.5"),
        el(doc, "Pre-load Digital Public Goods (Kolibri, Kiwix) on Micro-SD cards or school servers to bypass live cellular airtime costs.", "text-[11px] text-slate-500 mt-1 leading-snug")
      );

      auditBox.append(stat1, stat2);
      cardB.append(auditBox);

      supportGrid.append(cardA, cardB);
      container.append(supportGrid);

      host.replaceChildren(container);
    } catch (err) {
      if (id === requestId) {
        host.replaceChildren(el(doc, "p", `Could not render National Connectivity Snapshot: ${err.message}`, "p-4 text-xs text-rose-700 bg-rose-50 rounded-lg"));
      }
    }
  }

  render(state.get());
  const unsubscribe = state.subscribe((s, changed) => {
    if (changed.includes("country")) render(s);
  });
  return () => {
    requestId++;
    unsubscribe();
  };
}
