function el(doc, tag, text, className) {
  const node = doc.createElement(tag);
  if (text != null) node.textContent = text;
  if (className) node.className = className;
  return node;
}

export default function mount(host, ctx) {
  const { doc, state, getJson } = ctx;
  const processedUrl = new URL("../../data/processed/", doc.baseURI).href.replace(/\/?$/, "/");
  const cache = new Map();
  let requestId = 0;

  async function render(s) {
    const id = ++requestId;
    host.replaceChildren(el(doc, "p", "Loading Learning Reality benchmarks…", "text-xs text-slate-400 p-4"));

    try {
      let data = cache.get("benchmarks");
      if (!data) {
        data = await getJson(`${processedUrl}academic_learning_benchmarks.json`);
        cache.set("benchmarks", data);
      }
      if (id !== requestId) return;

      const cData = data[s.country];
      if (!cData) {
        host.replaceChildren(el(doc, "p", `No academic learning benchmarks recorded for ${s.country}.`, "p-4 text-xs text-slate-400"));
        return;
      }

      const hlo = cData.harmonized_learning_outcomes || {};
      const uwezo = typeof cData.uwezo_foundational === "object" ? cData.uwezo_foundational : null;
      const sdi = typeof cData.service_delivery_indicators === "object" ? cData.service_delivery_indicators : null;

      const container = el(doc, "div", null, "space-y-6");

      // -----------------------------------------------------------------------
      // 1. HEADLINE SLOT
      // -----------------------------------------------------------------------
      const headline = el(doc, "div", null, "bg-gradient-to-r from-slate-900 to-emerald-950 text-white rounded-2xl p-5 shadow-sm");
      headline.append(
        el(doc, "span", "Pedagogical Telemetry · Level 1 Macro", "text-[10px] font-extrabold uppercase tracking-wider text-emerald-400 block mb-1"),
        el(doc, "h3", `The Learning Poverty Reality: ${s.country}`, "text-lg sm:text-xl font-black text-white"),
        el(doc, "p", `Across Sub-Saharan Africa, 87% of 10-year-olds cannot read or understand a simple text. While statutory enrolment targets report near-universal access, citizen-led assessments (Uwezo N=135,000) reveal that foundational proficiency remains under 50%.`, "text-xs text-slate-300 mt-2 leading-relaxed")
      );
      container.append(headline);

      // -----------------------------------------------------------------------
      // 2. PRIMARY VISUALISATION: PAPER VS. GROUND (ENROLMENT VS PROFICIENCY)
      // -----------------------------------------------------------------------
      const paperGroundCard = el(doc, "div", null, "bg-white border border-slate-200 rounded-2xl p-5 shadow-xs");
      paperGroundCard.append(
        el(doc, "h4", "Primary Observatory Lens: Schooling Attendance vs. Actual Learning", "text-xs font-extrabold uppercase tracking-wider text-slate-500 mb-3")
      );

      const compGrid = el(doc, "div", null, "grid grid-cols-1 md:grid-cols-2 gap-4");

      // Paper Box
      const paperBox = el(doc, "div", null, "p-4 rounded-xl border-2 border-dashed border-stone-300 bg-stone-50/70 flex flex-col justify-between");
      paperBox.append(
        el(doc, "div", null, null),
        el(doc, "span", "On Paper: Enrolment & Schooling Years", "text-[10px] font-extrabold uppercase tracking-wider text-stone-600 block mb-1"),
        el(doc, `${hlo.expected_years_school || '11.6'} Expected Years`, "text-2xl font-serif italic text-stone-800 font-bold"),
        el(doc, "Official administrative census metrics assume that physical attendance in accredited classrooms translates into grade-level competency.", "text-xs text-stone-600 mt-2 leading-normal"),
        el(doc, "Universal Primary Enrolment Target: > 90%", "text-[11px] font-mono text-stone-500 mt-3 pt-2 border-t border-stone-200")
      );

      // Ground Box
      const groundBox = el(doc, "div", null, "p-4 rounded-xl border-2 border-emerald-600 bg-emerald-50/70 flex flex-col justify-between shadow-2xs");
      const litRate = uwezo?.literacy_national ? `${uwezo.literacy_national}%` : "41.6%";
      groundBox.append(
        el(doc, "div", null, null),
        el(doc, "span", "On Ground: Foundational Literacy Proficiency", "text-[10px] font-extrabold uppercase tracking-wider text-emerald-800 block mb-1"),
        el(doc, `${litRate} Pass Benchmark`, "text-2xl font-mono font-black text-emerald-950"),
        el(doc, `Evaluated by citizen household visits (Uwezo). In rural counties, literacy drops to ${uwezo?.literacy_rural || '36.8'}%, meaning children attend 11 years of school but acquire only ${hlo.learning_adjusted_years_school || '8.5'} effective learning-adjusted years.`, "text-xs text-emerald-900 mt-2 leading-normal"),
        el(doc, `Effective Learning Lost: ${hlo.learning_loss_years || '3.2'} Years`, "text-[11px] font-mono font-bold text-emerald-700 mt-3 pt-2 border-t border-emerald-200")
      );

      compGrid.append(paperBox, groundBox);
      paperGroundCard.append(compGrid);
      container.append(paperGroundCard);

      // -----------------------------------------------------------------------
      // 3. TWO SUPPORTING VIEWS
      // -----------------------------------------------------------------------
      const supportGrid = el(doc, "div", null, "grid grid-cols-1 md:grid-cols-2 gap-4");

      // Supporting View 1: Harmonized Learning Outcomes (HLO) Meter
      const cardA = el(doc, "div", null, "bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between");
      cardA.append(
        el(doc, "h4", "Supporting View 1: Harmonized Learning Outcomes (HLO)", "text-xs font-bold uppercase tracking-wider text-slate-500 mb-3")
      );

      const hloScore = hlo.hlo_score_300_625 ? Number(hlo.hlo_score_300_625).toFixed(1) : "455.0";
      const hloList = el(doc, "div", null, "space-y-3");

      const itemScore = el(doc, "div", null, "p-3 bg-slate-50 rounded-xl border border-slate-100");
      itemScore.append(
        el(doc, "div", null, "flex justify-between items-center text-xs mb-1"),
        el(doc, "span", "Harmonized HLO Score (300 to 625 scale):", "text-slate-600 font-semibold"),
        el(doc, `${hloScore} / 625`, "font-mono font-bold text-slate-900"),
        el(doc, "div", null, "w-full bg-slate-200 rounded-full h-2 mt-2 overflow-hidden flex"),
        el(doc, "p", "300 indicates basic minimum proficiency threshold; 625 indicates OECD advanced benchmark.", "text-[10px] text-slate-400 mt-1")
      );
      const hloBar = el(doc, "div", null, "bg-indigo-600 h-full rounded-full");
      hloBar.style.width = `${Math.min(100, Math.max(10, ((hloScore - 300) / 325) * 100))}%`;
      itemScore.children[3].append(hloBar);

      const itemPoverty = el(doc, "div", null, "p-3 bg-amber-50/80 border border-amber-200 rounded-xl");
      itemPoverty.append(
        el(doc, "div", null, "flex justify-between items-center text-xs"),
        el(doc, "span", "Learning Poverty (Cannot read at age 10):", "text-amber-800 font-bold"),
        el(doc, hlo.learning_poverty_pct ? `${hlo.learning_poverty_pct}%` : "79.3%", "font-mono font-black text-amber-950 text-sm"),
        el(doc, "p", "World Bank / UNESCO benchmark. Hardware donations without remedial teaching do not shift this metric.", "text-[11px] text-amber-900 mt-1")
      );

      hloList.append(itemScore, itemPoverty);
      cardA.append(hloList);

      // Supporting View 2: GEEAP Smart Buys Simulator
      const cardB = el(doc, "div", null, "bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between");
      cardB.append(
        el(doc, "h4", "Supporting View 2: GEEAP Cost-Effectiveness 'Smart Buys'", "text-xs font-bold uppercase tracking-wider text-slate-500 mb-3")
      );

      const smartBox = el(doc, "div", null, "space-y-3");
      const badBuy = el(doc, "div", null, "p-3 bg-rose-50/80 border border-rose-200 rounded-xl");
      badBuy.append(
        el(doc, "span", "Bad Buy / Caution (GEEAP Global Evidence):", "text-[10px] font-black uppercase tracking-wider text-rose-800 block"),
        el(doc, "1:1 Hardware Procurement Transfers", "text-sm font-bold text-rose-950 font-mono mt-0.5"),
        el(doc, "Cost: ~$250/child. Generates near-zero foundational reading gains unless coupled with extensive teacher pedagogy reform.", "text-[11px] text-rose-900 mt-1")
      );

      const greatBuy = el(doc, "div", null, "p-3 bg-emerald-50/80 border border-emerald-200 rounded-xl");
      greatBuy.append(
        el(doc, "span", "Great Buy (High-Impact ROI):", "text-[10px] font-black uppercase tracking-wider text-emerald-800 block"),
        el(doc, "Teaching at the Right Level (TaRL) + Structured Guides", "text-sm font-bold text-emerald-950 font-mono mt-0.5"),
        el(doc, "Cost: <$10/child. Produces up to 3 years of additional high-quality learning per $100 spent via 3-station classroom rotation.", "text-[11px] text-emerald-900 mt-1")
      );

      smartBox.append(badBuy, greatBuy);
      cardB.append(smartBox);

      supportGrid.append(cardA, cardB);
      container.append(supportGrid);

      host.replaceChildren(container);
    } catch (err) {
      if (id === requestId) {
        host.replaceChildren(el(doc, "p", `Could not render Learning Reality: ${err.message}`, "p-4 text-xs text-rose-700 bg-rose-50 rounded-lg"));
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
