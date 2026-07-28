# Public release process

Status: **Active — required for every public tag or exported release**

The clean public mirror already exists. This process governs later public tags,
archives and mirrors. It does not declare any other private repository
authoritative and it must not be read as evidence of technical or flight
readiness.

## Why

The sanitized branch removes risky files from the current tree, but Git history
can still contain removed files, old binaries, reference PDFs, model artifacts,
local metadata or other material that should not be public. A deletion commit is
not enough for publication.

## Required release path

1. Identify an exact reviewed commit in the public technical repository.
2. Confirm repository authority using `REPOSITORY_GOVERNANCE.md`.
3. Run the release checks below on that exact commit.
4. Generate a manifest containing commit, tool versions, artifact digests,
   licenses and known open technical claims.
5. Require named human sign-off for publication, provenance, legal/IP and
   technical-claims review.
6. Tag or export only the reviewed commit; never import private history.
7. Publish the manifest with the release.

Do not use GitHub fork/import features for the public release, because those can
carry private repository history.

## Export rule

When importing material from a non-public workspace, use an approved tree export
or `git archive` from an exact commit. Never fork, mirror or import private
history. Validate the resulting public tree independently.

## Release checks

Run these checks in the clean mirror before publication:

```powershell
git ls-files -ci --exclude-standard
git ls-files | rg -i '\.(pdf|docx|xlsx|zip|fzz|3mf|safetensors|pt|pth|ckpt|onnx|bin|gguf|ggml|tflite|h5|keras|dll|so|dylib|exe|pdb|nupkg|7z|rar)$'
rg -n -i --hidden --glob '!/.git/**' --glob '!PUBLIC_RELEASE_PROCESS.md' --glob '!PUBLICATION_AUDIT.md' '((api[_-]?key|client[_-]?secret|password|private[_-]?key)\s*[:=]\s*\S+|BEGIN [A-Z ]*PRIVATE KEY)'
rg -n -i --hidden --glob '!/.git/**' --glob '!PUBLIC_RELEASE_PROCESS.md' --glob '!PUBLICATION_AUDIT.md' '(C:\\Users|/home/|/Users/|aurorarig|@auroraits|@gmail|@hotmail)'
dotnet build '05_Software/GroundTelemetryDashboard/GroundTelemetryDashboard.sln'
```

Expected result:

- The binary-extension and sensitive-string scans return no unexpected matches.
- The dashboard build succeeds.

## Publication blockers

Do not publish if any of these are true:

- the public mirror contains private history;
- model weights, generated checkpoints or tokenizer dumps are present;
- third-party PDFs, Office files, backup archives or generated binaries are present;
- the AI model role split has not been documented;
- commercial-use and contribution terms have not been reviewed;
- patent/trademark filing decisions are still pending for material that will be
  disclosed.
- any model, dataset, adapter, generated result or design artifact lacks the
  provenance fields required by `ARTIFACT_PROVENANCE.md`;
- the release text promotes an open requirement, analysis or bench result to
  "validated", "confirmed", "flight-ready" or equivalent;
- the release manifest or required human sign-offs are absent.
