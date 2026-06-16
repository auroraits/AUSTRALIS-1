# Publication audit

Audit date: 2026-06-15

Scope: `auroraits/DIY-Nanosat`, branch `audit/publication-readiness`.

## Executive result

The current working tree can be cleaned for publication, but the existing private
repository history should not be made public directly. Several files that are not
public-release material existed in the current tree or in history:

- third-party PDFs, datasheets, brochures, academic papers and an auto-generated
  video transcript;
- Office documents with author/company metadata;
- generated .NET `bin/` and `obj/` outputs and native runtime binaries;
- KiCad backup ZIPs and generated archives;
- vendored IBM Granite model weights/tokenizer files;
- local editor/agent configuration;
- a Fritzing BOM export containing a local absolute path;
- an older shopping/prototype PDF and Obsidian workspace files in history.

Decision: publish a clean public mirror/export from the sanitized tree. Do not
rewrite the private canonical repository as the first choice, and do not simply
flip the private repo visibility to public.

## Secrets and personal data

No obvious high-risk credential was found in the current text tree after
excluding generated/model/build artifacts. A history scan excluding AI artifacts,
Office/PDF/binary files and build outputs found no high-risk secret pattern.

Manual findings:

- `docs/6.6CUSTINFO-PV.docx` had third-party metadata and a Boeing email in
  document properties.
- `06_Costs/BOREALIS1_cost_projection_2026-03-18.xlsx` had personal author
  metadata.
- `03_Power/EPS_PCB/EPS_Bench1S/Satellite_EPS_1_bom.html` contained a local
  absolute workstation path.
- `docs/Elevator Pitch.txt` contained personal/business biography and domains.

These were removed from the public tree.

## IP and redistribution risks

Removed or excluded from the public tree:

- vendor/reference PDFs and DOCX files under `99_References/` and `docs/`;
- Fritzing `.fzz` files with embedded third-party parts/attribution;
- generated transcript from DownSub;
- IBM Granite model weights/tokenizer artifacts;
- generated build outputs and native binaries;
- ZIP backups and generated archives;
- CAD artifact with unverified origin metadata.

Kept:

- authored Markdown architecture, mission, requirements, risks and ADRs;
- source code and scripts;
- KiCad source files that appear project-authored;
- structured BOM/cost Markdown/CSV with ROM/TBD values;
- AI dataset and benchmark files generated for the project.

## License recommendation

The stated goal is not compatible with an OSI-approved open-source license,
because commercial-use restrictions are not open source under the Open Source
Definition.

Recommended public scheme:

- code/software/firmware/scripts: PolyForm Noncommercial License 1.0.0;
- documentation/designs/datasets/CAD/PCB files: CC BY-NC-SA 4.0;
- project name, marks and mission identity: all rights reserved;
- commercial use: separate written license.

This is a source-available, non-commercial publication model, not OSI open
source. It matches the goal of allowing personal, educational and non-commercial
open collaboration while requiring permission for commercial use.

Why not CERN-OHL as the main hardware license: CERN-OHL v2 is a strong option
for true open hardware, but its variants are designed for freedom to use, study,
modify, share, distribute and make hardware. That does not match the explicit
goal of requiring permission for commercial use.

References:

- https://opensource.org/osd
- https://polyformproject.org/licenses/noncommercial/1.0.0
- https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en
- https://opensource.org/license/cern-ohl-p-2-0

## Publication decision

Use the process in `PUBLIC_RELEASE_PROCESS.md`. The public repository must start
from a fresh single-root commit produced from the reviewed sanitized tree.

## AI model role decision

The AI payload model roles are now split explicitly:

- Granite 350M: flight candidate / compact development line, not flight-ready;
- Granite 3.1 2B: bench and ground experimentation model, not primary flight
  candidate under the current power and thermal budget.

See `08_Decisions/ADR-20260615-ai-model-roles-granite350m-flight-candidate-2b-experimentation.md`
and `05_Software/AI PAYLOAD/MODEL_ASSETS.md`.

## Legal enforcement decision

The current license stack remains an interim standardized publication layer:

- software/scripts/firmware: PolyForm Noncommercial 1.0.0;
- docs/designs/datasets/CAD/PCB material: CC BY-NC-SA 4.0;
- marks, commercial use, manufacturing rights, flight-ready implementations and
  patentable inventions: reserved.

For stronger commercial enforcement, counsel should review whether to replace
the split scheme with a custom AUSTRALIS non-commercial research license before
the public mirror is made public. See `LEGAL_ENFORCEMENT_REVIEW.md`.

## Remaining blockers before public release

1. Create a clean public mirror/export. A deletion commit is not enough because
   history still contains removed material.
2. Execute the release checks in `PUBLIC_RELEASE_PROCESS.md` against the clean
   mirror, not only against this private branch.
3. Confirm ownership/origin of any CAD or PCB artifacts before reintroducing
   them publicly.
4. Have legal counsel review the license strategy, patent strategy, trademark
   protection and commercial license template.
5. Decide whether any patent/trademark filing must happen before disclosure.
6. Add automated secret scanning to CI before publication.

## Validation commands used

Representative checks:

```powershell
git ls-files
git ls-files -ci --exclude-standard
git log --all --name-only --pretty=format:
rg -n -i --hidden --glob '!/.git/**' '(api[_-]?key|secret|password|private[_-]?key|client[_-]?secret|BEGIN .* PRIVATE KEY)'
```

Additional manual checks were run against Office metadata, PDF metadata strings,
local absolute paths, emails/phones, heavy files and generated artifacts.
