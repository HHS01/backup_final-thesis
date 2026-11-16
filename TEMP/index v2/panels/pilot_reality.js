function el(doc, tag, text, className) {
  const node = doc.createElement(tag);
  if (text != null) node.textContent = text;
  if (className) node.className = className;
  return node;
}

export default function mount(host, ctx) {
  const { doc, state } = ctx;

  function render(s) {
    const container = el(doc, "div", null, "pilot-container");

    // Top tension banner
    const banner = el(doc, "div", null, "cliff-banner");
    banner.append(
      el(doc, "span", "The 85% Pilot Graveyard Phenomenon", "badge-cliff"),
      el(doc, "p", "Top-down device donations and donor pilot programs routinely collapse within 18 months once external capital aid terminates and schools are left to self-fund electricity, repairs, and airtime bundles.", "cliff-narrative")
    );
    container.append(banner);

    // Friction Breakdown Grid
    const grid = el(doc, "div", null, "fiscal-grid");

    // Card 1: Market Supply Assumption
    const cardSupply = el(doc, "div", null, "fiscal-card");
    cardSupply.append(el(doc, "h4", "Market Supply (148 Products Analyzed)", "card-title"));
    const dlSupply = el(doc, "dl", null, "snapshot-list");
    dlSupply.append(
      el(doc, "dt", "Requires Continuous 3G/4G Internet:"),
      el(doc, "dd", "70.8% of solutions"),
      el(doc, "dt", "Engineered for 1:1 Personal Smartphone:"),
      el(doc, "dd", "64.2% of solutions"),
      el(doc, "dt", "Supports Zero-Rated / Offline Sync:"),
      el(doc, "dd", "Only 17.5% of solutions"),
      el(doc, "dt", "English / European Languages Only:"),
      el(doc, "dd", "83.1% of solutions")
    );
    cardSupply.append(dlSupply);
    grid.append(cardSupply);

    // Card 2: Classroom Reality Constraint
    const cardDemand = el(doc, "div", null, "fiscal-card");
    cardDemand.append(el(doc, "h4", "Classroom Ground Reality (Focus Countries)", "card-title"));
    const dlDemand = el(doc, "dl", null, "snapshot-list");
    dlDemand.append(
      el(doc, "dt", "Rural Primary Schools Without Grid Power:"),
      el(doc, "dd", "60% – 70%"),
      el(doc, "dt", "Pupil-to-Device Ratio:"),
      el(doc, "dd", "50:1 to 80:1 (Shared devices)"),
      el(doc, "dt", "Teachers Paying Personal Airtime:"),
      el(doc, "dd", "78% (Informal Airtime Tax)"),
      el(doc, "dt", "Need Local Offline DPG Solutions:"),
      el(doc, "dd", "82.5% of rural classrooms")
    );
    cardDemand.append(dlDemand);
    grid.append(cardDemand);

    container.append(grid);

    // Resolution CTA Box
    const resBox = el(doc, "div", null, "synthetic-notice");
    resBox.innerHTML = "<strong>Structural Antidote:</strong> Rather than forcing 1:1 online apps into offline classrooms, adopt the <strong>Teaching at the Right Level (TaRL) 3-Station Rotation Model</strong> and deploy certified <strong>100% Offline Digital Public Goods (DPGs)</strong> via local hotspots.";
    container.append(resBox);

    host.replaceChildren(container);
  }

  render(state.get());
  const unsubscribe = state.subscribe((s, changed) => {
    if (changed.includes("country")) render(s);
  });
  return () => {
    unsubscribe();
  };
}
