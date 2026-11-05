# Analytical Framework 2: Project Evaluation

**Project:** Mapping EdTech Fit Across Sub-Saharan Africa: A Six-Pillars Observatory for Context-Aware Decisions
**Programme:** First-Level Master in ICT for Development and Social Good (UniTO / COREP / Impactskills)
**Status:** Working answers for project-clinic discussion; see `Thesis_First_Draft_Concept.md` for the integrated concept.

> **Evidence status:** The project combines public macro indicators and selected secondary sources. The 800-record AoA-related dataset is calibrated synthetic data, not collected survey responses. The qualitative “field voices” display contains secondary-source excerpts requiring individual source verification. Neither should be presented as primary field evidence.

---

## Technology focus

### 1. What is the expected technology output?

The expected output is an open, browser-based **decision-support prototype** and its supporting analytical materials:

- A 69-country public-indicator pipeline and selected country profiles, structured around UNESCO's Six Pillars.
- A seven-country SSA comparison and focused discrepancy analysis.
- A classroom feasibility audit, classroom rotation planner, and resource directory.
- A scenario-based modality/lifecycle aid with assumptions disclosed.

These are analytical and planning aids, not a validated readiness score, procurement recommendation, or impact-evaluation tool. The GIGA school connectivity panel is not yet a live feed.

### 2. What is the expected contribution of technology in relation to social-good goals?

The prototype aims to make evidence and its gaps more accessible to educators, school leaders, ministries, civil society, and local providers. It can help users structure questions about electricity, connectivity costs, maintenance, class/device ratios, language, and teacher support before adopting a tool. Its contribution is a transparent decision process and open access to organized evidence—not a demonstrated reduction in inequity or improved learning outcomes.

### 3. What socio-political visions and goals lie behind the technology? Are they the same for all actors?

No. Public agencies and assessment organizations value comparability and national planning; ministries and school authorities set policy and procurement; commercial providers may prioritize market growth and recurring revenue; local organizations may focus on context-specific delivery and sustainability; teachers, learners, and families need tools that are usable, affordable, safe, and relevant. These interests can conflict over cost, data control, language, and whose evidence counts. The project takes a critical ICT4D position: use open evidence to make assumptions and exclusions visible, while avoiding the claim that the researcher can speak for all local actors.

## Research approach

### 4. How does the project work with the technology?

The project combines:
1. **Observation and analysis:** descriptive comparison of public indicators across 69 countries, selected seven-country case profiles, and a bounded PISA-derived contextual comparison whose source and coverage still require documentation.
2. **Development:** construction of the data pipeline and static web observatory, including interactive country comparisons and planning tools.
3. **Evaluation / feedback:** intended review of the prototype with relevant users, if access and time permit. No completed user evaluation is documented yet. Synthetic calibration data are used for pipeline/scenario development only and cannot establish actual teacher or provider experience.

### 5. Who is involved, what are their interests and roles, and what power do they hold?

| Actor | Interest / role | Power and limitation |
|---|---|---|
| World Bank, UIS, ITU, OECD and other data publishers | Define, publish, and maintain indicators or assessments | High influence over what is measurable; coverage, timeliness, and definitions constrain analysis |
| Ministries and school authorities | Policy, curricula, procurement, and implementation | High formal authority; classroom feedback may not shape decisions consistently |
| Providers and local EdTech organizations | Develop and deliver products and services | Influence product design and business models; capacity and procurement access vary |
| Teachers and school leaders | Use, adapt, or reject tools in practice | Essential contextual knowledge; often bear implementation costs with limited formal decision power |
| Learners and families | Experience effects on learning, access, safety, and language | Directly affected, but often underrepresented in policy and product decisions |
| Researcher / project developer | Selects data, builds tools, interprets results | Controls framing and interface; must disclose assumptions, limitations, and positionality |

### 6. What participatory methodologies are adopted in design, development, testing, use, and evaluation?

The AoA teacher, provider, and expert instruments provide a possible framework for stakeholder evidence, but the repository does not establish that the current synthetic dataset consists of their responses or that participants co-designed the prototype. Participatory review and user testing are proposed next steps, not completed methods. The classroom audit and open resource directory are designed to invite contextual assessment, but their usability and appropriateness still require feedback from intended users.

