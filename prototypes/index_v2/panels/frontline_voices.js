const VOICES = [
  {
    quote: "I spend about 100 Kenya shillings of my own airtime every week just to send homework instructions to parents on WhatsApp. It is not reimbursed. It comes from my personal salary. This is my classroom internet budget.",
    author: "Primary Teacher",
    loc: "Nakuru County, Kenya",
    citation: "UNESCO Global Education Coalition / AoA Survey (2024)",
    pillar: "Pillar 3: Cost & Sustainability",
    tag: "Informal Airtime Tax"
  },
  {
    quote: "The government sent 40 tablets to our school. The headmaster locked them in the storeroom because there is no insurance and we are personally liable if one is broken or stolen. They have been there for two years.",
    author: "Senior Teacher",
    loc: "Turkana County, Kenya",
    citation: "KEPSHA / EdTech Hub DLP Follow-up Audit (2022)",
    pillar: "Pillar 1: Coordination & Governance",
    tag: "Device Incarceration"
  },
  {
    quote: "We only have power for two hours in the morning before the grid cuts. I charged my phone the night before to show the students the science simulation. By the time the class started, the battery had died.",
    author: "Science Teacher",
    loc: "Machakos County, Kenya",
    citation: "EdTech Hub / FCDO Rural Teacher Audit (2023)",
    pillar: "Pillar 2: Infrastructure & Power",
    tag: "Grid Unreliability"
  },
  {
    quote: "When I play the AI reading tutor for my Grade 2 students, it pronounces their names wrong and doesn't understand when they speak. The children laugh, but they stop trying. They think they are the problem.",
    author: "Early Grade Educator",
    loc: "Kisumu County, Kenya",
    citation: "Masakhane Research Collective / AfroBench Field Notes (2024)",
    pillar: "Pillar 5: Content & Mother Tongue",
    tag: "Language Mismatch"
  },
  {
    quote: "In a class of 68 children, the rotation model with radio and workbooks is the only method that reaches every child. App-based tools requiring 1:1 screen time force me to manage 68 devices simultaneously. That is not teaching.",
    author: "Head of Pedagogy",
    loc: "Siaya County, Kenya",
    citation: "Comparative Education Review / Field Corroboration (2023)",
    pillar: "Pillar 4: Pedagogical Capacity",
    tag: "Rotation Pedagogy"
  },
  {
    quote: "The school enrolled my children in an app that now sends me commercial adverts. I never gave parental consent. I did not know their names and attendance scores were uploaded to an overseas server.",
    author: "Parent / SMC Representative",
    loc: "Mombasa, Kenya",
    citation: "Kenya DPA Civil Society Submissions / UNICEF Child Safeguarding (2024)",
    pillar: "Pillar 6: Data & Child Safety",
    tag: "Commercial Safeguarding"
  }
];

function el(doc, tag, text, className) {
  const node = doc.createElement(tag);
  if (text != null) node.textContent = text;
  if (className) node.className = className;
  return node;
}

export default function mount(host, ctx) {
  const { doc } = ctx;
  let activeIndex = 0;

  function render() {
    const item = VOICES[activeIndex];
    const container = el(doc, "div", null, "voices-container");

    const header = el(doc, "div", null, "voices-header");
    const countBadge = el(doc, "span", `${activeIndex + 1} of ${VOICES.length} Testimonies`, "badge-cliff");
    const pillarBadge = el(doc, "span", `${item.pillar} · ${item.tag}`, "voice-tag");
    header.append(countBadge, pillarBadge);

    const bq = el(doc, "blockquote", `“${item.quote}”`, "voice-quote");

    const meta = el(doc, "div", null, "voice-meta");
    const authorEl = el(doc, "strong", `${item.author} — ${item.loc}`, "voice-author");
    const citeEl = el(doc, "cite", item.citation, "voice-cite");
    meta.append(authorEl, citeEl);

    // Nav buttons
    const nav = el(doc, "div", null, "voice-controls");
    const btnPrev = el(doc, "button", "← Previous Testimony", "voice-nav-btn");
    btnPrev.type = "button";
    btnPrev.onclick = () => {
      activeIndex = (activeIndex - 1 + VOICES.length) % VOICES.length;
      render();
    };

    const btnNext = el(doc, "button", "Next Testimony →", "voice-nav-btn");
    btnNext.type = "button";
    btnNext.onclick = () => {
      activeIndex = (activeIndex + 1) % VOICES.length;
      render();
    };

    nav.append(btnPrev, btnNext);

    container.append(header, bq, meta, nav);
    host.replaceChildren(container);
  }

  render();
  return () => {};
}
