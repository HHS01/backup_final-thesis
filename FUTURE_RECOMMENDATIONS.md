# Future recommendations: verified status and next actions

This list was checked against the current repository on 2026-11-13. It replaces earlier assumptions and estimates that were not supported by code or test evidence. Synthetic school data in `TEMP/giga_synthetic/` is for interface and pipeline testing only.

## Survey ingestion

| Item | Current evidence | Recommendation |
|---|---|---|
| Upload file validation | `index.html` treats every non-`.json` file as CSV and does not check MIME type. | **Do next:** accept only `.csv` and `.json`; reject other file types before reading. |
| CSV schema and parsing | The browser parser guesses columns from header substrings, splits rows on commas, and can report success when no recognized teacher fields were found. It does not report missing columns. | **Do next:** validate the headers/stream type, handle quoted CSV correctly, report missing fields, and distinguish “parsed” from “metrics updated.” |
| Empty uploads | The browser parser throws when the CSV has fewer than two non-empty lines; its upload handler displays the error. | No separate empty-file mechanism is needed; make the message actionable while improving parser validation. |
| Sample template and loading feedback | No downloadable CSV template or progress indicator was found. The status box does show “Parsing …”. | **Useful:** provide a template. A spinner is optional unless large uploads are common. |
| Browser parser tests | The Python Kobo processor has focused tests, including malformed/unmapped schemas and empty instruments. The inline browser parser has no corresponding tests. | **Do next:** extract the parser to a testable module and cover valid, malformed, missing-header, quoted-field, and empty-file cases. |
| Refresh persistence | Live uploads are held in page memory; no `localStorage` persistence was found. | **Do not add by default:** survey uploads may contain sensitive responses. Persistence needs a deliberate data-retention and privacy decision. |

## Ingestion and data handling

| Item | Current evidence | Recommendation |
|---|---|---|
| Kobo pagination | `scripts/fetch_kobo_submissions.py` fetches every page and checks for pagination loops and unexpected hosts. | Pagination is implemented. Exponential backoff and an async client are not justified by current evidence; add bounded retries only if API rate-limit failures occur. |
| Public-data safety | `scripts/process_kobo_surveys.py` excludes follow-up records from its public payload, allowlists aggregate fields, checks for identifier/email/phone-like content, and has tests for PII exclusion. | Keep these safeguards and tests. Do not copy raw submissions into `data/processed/`. |
| Raw response retention | Live Kobo exports require an output path outside the repository. This does not itself establish access controls, retention limits, or encryption. | Document and enforce those operational controls before real PII is collected. Do not introduce a contact database until a concrete follow-up workflow requires one. |
| Public connectivity bundles | `out/dashboard/` already contains country-specific geography, series, and change files. | Country-level lazy loading is already available; no additional JSON chunking work is needed for this dashboard. |
| Scale and incremental processing | The earlier 10–30k-row memory claims and 2GB estimate have no benchmark attached. | Defer Polars/Dask, incremental builds, archiving, and scoring-loop optimization until representative profiling demonstrates a bottleneck. |

## Privacy, testing, and references

- The Kobo processor’s automated PII checks apply to its public aggregate, not to raw exports or browser uploads. Keep raw records outside public output paths and review retention/access separately.
- A CI scan of `data/processed/` could be added if that directory begins receiving user-provided or unreviewed content; current processing already emits a constrained aggregate and tests its public-safety checks.
- No periodic legal-reference verification job or citation-linking requirement is established by the current code. Keep references reviewed as part of thesis updates rather than adding an automated job that cannot verify legal currency.

## Priority

1. Harden the browser upload parser: extension guard, schema/stream validation, quoted CSV support, and honest status messages.
2. Extract and test that parser without persisting user data.
3. Before collecting real responses, document raw-export access, retention, consent, and the separation between follow-up contacts and public aggregates.
4. Revisit scalability only after measuring a representative workload.
