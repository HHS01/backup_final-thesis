# Analytical Framework 2: Project Evaluation

**Project:** Mapping the EdTech Landscape in Sub-Saharan Africa and MENA: Bridging Macro-Level Assessment, the 6-Pillars Framework, and Grassroots Realities  
**Master:** ICT for Development and Social Good (UniTO / COREP / Impactskills)

---

## TECHNOLOGY FOCUS

### 1. What is the expected technology output?

* **Live Interactive Web Explorer (`EEA_2`):** A lightweight, client-side dashboard hosted on GitHub Pages displaying student AI adoption, screen-time distribution, and digital guidance policies across 85 educational systems drawn from OECD PISA 2025 data.
* **Automated 6-Pillars Data Pipeline (`fetch_6pillars_pipeline.py`):** An open-source Python engine querying and caching indicators across 69 nations (48 SSA, 21 MENA) aligned with UNESCO's Six Pillars of Digital Transformation, producing three processed datasets: `indicators_timeseries.csv`, `latest_country_profiles_6pillars.csv`, and `wb_digital_education_projects.csv`.
* **Decision-Support Matrix / Multi-Stakeholder Alignment Rubric:** A practical rubric mapping school-level connectivity constraints to appropriate EdTech delivery modalities, bridging startup product design with verified teacher classroom conditions for ministries and regional incubators.

---

### 2. What is the expected contribution of technology in relation to the "social good" goals?

* **Enabling new practices — Informed Public Resource Allocation:** Prevents ministries and donors from misallocating capital toward high-bandwidth, cloud-only systems that fail in off-grid settings by surfacing context-specific evidence.
* **Widening accessibility — Democratizing Strategic Insight:** Equips grassroots startups, local educators, and civil society with free, open development intelligence typically locked behind expensive proprietary consultancy reports.
* **Enhancing existing practices — Promoting Educational Equity:** Centers low-connectivity, offline-first, and marginalized learners who are ignored by mainstream digital platforms, making them visible within policy and planning processes.

---

### 3. What socio-political visions and goals lie behind the introduction or use of technology? Are they the same for all actors involved?

The technology is underpinned by an **ICT4D equity vision**: the belief that open data and transparent analytical infrastructure can correct structural information asymmetries that disadvantage Global South education systems.

**No — the visions differ substantially across actors:**

* **Multilateral Donors & Assessment Agencies (OECD, World Bank, UNESCO):** Pursue standardization, cross-national comparability, and evidence-based governance. Their metrics implicitly favor high-income institutional models (e.g., PISA sampling only enrolled 15-year-olds), potentially marginalizing the 30–50% of out-of-school SSA youth.
* **National Ministries of Education & ICT:** Primarily concerned with demonstrating compliance with donor frameworks to unlock funding, often prioritizing visible hardware procurement (CapEx) over sustained teacher training (OpEx).
* **International Tech Vendors:** Pursue market expansion and commercial lock-in; promote device-heavy, proprietary cloud solutions that generate recurring revenue but risk digital dependency in low-infrastructure contexts.
* **Grassroots Innovators & Regional Hubs (e.g., Dakar EdTech Hub):** Driven by local problem-solving — offline-first, SMS-based, or mobile-money-integrated solutions addressing real classroom constraints — but lacking procurement access and capital.
* **Teachers and Students:** Seek practical tools that work reliably given power cuts, device scarcity, and language barriers; their priorities diverge sharply from those of both vendors and policy agencies.

The research project itself takes an **explicitly critical and equity-oriented stance**, using technology (the open pipeline and dashboard) to surface the gaps between institutional visions and grassroots realities, rather than reinforcing existing power hierarchies.

---

## RESEARCH APPROACH

### 4. How does the project work with the technology?

The project engages technology across **three distinct research modes**:

1. **Observation and analysis (Tier 1):** The OECD PISA 2025 web dashboard is observed and systematically analyzed across 10 analytical domains — AI tool adoption, screen-time distribution, digital guidance policy — to extract macro behavioral and policy patterns across 85 educational systems.
2. **Development and automation (Tier 2):** The 6-Pillars pipeline (`fetch_6pillars_pipeline.py`) is actively *developed* as an original tool — querying World Bank, UIS, and ITU APIs, handling rate-limiting with disk-based caching, and producing cleaned cross-regional datasets. This includes iterative code development and testing.
3. **Evaluation and field evidence triangulation (Tier 3):** Survey instruments (teacher, provider, and expert consultation) are *designed and deployed* under the Alliance of Alliances framework, then analyzed to evaluate how macro data aligns with or diverges from micro classroom realities. The Multi-Stakeholder Alignment Rubric synthesizes findings into a practical decision-support tool.