## Technology development

### 7. What is the role and position of the technology development team? How do they work with other actors?

The researcher currently combines analyst and developer roles, producing the pipeline, web interface, and decision-support tools. The pipeline uses externally published datasets rather than co-developing with data agencies. Engagement with AoA participants, practitioners, ministries, and providers should be described only where documented; no co-design or field-testing claim is made in this draft.

### 8. What are the main technical constraints?

- Uneven indicator coverage, different reference years, missing data, and publication lags.
- API access/rate limits and the need for local caching and reproducible transformations.
- A static, client-side observatory limits real-time computation and depends on well-documented pre-processed data.
- The GIGA API panel is a placeholder pending access and populated, verified data.
- External dashboard data and field-voice quotations require source, coverage, and rights verification.
- Synthetic data must be visibly distinguished from observed survey data in files, interface labels, and analysis.

### 9. What are the main technological or digital barriers and divides?

The project examines differences in electricity, connectivity, affordability, functional devices, class size, teacher capacity, language/content fit, and data availability. These barriers vary within countries and should not be inferred from national averages alone. Additional methodological divides include the exclusion of some out-of-school learners from school-based assessments and the underrepresentation of locally relevant languages in digital content and AI systems.

## Technology adaptability and replicability

### 10. Should the technology be adaptable to other contexts? How?

Yes, in principle. The indicator pipeline can be configured for new country sets where comparable data exist, while the audit prompts and resource directory can be localized. Transfer requires checking indicator definitions, languages, laws, curricula, infrastructure, and community priorities in each context; changing country codes alone is not sufficient.

### 11. Are scalability, transferability, or replicability expected? How?

The static website and documented data pipeline are technically reusable. Analytical transfer is conditional on data quality and local review. The current prototype has not demonstrated user adoption, scale, or impact, and open licensing must be verified for each dataset, quotation, and resource before broad reuse is claimed.

## Ethics

### 12. What are the main ethical aspects concerning development and use?

Key issues are avoiding deficit framings, making the provenance and uncertainty of evidence visible, preventing synthetic data from being mistaken for testimony, protecting privacy, and avoiding the use of children’s or teachers’ data beyond the stated purpose. Secondary-source quotations require accurate attribution and reuse permission. The researcher’s role in selecting and interpreting Global South evidence should be made explicit. Open publication is conditional on privacy, consent, licensing, and source rights.

### 13. Are there relevant regulatory obligations?

Potential obligations depend on the data subjects, institutions, and jurisdictions involved. Before using primary responses, the project should confirm applicable institutional ethics review, informed consent, data minimization, access, retention, anonymization, and cross-border transfer requirements. If children are directly involved, additional safeguarding and consent requirements apply. The present draft does not claim that a particular national privacy law applies to all project data. The UniTO Final Project Guidelines require disclosure of generative-AI use and recommend an annex of relevant exchanges.

---

## Final Project Guidelines cross-check

| Guideline expectation | Current response / remaining action |
|---|---|
| Connect the project to the Master and social good | Uses an ICT4D equity lens and UNESCO Six Pillars; articulate social-good contribution without claiming unmeasured impact |
| Connect the project to internship learning | The AoA/EdTech landscape work is relevant context; document the specific research connection and confirm permission to use any internship-derived material |
| Integrate theoretical and practical components | Conceptual analysis plus pipeline and observatory prototype are documented |
| Submit a tangible practical product and include its URL | Prototype exists in the repository; confirm public URL and deployment before submission |
| Prepare a five-minute presentation | A concise idea-check deck is being prepared; use the final defense guidelines for the final presentation |
| Avoid a descriptive internship report | Focus on the research question, method, evidence, prototype, and critical reflection |
| Use third-person language and gender-neutral wording | Applied in the concept and these answers |
| Avoid unsupported claims; cite sources in the requested author/title/year/publisher format | Data dictionary and references are available, but full bibliographic/source verification remains necessary; distinguish estimates, synthetic data, and observed data |
| Disclose generative-AI use | Update the disclosure to include drafting/editing assistance and retain the relevant interaction annex |

*Source: “Final Project Guidelines (Full Master Model), A.Y. 2025–2026.” These answers respond to all 13 questions in Analytical Framework 2; they are not a substitute for the final submission template.*
