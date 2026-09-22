# Prompt guide for data work (Claude, ChatGPT, Gemini)

The same structure works on all three. Vague prompts cost more than the choice of model.

## The RCTFC frame
| Part | Say | Example |
|---|---|---|
| **R**ole | Who the assistant is | "You are a retail analytics lead for a kids' apparel chain." |
| **C**ontext | Business, data, period, constraints | "POS line items, 4 stores, Apr 2024–Jun 2025. Returns are negative rows." |
| **T**ask | One verb, one outcome | "Forecast weekly units per section for the next 8 weeks." |
| **F**ormat | Shape of the answer | "Table, then 3 bullet risks, then Python code." |
| **C**heck | How it must verify itself | "Compare to a seasonal-naive baseline; list assumptions; say what you could not verify." |

## Templates
**Describe a dataset**
> Here are the column names and 20 sample rows (no personal data). Describe the grain, likely keys, what each column group means, and data-quality risks. Flag anything ambiguous instead of guessing.

**Choose a model**
> Objective: reduce stock-outs in Baby Care. Data: [columns, period, rows]. List 3 modelling approaches, each with target definition, metric, data needed, leakage risks, and a naive baseline. Recommend one and say why.

**Write analysis code**
> Write pandas code that loads `sales.csv`, treats `Return` bills separately, and produces weekly net revenue by DIVISION. Time-ordered split, no random split. Add asserts on row counts. Explain each step in a comment.

**Interpret results**
> Here are the metrics and top features [paste]. Explain to a store manager in 5 sentences. Then list 3 ways this result could be misleading.

**Stress-test**
> Act as a skeptical reviewer. What could make this conclusion wrong? What would you check first?

## Habits that raise quality
1. Give schema and a small sample, not the whole file. Strip names, phone numbers and card data first.
2. Ask for assumptions and unknowns to be listed.
3. Iterate: ask for a plan first, approve, then code.
4. Ask for one change at a time when editing code.
5. Run the code yourself. Treat numbers the model states without running code as unverified.
6. Save prompts that worked as reusable templates or skills.

## Data safety
Do not paste customer identifiers, credentials or unreleased financials into a consumer chat app. Use a business/enterprise plan with data controls, or work locally (Claude Code reads files on your machine and only sends what it is shown).