---

### 5. Consider the people involved. What are their interests and expectations? What are their roles? What power do they hold on that technology?

| Actor | Interests & Expectations | Role | Power over Technology |
|---|---|---|---|
| **OECD / World Bank / UNESCO** | Cross-national benchmarking, evidence-based policy | Agenda-setters, data providers | High — control indicator definitions, API access, and global benchmarks |
| **National Ministries** | Donor compliance, procurement visibility | Policy implementers, gatekeepers | High — procurement and curricular authority, but limited feedback loops from classrooms |
| **Tech Vendors** | Market expansion, SaaS subscriptions | Technology suppliers | High commercially — promote proprietary solutions; low civic accountability |
| **Grassroots EdTech Startups / Hubs** | Solving real classroom constraints | Local innovators, field partners | Low institutionally — no procurement access or donor recognition, but high contextual relevance |
| **Teachers** | Reliable, low-friction tools; professional support | Frontline actors, survey respondents | Very low — directly bear the burden of power outages, device failure, and absent training |
| **Students** | Accessible, culturally relevant learning content | Beneficiaries | Lowest — no voice in procurement or curriculum design |
| **Researcher (project team)** | Producing credible, actionable open evidence | Analyst, pipeline developer, survey designer | Mediated — no institutional power, but authority through methodological rigor and open publication |

---

### 6. What kind of (participatory) methodologies are adopted in the tech design, development, test, use, and evaluation phases?

