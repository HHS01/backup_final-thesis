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
    host.replaceChildren(el(doc, "p", "Loading Macro-Fiscal & Aid data…", "text-xs text-slate-400 p-4"));

    try {
      let data = cache.get("macro_fiscal");
      if (!data) {
        data = await getJson(`${processedUrl}macro_fiscal_ecosystem.json`);
        cache.set("macro_fiscal", data);
      }
      if (id !== requestId) return;

      const countryData = data.countries?.[s.country];
      if (!countryData) {
        host.replaceChildren(
          el(doc, "p", `No detailed macro-fiscal profile available for ${s.country}.`, "p-4 text-xs text-slate-400")
        );
        return;
      }

      const df = countryData.domestic_fiscal || {};
      const ea = countryData.external_assistance || {};
      const rc = countryData.recurrent_cliff_analysis || {};
      const mc = countryData.macro_context || {};
      const ratio = rc.domestic_edu_to_comm_ratio || 40.1;

      const container = el(doc, "div", null, "space-y-6");

      // -----------------------------------------------------------------------
      // 1. HEADLINE SLOT
      // -----------------------------------------------------------------------
      const headline = el(doc, "div", null, "bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl p-5 shadow-sm");
      headline.append(
        el(doc, "span", "Macro-Fiscal Telemetry · Level 1 Macro", "text-[10px] font-extrabold uppercase tracking-wider text-amber-400 block mb-1"),
        el(doc, "h3", `The Digital Recurrent Cliff: ${countryData.country_name || s.country}`, "text-lg sm:text-xl font-black text-white"),
        el(doc, "p", rc.narrative || "National budget allocations demonstrate strong domestic education commitment alongside severe ICT infrastructure under-investment, locking schools in recurring maintenance deficits.", "text-xs text-slate-300 mt-2 leading-relaxed")
      );
      container.append(headline);

      // -----------------------------------------------------------------------
      // 2. PRIMARY VISUALISATION: PAPER VS. GROUND (40:1 BAR RATIO)
      // -----------------------------------------------------------------------
      const paperGroundCard = el(doc, "div", null, "bg-white border border-slate-200 rounded-2xl p-5 shadow-xs");
      paperGroundCard.append(
        el(doc, "h4", "Primary Observatory Lens: Domestic Financing Asymmetry", "text-xs font-extrabold uppercase tracking-wider text-slate-500 mb-3")
      );

      const compGrid = el(doc, "div", null, "grid grid-cols-1 md:grid-cols-2 gap-4");

      // Paper Box: Education Commitment
      const paperBox = el(doc, "div", null, "p-4 rounded-xl border-2 border-dashed border-stone-300 bg-stone-50/70 flex flex-col justify-between");
      paperBox.append(
        el(doc, "div", null, null),
        el(doc, "span", "On Paper: Domestic Education Budget", "text-[10px] font-extrabold uppercase tracking-wider text-stone-600 block mb-1"),
        el(doc, `${df.education_pct_budget != null ? df.education_pct_budget + '%' : '18.4%'} of Budget`, "text-2xl font-serif italic text-stone-800 font-bold"),
        el(doc, "High political commitment to universal schooling (exceeds the 15-20% Incheon Declaration UNESCO benchmark).", "text-xs text-stone-600 mt-2 leading-normal"),
        el(doc, `GDP Share: ${df.education_pct_gdp || '3.8'}% · IMF COFOG 709`, "text-[11px] font-mono text-stone-500 mt-3 pt-2 border-t border-stone-200")
      );

      // Ground Box: ICT Communications Bottleneck
      const groundBox = el(doc, "div", null, "p-4 rounded-xl border-2 border-amber-500 bg-amber-50/70 flex flex-col justify-between shadow-2xs");
      groundBox.append(
        el(doc, "div", null, null),
        el(doc, "span", "On Ground: Central ICT Allocation", "text-[10px] font-extrabold uppercase tracking-wider text-amber-800 block mb-1"),
        el(doc, `${df.communication_pct_budget != null ? df.communication_pct_budget + '%' : '0.46%'} of Budget`, "text-2xl font-mono font-black text-amber-950"),
        el(doc, `Produces a ${ratio}:1 Domestic Financing Asymmetry. Because ICT receives under 0.5% of central revenue, schools receive zero recurring subsidies for Wi-Fi bills, repairs, or solar batteries.`, "text-xs text-amber-900 mt-2 leading-normal"),
        el(doc, `Cliff Tension: ${rc.cliff_risk_tier || 'High Structural Lock'}`, "text-[11px] font-mono font-bold text-amber-800 mt-3 pt-2 border-t border-amber-200")
      );

      compGrid.append(paperBox, groundBox);
      paperGroundCard.append(compGrid);

      // Visual Asymmetry Ratio Bar
      const ratioBarWrap = el(doc, "div", null, "mt-4 pt-4 border-t border-slate-100");
      const barHeader = el(doc, "div", null, "flex justify-between items-center text-xs mb-1.5");
      barHeader.append(
        el(doc, "span", "Domestic Expenditure Asymmetry (Education vs. ICT Outlays):", "font-bold text-slate-700"),
        el(doc, `${ratio} : 1 Ratio`, "font-mono font-black text-amber-700 text-sm")
      );
      const ratioBar = el(doc, "div", null, "w-full bg-slate-200 rounded-full h-3 flex overflow-hidden");
      const segEdu = el(doc, "div", null, "bg-stone-500 h-full");
      segEdu.style.width = "97.5%";
      segEdu.title = `Education Budget: ${df.education_pct_budget}%`;
      const segIct = el(doc, "div", null, "bg-amber-500 h-full");
      segIct.style.width = "2.5%";
      segIct.title = `Communications Budget: ${df.communication_pct_budget}%`;
      ratioBar.append(segEdu, segIct);
      ratioBarWrap.append(barHeader, ratioBar);
      paperGroundCard.append(ratioBarWrap);

      container.append(paperGroundCard);

      // -----------------------------------------------------------------------
      // 3. TWO SUPPORTING VIEWS
      // -----------------------------------------------------------------------
      const supportGrid = el(doc, "div", null, "grid grid-cols-1 md:grid-cols-2 gap-4");

      // Supporting View 1: External Aid Asymmetry (IATI)
      const cardA = el(doc, "div", null, "bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between");
      cardA.append(
        el(doc, "h4", "Supporting View 1: International Aid Inflow Asymmetry (IATI)", "text-xs font-bold uppercase tracking-wider text-slate-500 mb-3")
      );

      const eduAid = ea.cumulative_education_aid_usd_m ? `$${ea.cumulative_education_aid_usd_m.toFixed(1)}M` : "$1,016.6M";
      const ictAid = ea.cumulative_ict_aid_usd_m ? `$${ea.cumulative_ict_aid_usd_m.toFixed(1)}M` : "$4.8M";

      const aidList = el(doc, "div", null, "space-y-3");
      const makeAidRow = (label, val, note, col) => {
        const item = el(doc, "div", null, "p-3 bg-slate-50 rounded-xl border border-slate-100");
        const top = el(doc, "div", null, "flex justify-between items-center text-xs");
        top.append(el(doc, "span", label, "text-slate-600 font-semibold"), el(doc, "strong", val, `font-mono font-black text-sm ${col}`));
        item.append(top, el(doc, "p", note, "text-[11px] text-slate-400 mt-1 leading-tight"));
        return item;
      };

      aidList.append(
        makeAidRow("Cumulative Education Aid (2017–2024)", eduAid, "Normalized across 29,388 IATI development transactions.", "text-indigo-900"),
        makeAidRow("Cumulative Central ICT / Telecom Aid", ictAid, "External donors heavily fund classroom hardware, but fund zero operational bandwidth.", "text-amber-800"),
        makeAidRow("2020 COVID Emergency Surge", ea.covid_2020_education_aid_usd_m ? `$${ea.covid_2020_education_aid_usd_m.toFixed(1)}M` : "$244.0M", "Emergency aid spiked hardware donations with no long-term counterpart budget.", "text-slate-700")
      );
      cardA.append(aidList);

      // Supporting View 2: The Structural Recurrent Lock
      const cardB = el(doc, "div", null, "bg-white border border-slate-200 rounded-2xl p-5 shadow-xs flex flex-col justify-between");
      cardB.append(
        el(doc, "h4", "Supporting View 2: The Post-Donor 'Recurrent Cliff'", "text-xs font-bold uppercase tracking-wider text-slate-500 mb-3")
      );

      const lockBox = el(doc, "div", null, "space-y-3");
      const lock1 = el(doc, "div", null, "p-3 bg-rose-50/80 border border-rose-200 rounded-xl");
      lock1.append(
        el(doc, "span", "The 18-Month Project Mortality Mechanism:", "text-[11px] font-bold text-rose-900 block"),
        el(doc, "Capital Grants End $\\rightarrow$ Headmasters Tax Teachers", "text-sm font-black text-rose-950 font-mono mt-0.5"),
        el(doc, "When donor grants close, software license renewals, SIM airtime bundles, and screen replacements fall entirely on school petty cash. Without central ICT line items, tablets are locked in storerooms to avoid teacher liability.", "text-[11px] text-rose-900 mt-1 leading-snug")
      );

      const lock2 = el(doc, "div", null, "p-3 bg-emerald-50/80 border border-emerald-200 rounded-xl");
      lock2.append(
        el(doc, "span", "Policy Remedy:", "text-[11px] font-bold text-emerald-900 block"),
        el(doc, "Pre-flight SMC Feasibility Memorandums", "text-sm font-black text-emerald-950 mt-0.5"),
        el(doc, "Require incoming donor projects to include 3-year recurring airtime and maintenance endowments before school boards sign adoption covenants.", "text-[11px] text-emerald-800 mt-1 leading-snug")
      );

      lockBox.append(lock1, lock2);
      cardB.append(lockBox);

      supportGrid.append(cardA, cardB);
      container.append(supportGrid);

      host.replaceChildren(container);
    } catch (err) {
      if (id === requestId) {
        host.replaceChildren(el(doc, "p", `Could not render Macro-Fiscal view: ${err.message}`, "p-4 text-xs text-rose-700 bg-rose-50 rounded-lg"));
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
