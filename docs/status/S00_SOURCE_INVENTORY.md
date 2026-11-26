# ETEMAD S00 — source receipt and integrity inventory

Receipt status: **10/10 architecture documents received in conversation; 0/10 originals imported into the GitHub repository**. Never treat uploaded-chat files as tracked repository files.

Documents were opened locally using python-docx and checked for ZIP/OOXML corruption on 2026-11-22. All ten opened successfully. Hashes below are SHA-256 of **exact uploaded DOCX bytes**, not of extracted text.

| Document | SHA-256 prefix (16 hex chars) |
|---|---|
| 00_MASTER_ETEMAD_ARCHITECTURE.docx | 117e7c0210ebea28 |
| B01_FOUNDATION_TECHNICAL_SPEC.docx | 2d96c2ef58716ffd |
| B02_DOMESTIC_INGEST_TECHNICAL_SPEC.docx | 1cc2577245ece3de |
| B03_FOREIGN_INGEST_TECHNICAL_SPEC.docx | 8076c289f0bf8365 |
| B04_PREPROCESSING_TECHNICAL_SPEC.docx | bc845c34c4461f6d |
| B05_CONTENT_TECHNICAL_SPEC.docx | a27c9f359e4092b0 |
| B06_INTELLIGENCE_TECHNICAL_SPEC.docx | fd55474bb695d825 |
| B07_STUDIO_TECHNICAL_SPEC.docx | 16e9f0ee87cdafcd |
| B08_PUBLISHING_TECHNICAL_SPEC.docx | 8f54dcd5f74a9375 |
| B09_INTERFACE_TECHNICAL_SPEC.docx | 76a7c82165730db6 |

**Integrity note:** Only one local B02 file copy is currently available; the earlier upload cannot be separately compared byte-for-byte. Do not claim duplicate equality.

## Source decisions observed
- Master spec 1.1 identifies Python/FastAPI, PostgreSQL, Redis, React/TypeScript and a replaceable model gateway, three separated environments and nine delivery packages.
- B01 owns P01, P02, P03, P26, P28 and P29. Other package documents enumerate B02–B09 ownership. No package implementation has been verified.
- Master and B09 documents use Mantine, whereas the newer Cursor v2 guide states shadcn/ui + Tailwind v4. Record as an ADR, not a hidden rewrite.
- The original JSON Schemas, task matrix, prompts, attachment lists, and extracted Markdown source files are still missing from the GitHub repository. S00 contract checks are therefore blocked.

## Next required operation
Import the **exact ten original files**, ideally from a fully versioned original package, under `source/specs/original/`; generate separately reviewed text/Markdown mirrors under `source/specs/` without modifying originals. Verify the full SHA-256 values of GitHub files after import. Then import the original contracts and manifests. Do not merge an incomplete bootstrap as a finished S00 gate.