* **Participatory Survey Design (AoA framework):** Survey instruments for SSA teachers, EdTech providers, and expert consultants are co-framed within UNESCO's Global Education Coalition — ensuring questions reflect real operational bottlenecks rather than top-down assumptions.
* **Community Ground-Truthing:** Teacher and provider survey findings directly feed back into the Multi-Stakeholder Alignment Rubric, so the decision-support output is shaped by practitioner input rather than purely macro data.
* **Open-Access Dissemination:** The pipeline and dashboard are published as free, open tools — a participatory commitment to enable local actors (startups, NGOs, civil servants) to access and interrogate the data without dependency on external intermediaries.
* **Reflexive Methodological Critique:** The framework explicitly interrogates whose metrics dominate (PISA's high-income school bias) and adopts a researcher positionality that foregrounds marginalized voices — teachers, out-of-school youth, offline learners.

---

## TECHNOLOGY DEVELOPMENT

### 7. What's the role and position of the technology development team? How do they work with the other actors?

The **researcher acts as the sole developer** of the custom technology outputs (the 6-Pillars pipeline and the EEA_2 dashboard), occupying a **researcher-developer hybrid role** unusual in ICT4D projects:

* **Relationship with data providers (World Bank, UIS, ITU):** The pipeline consumes open APIs as a downstream user — no co-development, but active engagement with documentation, rate limits, and data quality gaps.
* **Relationship with field actors (AoA / UNESCO GEC):** Survey instruments are designed in alignment with the Alliance of Alliances network, positioning the researcher as a methodological collaborator rather than a neutral outsider.
* **Relationship with end users (ministries, NGOs, startups):** The technology outputs are explicitly designed *for* these actors — the dashboard is self-service, publicly hosted, requires no login, and the decision-support rubric is formatted for non-technical policy audiences.
* **Generative AI use:** AI tools were used strictly for code debugging and syntax structuring (as declared per UniTO Final Project Guidelines §26); all conceptual decisions, analytical interpretations, and framework design remain the researcher's original scholarly contribution.

---

### 8. What are the main technical constraints?

* **Target Context Realities:** Rural electrification rates below 30% in many SSA regions, high mobile data costs relative to household income, device fragility, and shared family phone ownership define the operational environment of the *users* the research serves.
* **Pipeline Constraints:** API rate-limiting and connection interruptions from World Bank, UIS, and ITU endpoints necessitate disk-based caching and retry logic to ensure reproducibility.
* **Dashboard Constraints:** The EEA_2 explorer must run purely client-side (static assets on GitHub Pages) with minimal bandwidth overhead — ruling out server-side rendering, databases, or dynamic backends.
* **Data Lag:** Macro databases carry significant time lags (1–3 years) and missing data points for rural indicators, constraining the recency and completeness of the meso-level analysis.

---

### 9. What are the main (technological / digital) barriers and divides?

* **Technical:** Intermittent power supply, device scarcity, and low bandwidth in SSA classrooms make standard ed-tech platforms (cloud-dependent, video-heavy) largely inaccessible to the majority of target beneficiaries.
* **Economic:** High mobile data costs relative to household income; institutional budgetary preference for one-off CapEx hardware purchases over sustainable OpEx (training, maintenance, licensing).
* **Upstream Data Incompleteness:** Missing data rows, irregular census intervals, and the systematic exclusion of out-of-school populations from global benchmarks (PISA's survivorship bias) create analytical blind spots.
* **Cultural / Digital Literacy:** Digital curricula predominantly published in English or French, with scarce localized materials in indigenous languages; teacher digital literacy gaps in rural contexts.
* **Cultural / Digital Acceptancy:** Resistance to AI-mediated tools in communities where trust in technology is conditioned by prior experiences of failed hardware pilots or culturally misaligned software.

---

## TECHNOLOGY ADAPTABILITY AND REPLICABILITY

### 10. Should this tech be adaptable to other social and geographical contexts? How?

**Yes.** The 6-Pillars data pipeline is modular and country-agnostic; new countries or geographic regions (e.g., South Asia, Latin America) can be incorporated simply by adding ISO codes to the indicator query configuration.

**Contextual Adaptation Model — three infrastructure tiers:**
1. *Off-Grid:* Solar-powered kits, radio/SMS delivery, and paper-digital hybrids.
2. *Low / Intermittent Connectivity:* Offline local micro-servers (e.g., Kolibri, RACHEL) preloaded with open educational resources.
3. *Connected Urban:* Hybrid platforms and guided AI pedagogical integration.

---

### 11. Scalability / transferability / replicability: are they expected? How?

**Yes — across all three dimensions:**

* **Technical Scalability:** The web explorer is deployed as static assets on GitHub Pages with zero server upkeep and no hosting expenses, supporting high traffic without performance degradation. The pipeline scales from querying a handful of countries to the full 69-nation panel.
* **Analytical Scalability:** The evaluation model scales from assessing single pilot schools to national education systems and regional economic communities (ECOWAS, SADC).
* **Replicability:** The entire codebase and datasets are open-source and open-licensed (Creative Commons), enabling other researchers, ministries, or NGOs to reproduce, extend, or localize the analysis without proprietary dependencies.

---

## ETHICS

### 12. What are the main ethical aspects concerning the development and use of the technology?

* **Avoiding Digital Extractivism:** Preventing Global South school environments from being treated merely as data sources or testbeds for foreign technology without local benefit — addressed by making all outputs open-access and directly actionable for local actors.
* **Exacerbating Educational Inequity:** Ensuring digital initiatives do not widen the gap between affluent urban students and marginalized rural or displaced learners; the framework explicitly centers offline and low-connectivity contexts.
* **Algorithmic Bias in AI:** Mitigating the risks of deploying generative AI tools trained on Western datasets that misrepresent local cultures or languages; the research critiques rather than uncritically promotes AI adoption.
* **Data Anonymity:** Ensuring all field survey responses from teachers and innovators are fully anonymized, with no personally identifiable information retained.
* **Reflexive Positionality:** Acknowledging the researcher's position as a Global North actor analyzing Global South contexts, and counteracting this through participatory survey design and integration of local actor perspectives.

---

### 13. Are there relevant regulatory obligations concerning the development and use of this technology?

* **Data Protection & Sovereignty:** Aligning with national data protection legislation — Kenya DPA, South Africa POPIA, Nigeria NDPR — to safeguard student and teacher privacy in survey data handling.
* **Child Online Protection (COP):** Ensuring minors are protected from unmonitored commercial profiling and harmful online material in school environments covered by the research.
* **Open Licensing (OER):** Adhering to open licensing frameworks (Creative Commons) to prevent vendor lock-in and enable free contextual re-appropriation of learning resources and analytical tools.
* **Generative AI Disclosure (UniTO §26):** Full compliance with the Master's programme's mandatory disclosure requirements for AI-assisted work, with interaction logs archived in supplementary materials.

---

> *Cross-reference: This document responds to all 13 questions of Analytical Framework 2 (final projects). Answers expand on Analytical Framework 1 (case studies & pilots), incorporating the three additional dimensions: socio-political visions (Q3), modalities of engagement with technology (Q4), and the researcher-as-developer positionality (Q7).*
