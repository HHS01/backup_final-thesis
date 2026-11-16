# Kobo Pipeline Change Log

This log records local Kobo-pipeline changes for review and rollback. Changes are
uncommitted and have not been pushed.

## 2026-11-13 — Phase 1: fail-closed ingestion and privacy boundary

### Pre-change audit

- The repository is public and GitHub Pages is built at
  `https://hhs01.github.io/backup_final-thesis/`.
- The local Git refs contain three tracked Kobo JSON cache files (50 records
  each); all record IDs in the inspected historical version use the mock
  `sub_t_`, `sub_p_`, and `sub_e_` prefixes.
- The tracked calibrated workbook in local history has 600 teacher, 120 provider,
  and 80 expert rows. Its schema has identifier-like columns and is documented
  elsewhere in the project as synthetic/calibrated.
- No real Kobo submissions were identified in those inspected files. This is
  not proof that no copies exist outside the inspected Git refs or in other
  locations.
- GitHub lists the weekly workflow as active, but the run list was empty.

### Files changed

- `.github/workflows/weekly_kobo_fetch.yml`
  - Reduced the workflow token to `contents: read`.
  - Read `KOBO_SERVER` from the repository Actions variable and require all four
    asset UID secrets.
  - Fetches and processes only under `RUNNER_TEMP`; removed repository-wide
    staging, bot commits, pushes, and the unconnected triangulation step.
  - Does not upload artifacts or publish dashboard data in this phase.
- `scripts/fetch_kobo_submissions.py`
  - Requires live credentials and all four asset UIDs; API/configuration errors
    stop the fetch instead of falling back to a cache or generated sample.
  - Fetches all pages for teacher, provider, expert, and follow-up instruments;
    writes only after all four fetches succeed.
  - Requires live output outside the repository. Explicit `--demo` (also
    accepted as the legacy `--offline` alias) writes marked synthetic records
    to `data/demo/kobo`, never to `data/raw/kobo`.
- `.gitignore`
  - Ignores untracked raw Kobo exports and the live intermediate workbook.
  - Existing tracked mock files remain tracked but are no longer read as live
    fallback data.
- `tests/test_fetch_kobo_submissions.py`
  - Adds offline tests for pagination, cross-host pagination rejection,
    required configuration, all-four instrument handling, repository output
    protection, and explicit synthetic marking.
- `KOBO_PIPELINE_CHANGELOG.md`
  - Records this work and its known limitations.

### Known follow-up work

- The Excel bridge still analyzes only teacher, provider, and expert sheets;
  follow-up responses are fetched but not analyzed.
- The calibrated processor still has schema mismatches, including the missing
  `AI_Confidence` field seen when processing the current mock cache. The
  scheduled job therefore remains a non-publishing preflight until the
  normalizer and analysis pipeline are repaired.
- Raw data stays temporary, but this phase does not yet implement approved
  de-identification, analysis aggregates, real-data dashboard loading, explicit
  Demo visualization, insufficient-data UI states, or a reviewed publish gate.
- The existing tracked mock caches and calibrated workbook were not deleted or
  rewritten; review their history separately before any cleanup or history
  rewrite.

### Validation

- `python3 -m unittest discover -s tests -v`: 6 tests passed.
- `python3 -m py_compile scripts/fetch_kobo_submissions.py tests/test_fetch_kobo_submissions.py`:
  passed.
- GitHub Actions workflow YAML parse: passed.
- `git diff --check`: passed.

### Rollback boundary

All Kobo-specific edits are limited to the four files listed above plus this
log. The added test and log can be removed; the workflow, ignore rules, and
fetcher changes can be reverted independently. Do not roll back the pre-existing
dashboard edits in `index.html` or `js/admin1_explorer.js` as part of this task.

## 2026-11-13 — Local credential handling and Phase 2 preparation

- Changed the local `.env` file permissions from `0644` to `0600`; its values
  were not displayed, copied, or added to Git.
- Queried Kobo asset metadata only to confirm form schemas and field counts.
  No respondent submissions were fetched.
- Confirmed the selected analysis fields and response codes against the local
  XLSForms. The follow-up instrument contains contact details and will be
  excluded from public aggregates.
- Added the generated live dashboard aggregate path to `.gitignore`.

## 2026-11-13 — Phase 2: allowlisted analysis and real/Demo dashboard

### Files changed

- `scripts/process_kobo_surveys.py` (new)
  - Reads the four Kobo exports from a temporary input directory and maps
    current XLSForm choice codes for teacher, provider, and expert summaries.
  - Produces only fixed-schema aggregate data; respondent IDs, contact fields,
    organisation/school names, precise location fields, and all free text are
    excluded. Only country-level teacher signals with publishable sample sizes
    are included.
  - Excludes follow-up responses from public output. No AI text analysis or
    third-party text processing is performed.
  - Suppresses a complete distribution when any group has fewer than five
    responses; expert charts publish counts only.
  - Rejects synthetic markers, unmapped form schemas, email/phone strings, and
    identifier-like output fields.
