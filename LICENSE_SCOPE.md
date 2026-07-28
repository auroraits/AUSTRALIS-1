# License scope and file classification

Status: **Interim / legal review open**  
Effective date: 2026-07-27

This file provides deterministic repository-level classification while
per-file SPDX headers and the complete reviewed license bundle remain open
release actions. An explicit file notice or third-party license overrides this
mapping.

| Path or material | Intended identifier | Qualification |
|---|---|---|
| Project-authored source code, scripts and firmware | `PolyForm-Noncommercial-1.0.0` | Interim; exact text must be bundled before tag |
| Project-authored Markdown, CSV, JSON/JSONL datasets, diagrams and requirements | `CC-BY-NC-SA-4.0` | Interim; dataset rights/provenance must also be demonstrated |
| Project-authored CAD and PCB source | `CC-BY-NC-SA-4.0` | Does not grant patent, trademark, flight or manufacturing assurance |
| Generated evidence and binaries | No automatic classification | Requires artifact manifest, source inputs and explicit release decision |
| Third-party material | `NOASSERTION` until recorded | Original terms control; see `THIRD_PARTY_NOTICES.md` |
| Names, marks, logos and mission identity | No public trademark grant | All rights reserved pending counsel review |

## Release requirement

Before a tagged release:

1. confirm the legal rightsholder and chain of title;
2. include exact reviewed license texts in `LICENSES/`;
3. add SPDX identifiers or a complete machine-readable manifest for every
   tracked file;
4. resolve all `NOASSERTION` entries;
5. record the reviewing authority and manifest digest.

This classification is not legal advice and does not itself establish ownership
or a valid grant.
