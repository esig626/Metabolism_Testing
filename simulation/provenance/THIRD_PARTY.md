# Third-party and source-material record

The Metabolism_Testing repository and fluxemu-prototype did not expose a
top-level license at the audited commits. That unresolved licensing question
applies to the copied FluxEMU source and must be resolved before treating this
snapshot as generally redistributable.

## mfapy

mfapy is external and is not copied here. The dependency and official Example
0-derived fixture trace to https://github.com/fumiomatsuda/mfapy commit
a10433af16682386548b360297e2476152d46ede. Its LICENSE blob
87a23a77740d74fa709ad29c8ccb173d71610d00 contains the following notice:

MIT License

Copyright (c) 2018 Fumio Matsuda

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## COBRApy

COBRApy 0.31.1 is an external runtime dependency, not vendored content. The
source snapshot inspected during development carried LICENSE blob
99cec1bcf54cca8f851f76600e02b1ec92ae689d. Consumers must obtain COBRApy and
its license from its official distribution.

## Models, publication transcriptions, and generated fixtures

- The toy model is source-project test material adapted from mfapy Example 0.
- The Antoniewicz TCA model and small numerical tables were transcribed from
  the named publication. The local PDF was unverified, is not included, and
  the transcription and reuse rights remain to be independently checked.
- The R1 CSV/JSON files are generated, noise-free simulation evidence. Their
  own manifests trace the generating source state and upstream example-map
  labels; they are not raw biological measurements.
- The topology fixtures are synthetic generated diagnostics.

No full vendor tree, external PDF, or bulk generated result tree is included.
