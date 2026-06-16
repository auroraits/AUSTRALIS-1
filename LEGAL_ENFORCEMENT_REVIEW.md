# Legal enforcement review

Status: working legal-risk memo for counsel review. This is not legal advice and
does not replace review by a qualified lawyer in the relevant jurisdictions.

## Goal

Allow public learning, personal experimentation, education and non-commercial
open collaboration, while preserving the ability to stop or license commercial
exploitation of AUSTRALIS-1 / DIY-Nanosat.

## Recommended posture

Use a source-available, non-commercial publication model with dual commercial
licensing:

- public non-commercial license for inspection, education, personal experiments
  and non-commercial collaboration;
- separate written commercial license for paid products, paid services,
  manufacturing, launch-provider deliverables, contract R&D, sublicensing, resale
  or commercial model/dataset usage;
- no public grant of trademarks, endorsement rights, flight-ready implementation
  rights, manufacturing rights or patent rights beyond the minimum rights in the
  selected public license;
- clean public mirror only, so the public record starts from an intentional
  release boundary.

The current interim scheme is:

- software/scripts/firmware: PolyForm Noncommercial 1.0.0;
- docs/designs/datasets/CAD/PCB material: CC BY-NC-SA 4.0;
- marks, project identity, commercial use and patentable inventions: reserved.

For stronger enforcement, ask counsel whether to replace the split scheme with a
single custom "AUSTRALIS Noncommercial Research License" that covers software,
hardware design files, documentation, datasets, model adapters and mission
architecture under one set of definitions.

## License options reviewed

### PolyForm Noncommercial 1.0.0

Good fit for project-authored software because it is a standardized
source-available non-commercial software license. It grants use for
non-commercial purposes and personal research/experimentation, includes notice
requirements, no-other-rights language, patent-defense language and a violation
cure/termination structure.

Risk: it is software-focused. It is not a complete substitute for patent,
trademark, hardware-manufacturing or contributor-IP strategy.

Reference: https://polyformproject.org/licenses/noncommercial/1.0.0

### CC BY-NC-SA 4.0

Good fit for documents, diagrams, educational material and datasets where a
standard non-commercial sharing license is desirable. Creative Commons states
that commercial permissions can be offered separately from a NonCommercial public
license.

Risks:

- CC licenses are copyright licenses, not patent or trademark grants.
- NonCommercial interpretation can be fact-specific.
- CC is not recommended as the main license for software.
- Functional hardware ideas, discoveries, methods and inventions may need patent
  strategy before public disclosure.

References:

- https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.en
- https://creativecommons.org/faq/

### Business Source License 1.1

Useful reference model for source-available commercial control. It allows
non-production use and requires a commercial license for non-compliant use, but
it also requires an eventual open-source change license. That time-based
conversion does not match the current goal unless the project explicitly wants a
future open-source conversion.

Reference: https://mariadb.com/bsl11/

### Functional Source License 1.1

Useful for software businesses that want broad use while blocking competing
commercial offerings, with automatic conversion to MIT or Apache after two
years. It is not ideal for AUSTRALIS if the intent is to require permission for
all commercial exploitation indefinitely.

Reference: https://fsl.software/

## Enforcement gaps to close before publication

1. Copyright protects code, text, diagrams, datasets and original expressive
   files; it does not protect bare ideas, facts, discoveries or functional
   concepts.
2. Hardware built from independently implemented functional ideas may not be
   stopped by copyright alone unless protected design files, firmware, text,
   datasets or other copyrightable material were copied.
3. Patentable inventions may lose protection if publicly disclosed before filing
   or before counsel confirms the filing strategy.
4. Trademarks and mission identity require separate registration/use strategy.
5. External contributions can create ownership ambiguity unless contributions
   are governed by a CLA, DCO or explicit inbound license.
6. AI datasets, adapters and benchmark outputs need clear provenance and
   commercial-use restrictions if they are intended to be monetizable assets.

## Required controls

- Publish from a clean mirror, not private history.
- Add a contribution policy before accepting external pull requests.
- Require contributors to certify original work and grant the project owner the
  right to use, sublicense and commercially license contributions.
- Keep the AUSTRALIS name, logos, mission identity and confusingly similar marks
  outside the public license grant.
- Keep model weights, private checkpoints and unpublished datasets out of Git.
- Add commercial-contact instructions to README and repository description.
- Preserve third-party notices and avoid vendoring third-party PDFs, CAD,
  datasheets, papers, model artifacts or generated binaries.
- Decide patent/trademark filings before public mirror release.

## Commercial license checklist

A separate commercial agreement should cover:

- licensed materials and version/commit scope;
- permitted commercial field and excluded fields;
- manufacturing and flight/launch permissions;
- warranty disclaimer and mission-risk allocation;
- support, updates and security obligations;
- attribution and branding rules;
- sublicensing and affiliate use;
- confidentiality for non-public material;
- patent license scope or explicit no-patent grant;
- fee structure, audit rights, termination and cure;
- governing law, venue and dispute process.

## Practical conclusion

For the next release gate, keep the current standardized public terms as an
interim publication layer, but treat them as incomplete for high-value commercial
enforcement. Before flipping any public mirror to public visibility, legal
counsel should decide whether to:

1. keep the current PolyForm NC + CC BY-NC-SA split with stronger notices and a
   separate commercial license template; or
2. replace it with a custom AUSTRALIS non-commercial research license drafted for
   software, hardware design files, datasets, AI assets and mission architecture.