- `tests/test_process_kobo_surveys.py` (new)
  - Covers mapped distributions, multi-select responses, country suppression,
    small-group suppression, follow-up PII exclusion, synthetic-data rejection,
    schema and choice-code mismatches, empty responses, and the no-response
    quality gate.
- `.github/workflows/weekly_kobo_fetch.yml`
  - Fetches all four instruments every Monday and on manual dispatch. Raw
    submissions remain under `RUNNER_TEMP`; only the sanitized aggregate is
    uploaded as a short-lived artifact.
  - Adds a quality-gate failure for empty/insufficient overall samples and
    publishes only the exact aggregate file after explicit manual approval
    (`workflow_dispatch` input `publish=true`) or, for scheduled runs only,
    opt-in Actions variable `SURVEY_PUBLISH_ENABLED=true`. A manual preflight
    with `publish=false` never publishes, even when scheduled publishing is on.
  - Limits write permission to the separate publishing job and pins action
    releases to immutable commit SHAs.
- `index.html`
  - Defaults to loading `data/processed/survey_dashboard_live.json`; missing,
    malformed, empty, and insufficient data receive explicit status messages.
  - Adds an opt-in Demo preview that uses only the existing synthetic baseline.
    Real and Demo data are never combined. Survey country signals in the matrix
    and digest heatmap now use the selected mode rather than silently falling
    back to synthetic signals.
  - Removes the policymaker-facing manual CSV/JSON/Google Sheets ingestion UI
    and replaces unsupported/unsourced survey claims with measured or
    unavailable states. Provider personal-data spending is not inferred from
    connectivity responses.
- `.gitignore`
  - Keeps locally generated live aggregate JSON out of accidental commits.
- `KOBO_PIPELINE_CHANGELOG.md`
  - Records this phase and its rollback boundary.

### Validation and limitations

- Kobo fetcher and processor unit tests pass; the real submission API was not
  called. Tests use synthetic fixtures in temporary directories only.
- Python compilation, inline JavaScript syntax, workflow YAML, and
  `git diff --check` are validated locally.
- No local live aggregate is present, so the dashboard correctly shows the
  unavailable-data state until an approved workflow run publishes one.
- GitHub Actions secrets/variable have not been configured or changed remotely.
  The local workflow edits have not been committed or pushed. The current Pages
  source is branch-based; its response to a workflow-token push has not been
  tested, so the first approved publish must verify that the Pages deployment
  updates as expected.
- Sharp-drop thresholds are not configured; no arbitrary percentage cutoff was
  introduced. Per-form counts are logged with small samples suppressed, and
  empty/overall-insufficient runs fail the quality gate.
- Free text is deliberately excluded, not cleaned or thematically coded. Any
  future qualitative coding or quotation requires a separate consent, review,
  and privacy decision.

### Unresolved items / handoff for the next agent

These items were not completed in this session and should not be treated as
verified:

- **GitHub Actions configuration:** repository secrets for the Kobo token and
  four asset UIDs, plus the `KOBO_SERVER` variable, were not configured or
  verified. `SURVEY_PUBLISH_ENABLED` remains unset/unverified. Local `.env`
  values were not copied or exposed.
- **Live end-to-end run:** no respondent submissions were fetched. The
  fetch-to-dashboard flow was tested with fixtures, not against live responses.
  Run it only after confirming the approved credentials and publication scope.
- **Sharp-drop detection:** no previous-run comparison or sharp-drop threshold
  is implemented. The overall empty/insufficient-data gate works; choose and
  document a per-form threshold and how legitimate zero counts/withdrawals
  should be handled before adding this check.
- **Independent first-publish approval:** manual dispatch requires
  `publish=true`, but no protected GitHub Environment/reviewer approval was
  configured. Decide whether the explicit operator input is sufficient or add
  a separate approval gate before the first live publish.
- **Pages deployment:** the workflow's push to `main` and its effect on the
  branch-based Pages deployment were not tested. Verify with a controlled,
  approved publish before relying on the public dashboard update.
- **Qualitative analysis:** free text and follow-up data remain excluded.
  Establish ethics/consent, human review, and quote-consent rules before adding
  any text coding, quotes, or linkage.

### Rollback boundary

The Phase 2 Kobo changes are limited to `.github/workflows/weekly_kobo_fetch.yml`,
`.gitignore`, `index.html` survey-related markup/scripts, the new
`scripts/process_kobo_surveys.py`, its new test, and this log. `.env` remains
ignored and has mode `0600`. The pre-existing dashboard changes in
`js/admin1_explorer.js` and unrelated parts of `index.html` are not part of this
rollback boundary. No changes were committed or pushed.
