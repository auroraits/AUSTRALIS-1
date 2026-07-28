# Third-party notices

This repository intentionally avoids vendoring third-party PDFs, model weights,
generated build outputs and binary reference archives in the public tree.

## AI model ecosystem

- `gemma4:e2b` is the current evaluation candidate. The mutable tag is not an
  immutable identity and does not prove license, provenance or reproducibility.
  Upstream model identity, digest, runtime build and applicable license must be
  captured before benchmarking or redistribution. No weights are vendored here.
- IBM Granite model families are historical/deferred in the current baseline.
  The prior repository evidence attributed to Granite 350M was executed with
  Granite 3.1 2B and cannot validate Granite 350M.
  - https://www.ibm.com/granite/docs/models/granite
  - https://huggingface.co/ibm-granite/granite-4.0-350m-base
- IBM Granite 3.1 2B Instruct is an Apache 2.0 upstream model used only for
  historical bench and ground experimentation in this repository, not as the
  current flight candidate.
  - https://huggingface.co/ibm-granite/granite-3.1-2b-instruct
- Hugging Face Transformers, PEFT, TRL and Datasets are third-party dependencies
  used by the AI payload scripts. They remain under their upstream licenses.

The public repository does not include IBM model weights or tokenizer artifacts.
Download upstream assets directly from the original source and comply with the
upstream license.

## Ground telemetry dashboard

- `System.IO.Ports` is referenced as a NuGet dependency by the .NET dashboard.
  Generated DLLs and native runtime libraries are not stored in the public tree.
- Browser-side dashboard dependencies must be pinned and packaged with their
  upstream notices for offline/reproducible operation. The release manifest
  records exact versions and digests; an unpinned CDN reference is not accepted
  as verification evidence.

## Hardware and reference designs

- OpenLST is referenced only as an external candidate/reference for UHF TTC
  analysis. No OpenLST source or hardware files are vendored here.
- Fritzing prototype archives were removed from the public tree because they
  embed third-party parts and attribution data. The public source of truth should
  be Markdown, KiCad, and explicitly attributed design assets.
- CubeSat standards, NASA documents, Iridium brochures, academic papers,
  datasheets, vendor PDFs and auto-generated video transcripts are not vendored
  in the public tree. Use citations or links instead of storing copies.

## Removed binary reference material

The audit removed public-tree copies of reference PDFs/DOCX/XLSX/ZIP/model files.
Those files may still exist in the private repository history. Do not make this
private repository public without a clean-history publication step.
