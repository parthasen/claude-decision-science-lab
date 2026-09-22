# Which assistant for which job — Claude vs ChatGPT vs Gemini

Model lineups and features change quickly. Treat this as a decision guide based on typical strengths, and re-test on your own data before committing. Verify current plans and data terms on each vendor's site.

## Quick pick
| If the job is… | First choice | Why |
|---|---|---|
| Multi-step work on files in a folder (profile → clean → model → report), reproducible code | **Claude (Claude Code)** | Works directly on local files, runs scripts, keeps skills and approval gates |
| Long documents: contracts, supplier terms, policy PDFs, many reports at once | **Claude** or **Gemini** | Large context windows; check limits for your plan |
| Careful writing, analysis narratives, code review, following long instructions | **Claude** | Strong instruction-following and drafting |
| Ad-hoc chart/table from an uploaded CSV in a chat, quick what-ifs | **ChatGPT** | Built-in data-analysis sandbox and chart output in the chat |
| Work inside Google Workspace (Sheets, Docs, Gmail, Drive) or BigQuery | **Gemini** | Native integration with Google products |
| Multimodal: shelf photos, store video, receipts, product images | **Gemini** or **ChatGPT**; **Claude** for images and PDFs | Test on your own images; accuracy varies |
| Custom shareable mini-assistants for staff (no code) | **ChatGPT (GPTs)**, **Gemini (Gems)**, **Claude (Projects/Skills)** | Each has a reusable-assistant feature |
| Embedding AI in your own app or pipeline | Any via API — choose on cost, latency, data-residency and accuracy in a bake-off | |

## How to decide (10-minute bake-off)
1. Take 3 real tasks: one analysis, one document task, one customer-facing text.
2. Run the same RCTFC prompt on each candidate with the same non-sensitive data.
3. Score 1–5 on accuracy (verify numbers), completeness, format compliance, and time to usable output.
4. Add cost per task and data-handling terms. Choose per task; using two tools is normal.

## Criteria checklist
- **Data privacy**: training on your data? retention? regional hosting? enterprise controls?
- **Integration**: does it connect to your POS export, warehouse, Drive/SharePoint?
- **Reproducibility**: can it leave you code and files, not just answers?
- **Governance**: audit log, SSO, role-based access.
- **Cost**: seat price vs API usage; heavy reasoning and long context cost more.

## This project's recommendation
Use **Claude Code with the DSLC skills** for the analysis pipeline (local files, notebooks, approval gates, reports). Use **ChatGPT** or **Gemini** alongside for quick chat-side exploration or Google Workspace tasks if your team already has them. Decide by bake-off, not brand.
