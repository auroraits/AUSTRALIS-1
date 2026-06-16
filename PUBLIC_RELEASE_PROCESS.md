# Public release process

Status: required for any public repository publication.

Decision: publish AUSTRALIS-1 / DIY-Nanosat through a clean mirror/export, not by
changing the visibility of the private working repository.

## Why

The sanitized branch removes risky files from the current tree, but Git history
can still contain removed files, old binaries, reference PDFs, model artifacts,
local metadata or other material that should not be public. A deletion commit is
not enough for publication.

## Required release path

1. Merge the publication-readiness cleanup into the private canonical repo.
2. Export only the reviewed tree from the approved commit.
3. Create a new empty repository for the public mirror.
4. Commit the exported tree as the first public commit.
5. Run the release checks below on the public mirror.
6. Keep the public mirror private until a human release review signs off.
7. Change visibility only after legal, IP and technical release gates are closed.

Do not use GitHub fork/import features for the public release, because those can
carry private repository history.

## Suggested export commands

From the private canonical repository after the cleanup commit is approved:

```powershell
$export = "$env:TEMP\DIY-Nanosat-public-export"
Remove-Item -Recurse -Force $export -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $export | Out-Null
git archive --format=tar HEAD | tar -x -C $export
```

Then initialize a fresh repository in `$export` and push that single-root-commit
history to the new public mirror.

## Release checks

Run these checks in the clean mirror before publication:

```powershell
git rev-list --all --count
git ls-files -ci --exclude-standard
git ls-files | rg -i '\.(pdf|docx|xlsx|zip|fzz|3mf|safetensors|dll|so|dylib|exe|pdb|nupkg|7z|rar)$'
rg -n -i --hidden --glob '!/.git/**' --glob '!PUBLIC_RELEASE_PROCESS.md' '(api[_-]?key|secret|password|private[_-]?key|client[_-]?secret|BEGIN .* PRIVATE KEY)'
rg -n -i --hidden --glob '!/.git/**' --glob '!PUBLIC_RELEASE_PROCESS.md' '(C:\\Users|/home/|/Users/|aurorarig|@auroraits|@gmail|@hotmail)'
dotnet build '05_Software/GroundTelemetryDashboard/GroundTelemetryDashboard.sln'
```

Expected result:

- `git rev-list --all --count` returns `1` for the first public mirror commit,
  unless later public-only release commits were intentionally added.
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
