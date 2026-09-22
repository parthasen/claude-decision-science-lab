# Connectors and skills available

Status checked in the Claude Code desktop session on 2026-09-20. Re-check with `mcp__ccd_connectors__session_connectors_status` — availability changes.

## Connectors / MCP servers
| Connector | Use in this skill | Status |
|---|---|---|
| Local files (Read/Bash) | Discover, profile, model | Ready |
| Jupyter MCP (`jupyter`) | Live notebook execution (dslc runtime `jupyter-live`) | Configured; failed to connect this session — start JupyterLab with `scripts/start_jupyter.sh` |
| Google Colab MCP (`colab-mcp`) | Colab runtime for heavy models / GPU | Configured |
| Google Drive | Find user datasets in Drive; store outputs | Available |
| Claude Docs (docs connector) | Publish brief/report as a shared doc | Available |
| Claude in Chrome / built-in browser | Browse Kaggle, data portals, docs | Available |
| Kaggle CLI | Search/download datasets | Installed only if `~/.kaggle/kaggle.json` exists; **no token as of 2026-09-13** |
| Hugging Face datasets | Search/load public datasets | Via `huggingface_hub` or connector if enabled |
| BigQuery public data | Public retail/commerce datasets | Connector needed; estimate query cost first |
| Web search / fetch | Domain research, dataset search | Ready |
| Amplitude, Asana, Atlassian, ClickUp, Figma, Fireflies, Intercom, Linear, Monday, Notion, Pendo, Similarweb, Slack (product-management plugin) | Optional: pull product analytics, publish results, notify | **Need OAuth** — authorise via claude.ai connector settings; unavailable until then |

Suggested extra connectors for retail: a data warehouse (BigQuery/Snowflake), POS/ERP export via Drive or S3, Google Analytics, Shopify/WooCommerce, Slack or Teams for alerts. Use `mcp__mcp-registry__search_mcp_registry` to find them.

## Skills
| Skill | Role |
|---|---|
| `dataset-explorer` (this) | Orchestrates find → brief → search → models → build |
| `dslc` + `dslc-frame/acquire/profile/prepare/stats/model/explain/report` | The 8-stage life cycle used in Step 5 |
| `dataviz` | Chart design for stats and reports |
| `anthropic-skills:xlsx / docx / pptx / pdf` | Export tables, reports, decks |
| `anthropic-skills:docs` | Shared living docs |
| `anthropic-skills:schedule`, `loop` | Recurring refresh of a model or brief |
| `product-management:*` | Specs, metric reviews, stakeholder updates from findings |
| `code-review`, `security-review` | Review the generated pipeline code |
