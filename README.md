# Person Re-ID Datasets, Methods, Evidence, and Protocols

Public companion and reproducibility repository for the protocol-oriented critical review of person re-identification (ReID):

> Person Re-Identification Datasets and Protocols: From Fixed-Source to Unified Multi-Source Retrieval

This repository maintains the structured research materials behind the review's Dataset–Protocol–Evidence framework. It is the public home for the machine-readable registries, evidence records, protocol descriptions, and audit materials cited by the manuscript and its supplementary appendices.

## Repository Contents

- `tables/`: machine-readable versions of Appendices A-E.
- `evidence/source-manifest.csv`: Appendix C evidence sources, official or archived URLs, source versions, and checking dates.
- `evidence/citation-audit-summary.csv`: summary of the submission citation audit.
- `evidence/main-references.csv`: the 88 main references, with stable citation keys and bibliographic titles.
- `evidence/supplementary-references.csv`: the five supplementary-only sources, labelled S1-S5.
- `evidence/citation-map.csv`: stable-key mapping from the original 118-reference manuscript to the current references; omitted entries are explicitly marked.
- `evidence/submission-snapshot.json`: version metadata, exported row counts, and SHA-256 checksums.
- `supplementary/appendix.pdf`: standalone Supplementary Material corresponding to the manuscript snapshot.

## Appendix Map

- **Appendix A**: structured dataset master table.
- **Appendix B**: method-evidence registry.
- **Appendix C**: availability, license, ethics, anonymization, usage restrictions, maintenance, and source traceability.
- **Appendix D**: twelve published MP-ReID query-to-gallery directions; no original experimental results are distributed here.
- **Appendix E**: structured Query-Gallery protocol registry.
- **Appendix F**: task difficulties and methodological responses (Table F1 in the PDF).
- **Appendix G**: detailed future evaluation settings (Table G1 in the PDF).

## Scope and Restrictions

This repository contains metadata, evidence links, protocol descriptions, and derived tables only. It does not redistribute dataset images, videos, raw surveillance footage, personally identifiable information, or files that require a release agreement. Source-specific terms and redistribution restrictions remain controlling.

The label "Not explicitly reported in the listed evidence sources (checked YYYY-MM-DD)" means that no clear statement was located in the listed sources as of the checking date; it does not establish that the underlying practice or restriction does not exist.

## Manuscript Snapshot

The version corresponding to the current 88-reference manuscript is archived as [Release `v1.2.1-paper-submission`](https://github.com/Trans1010/person-reid-datasets-methods-protocols/releases/tag/v1.2.1-paper-submission). The `main` branch may receive later verification updates; those updates do not change the evidence snapshot associated with that release.

Registry entries in the manuscript and supplementary material were last verified on 4 September 2026. The primary literature search covered 1 January 2007–4 August 2026, followed by an update search completed on 17 September 2026.

The snapshot uses the current manuscript's 88-reference numbering. Numerical citations [1]-[88] in the CSV registries, source manifest and supplementary PDF correspond to `evidence/main-references.csv`. Citations [S1]-[S5] refer only to the supplementary reference list. The public PDF contains Appendices A-G; the machine-readable tables cover A-E.

The A-E tables and source manifest were regenerated from the current supplementary LaTeX source using stable citation keys, rather than renumbering the old public CSVs by position. The version audit was completed on 8 October 2026; this does not change the historical evidence-checking dates above. `scripts/sync_submission.py` reproduces the export when supplied with the matching manuscript source directory.

Release `v1.1-paper-submission` remains a historical snapshot of the earlier 118-reference version and must not be used to interpret citations in the current manuscript.

Release `v1.2.1-paper-submission` also supersedes the initial v1.2 synchronization snapshot. It fixes CSV line-ending reproducibility so the recorded SHA-256 checksums match the files downloaded from GitHub. CSV exports use LF line endings, enforced by `.gitattributes`.

## Citation

Please cite the associated review manuscript and, when referring to a specific dataset or protocol, cite the original source listed in the relevant table. The repository metadata are described in `CITATION.cff`.

Repository: https://github.com/Trans1010/person-reid-datasets-methods-protocols

Last version and citation audit: 2026-10-08.
