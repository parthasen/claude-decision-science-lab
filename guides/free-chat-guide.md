# Using this workflow in free Claude.ai chat (no Claude Code)

Everything else in this repo (`dataset-explorer`, `dslc`) is built for **Claude Code** — it needs plugin installation and local file/script access that plain [claude.ai](https://claude.ai) chat doesn't have. If your team only uses free Claude.ai chat, you can still work through the same *thinking*, manually, with copy-paste prompts. It'll be lighter-weight — no saved project folder, no reproducible pipeline, no automatic reports — but the questions and the discipline (stop and check before acting) carry over.

## What's different here

- **No installed skills.** Nothing to set up — just open a chat.
- **You upload the file directly into the conversation** (CSV or Excel), instead of pointing at a folder.
- **Whether Claude can run real calculations on your file** (not just describe it) depends on your Claude.ai plan and what's enabled for your account. If it can, ask it to; if it can't, it will still reason well from a description of your data and numbers you paste in.
- **Nothing is saved automatically.** Download or copy out anything you want to keep — a chat isn't a project folder.
- **One conversation, one dataset.** Start a fresh chat per dataset/question so context doesn't get muddled.

## Before you start

- Export the sheet you actually need as `.csv` or `.xlsx` — don't upload an entire multi-tab workbook if you only need one tab.
- Strip or mask anything genuinely sensitive (customer names, emails, IDs you don't want in a chat log) unless your organization's Claude.ai plan is approved for that kind of data.
- Know roughly what you're trying to decide — even a rough sentence like "should I reorder these products" is enough to start.

## Step-by-step prompts (copy, paste, fill in the blanks)

### 1. Understand the data
> I've attached [filename]. Tell me in plain English: what is each column, what time period does this cover, roughly how many rows, and anything that looks off (missing values, duplicates, weird outliers). Don't build anything yet — just describe what's here.

### 2. Agree on the question
> Given that data, I want to answer: [your business question, e.g. "which products are we likely to run out of in the next two weeks"]. What's the most useful way to frame this as a specific, measurable question? What would count as a good answer?

### 3. Check data quality before trusting it
> Before we go further — is there anything in this data that would make an answer to that question unreliable? Missing history, too few examples, obvious data entry errors?

### 4. Get the insight
> Based on this data, what actually drives [the outcome you care about]? Show me the pattern, and tell me honestly whether it looks like a real signal or could just be noise from a small sample.

### 5. Ask for a recommendation, not just a description
> Given everything above, what would you actually recommend I do? Give me 2–3 options with the tradeoffs, not just one answer.

### 6. Get something you can share
> Write this up as something I could paste into an email to my manager / present in a meeting — a short summary, the key numbers, and the recommendation. Keep it non-technical.

## If you want more than a chat can give you

A single chat won't give you: a reproducible pipeline, a held-out test of a prediction model, a saved model you can reuse, or a multi-person audit trail of decisions. If you find yourself needing that, that's exactly what the full `dataset-explorer`/`dslc` toolkit in this repo is for — it just needs someone with Claude Code (or a paid Claude.ai plan with Projects/custom Skills enabled) to run it. See [`manager-guide.md`](manager-guide.md) for what that looks like.
