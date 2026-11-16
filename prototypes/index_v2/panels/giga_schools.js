const STATUS_ORDER = { no: 0, moderate: 1, good: 2, unknown: 3 };

function element(doc, tag, text, className) {
  const node = doc.createElement(tag);
  if (text != null) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function metric(value, digits = 1) {
  return value == null ? "Not measured" : Number(value).toFixed(digits);
}

export default function mount(host, ctx) {
  const { doc, state, getJson, schoolDataUrl } = ctx;
  const cache = new Map();
  let requestId = 0;

  async function render(s) {
    const id = ++requestId;
    host.replaceChildren(element(doc, "p", "Loading synthetic school placeholders…", "slot"));
    try {
      let promise = cache.get(s.country);
      if (!promise) {
        promise = getJson(`${schoolDataUrl}${s.country}_schools.json`);
        cache.set(s.country, promise);
      }
      const schools = await promise;
      if (!Array.isArray(schools)) throw new Error("Unexpected school-data format");
      if (id !== requestId) return;

      const visible = s.region ? schools.filter((school) => school.admin1_id === s.region) : schools;
      const measured = visible.filter((school) => school.download_median_30d_mbps != null);
      const connected = visible.filter((school) => school.connectivity_govt === "Yes");
      const regionName = visible[0]?.admin1_boundary || "selected region";
      const summary = element(doc, "p",
        `${s.region ? `${regionName} · ` : ""}${visible.length} placeholder schools · ${connected.length} reported connected · ${measured.length} with recent meter readings`,
        "muted");
      const notice = element(doc, "p",
        "Synthetic demonstration records only. Names, school locations, and connectivity readings are generated; they are not observations about real schools.",
        "synthetic-notice");
      const table = element(doc, "table");
      const head = element(doc, "thead");
      const headerRow = element(doc, "tr");
      for (const label of ["School", "Level", "Reported connection", "30-day download (Mbps)", "Status"]) {
        headerRow.append(element(doc, "th", label));
      }
      head.append(headerRow);
      const body = element(doc, "tbody");
      const sorted = visible.slice().sort((a, b) =>
        (STATUS_ORDER[a.connectivity_status] ?? 4) - (STATUS_ORDER[b.connectivity_status] ?? 4)
        || a.school_name.localeCompare(b.school_name));
      for (const school of sorted.slice(0, 40)) {
        const row = element(doc, "tr");
        row.append(
          element(doc, "td", school.school_name),
          element(doc, "td", school.education_level),
          element(doc, "td", school.connectivity_govt),
          element(doc, "td", metric(school.download_median_30d_mbps)),
          element(doc, "td", school.connectivity_status),
        );
        body.append(row);
      }
      table.append(head, body);
      host.replaceChildren(summary, notice, table);
      if (sorted.length > 40) {
        host.append(element(doc, "p", `Showing 40 of ${sorted.length} placeholder schools.`, "panel-meta"));
      }
      if (!visible.length) {
        host.replaceChildren(
          summary,
          notice,
          element(doc, "p", "No synthetic schools were generated for this region.", "slot"),
        );
      }
    } catch (error) {
      if (id === requestId) {
        host.replaceChildren(element(doc, "p", `Synthetic school data could not be loaded: ${error.message}`, "slot"));
      }
    }
  }

  render(state.get());
  const unsubscribe = state.subscribe((s, changed) => {
    if (changed.some((key) => ["country", "region"].includes(key))) render(s);
  });
  return () => {
    requestId++;
    unsubscribe();
  };
}
