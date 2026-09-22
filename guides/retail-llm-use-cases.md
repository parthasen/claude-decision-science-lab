# Using ChatGPT, Claude and Gemini in retail

Each use case: what it does, which assistant fits, the data it needs, and the guard-rail. "Fit" is a starting point — see `llm-selection.md`. Numbers must come from your data and code, never from the model's memory.

## Merchandising and planning
| Use case | How | Fit | Guard-rail |
|---|---|---|---|
| Assortment and range review | Summarise sales by section/brand, find tail SKUs, draft range recommendations | Claude Code / ChatGPT | Human merchant signs off |
| Demand forecast and replenishment | LLM writes and explains the forecasting pipeline; a statistical model produces the numbers | Claude Code | Always compare against a naive baseline |
| Markdown and promotion planning | Scenario what-ifs, draft promo calendar, post-promo readout | ChatGPT / Claude | Margin math verified in code |
| Vendor negotiation prep | Summarise contracts, price lists, past performance | Claude / Gemini (long context) | Check clause citations |

## Customer and marketing
| Use case | How | Fit | Guard-rail |
|---|---|---|---|
| Segment naming and campaign copy | Feed RFM cluster profiles (aggregates only) → personas, message variants, subject lines | Any | Brand review; consent and opt-in rules |
| Personalised recommendations text | Model picks products; LLM writes the message | Any via API | No personal data in prompts |
| Review and feedback mining | Cluster themes, sentiment, product issues from reviews and support tickets | Claude / Gemini / ChatGPT | Sample-check labels |
| Conversational shopping assistant | RAG over catalogue and policies | Any via API | Ground answers in catalogue; escalate to human |

## Store operations
| Use case | How | Fit | Guard-rail |
|---|---|---|---|
| Staff Q&A on SOPs, returns, GST rules | Assistant over policy docs | Claude Project / GPT / Gem | Cite source doc; version control |
| Shift and task summaries | Turn POS and footfall into a daily brief | Claude / Gemini | Verify with source numbers |
| Shelf and planogram checks | Photo → compliance notes | Gemini / ChatGPT | Pilot accuracy per store; human audit |
| Loss and fraud triage | Anomaly model flags bills; LLM drafts case notes | Claude Code | Model flags, humans decide |

## Finance, supply chain, back office
| Use case | How | Fit | Guard-rail |
|---|---|---|---|
| Tax/HSN mapping and invoice checks | Validate HSN vs GST rate, flag mismatches | Claude Code | Rules in code, LLM explains exceptions |
| Inventory ageing and waste narrative | Summarise ageing, suggest actions | Any | Needs expiry and stock data |
| Supplier email and PO drafting | Draft, translate, summarise threads | Any; Gemini in Gmail | Human sends |
| Management reporting | Monthly deck / doc from KPIs | Claude (docx/pptx skills) | KPI definitions fixed in code |

## Where an LLM is the wrong tool
Exact arithmetic, forecasting numbers, and pricing decisions belong in code or a statistical model. Use the LLM to write, explain, and review that code.

## Getting started (30 days)
1. Week 1: pick 2 low-risk use cases (review mining, SOP assistant). Set data rules.
2. Week 2: run a bake-off on your own data (`llm-selection.md`).
3. Week 3: build the reusable prompt/skill; add a human review step.
4. Week 4: measure time saved and error rate; decide scale-up.

## Measure
Time per task, error rate after review, adoption, and business KPI (waste %, stock-out %, campaign conversion). Stop use cases that do not move a KPI.
