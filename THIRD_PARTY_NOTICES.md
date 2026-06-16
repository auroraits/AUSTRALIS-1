# Third-party notices

This repository intentionally avoids vendoring third-party PDFs, model weights,
generated build outputs and binary reference archives in the public tree.

## AI model ecosystem

- IBM Granite model family: upstream models are published by IBM. Granite 4.0
  documentation and the Hugging Face model card identify Granite 4.0 350M as
  Apache 2.0 licensed. In this repository, the Granite 350M family is treated as
  the compact flight-candidate line, not as a flight-ready model.
  - https://www.ibm.com/granite/docs/models/granite
  - https://huggingface.co/ibm-granite/granite-4.0-350m-base
- IBM Granite 3.1 2B Instruct is an Apache 2.0 upstream model used only for
  bench and ground experimentation in this repository, not as the primary flight
  candidate.
  - https://huggingface.co/ibm-granite/granite-3.1-2b-instruct
- Hugging Face Transformers, PEFT, TRL and Datasets are third-party dependencies
  used by the AI payload scripts. They remain under their upstream licenses.

The public repository does not include IBM model weights or tokenizer artifacts.
Download upstream assets directly from the original source and comply with the
upstream license.

## Ground telemetry dashboard

- `System.IO.Ports` is referenced as a NuGet dependency by the .NET dashboard.
  Generated DLLs and native runtime libraries are not stored in the public tree.
- Browser-side dashboard dependencies are loaded from public CDNs in the current
  prototype (`SignalR`, `Chart.js`, `three.js`). Review their upstream licenses
  before redistributing a packaged offline build.

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
