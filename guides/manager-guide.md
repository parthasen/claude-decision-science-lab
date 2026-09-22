# A manager's guide to this toolkit (no coding needed)

This page is for you if you're not a coder and just want to turn a spreadsheet or data export into an answer — "should we restock this?", "which customers are about to churn?", "what's driving this drop in sales?" — by having a conversation, not writing code.

## What this actually is

Think of it as a analyst who:
- never touches your data without telling you first,
- shows you what it found in plain English before doing anything else,
- always stops and asks you to choose before moving to the next step,
- and at the end, hands you a report, a slide deck, or a spreadsheet — whatever you'd actually use in a meeting.

You talk to it the same way you'd type a message to a colleague. No code, no notebooks, no formulas required from you.

## How to start

1. Open Claude Code and make sure you're pointed at this `LAB` folder.
2. Put your data file (Excel, CSV) somewhere in the folder, or tell it where the file already lives.
3. Type in plain English what you want. That's it. Some examples that work:
   - *"What data do I have in this folder?"*
   - *"Look at sales.xlsx and tell me what's in it."*
   - *"I want to know which products we're likely to run out of next week."*
   - *"Why did revenue drop in March?"*

You don't need to know the "right" words. If your request is vague, it will ask you a clarifying question instead of guessing.

## What happens next (in plain terms)

The work happens in small steps. After every step, it stops, shows you what it found, and gives you a short list of choices — it never barrels ahead on your behalf. Here's the shape of it, translated out of jargon:

| Step | What it's really doing | What you'll be asked |
|---|---|---|
| 1. Look at the data | Opens the file, figures out what each column means, flags anything odd (missing values, duplicates, obvious errors) | "Does this description match what you know about the data? Anything I got wrong?" |
| 2. Agree on the question | Turns your business question into something specific and measurable | "Is this the right target? Is this the right success measure?" |
| 3. Get more context (optional) | Looks for outside data or benchmarks that would help (e.g. public retail datasets, industry averages) | "Want me to pull in any of these?" |
| 4. Check data quality | Looks harder at the data for problems that would quietly ruin the answer | "Fix it this way, or go get better data first?" |
| 5. Clean and prep | Fixes what it can, builds the features needed for analysis, sets aside a fair test set | "Here's how I split things so we're not cheating on the test — OK?" |
| 6. Find the story / test the theory | Runs the actual statistics — what's really moving the number, and is it a real pattern or just noise | "Here's what the data says. Want to go further, or is this enough to act on?" |
| 7. Build a prediction (if needed) | Only if your question needs forecasting/predicting — builds and compares a few models against a "just guess the average" baseline | "This model beats the naive guess by X% — good enough to use?" |
| 8. Explain and stress-test | Explains *why* the model predicts what it predicts, checks it isn't quietly unfair to some group, checks where it tends to be wrong | "Comfortable trusting this, or does something here worry you?" |
| 9. Report | Packages everything into whatever you actually need — a written report, a slide deck, a spreadsheet, a one-page summary | "Which of these do you want, and for who — you, your boss, the team?" |

You can also stop after step 6 if you just wanted an answer, not a predictive model — not every question needs one.

## What you'll get at the end

Depending on what you asked for:
- A **plain-language brief** — what's in the data, in a paragraph, not a table dump.
- A **written report** (HTML, readable in any browser, or a Word doc).
- A **slide deck** — if you need to present this to others.
- A **spreadsheet** — the actual numbers behind the recommendation, so anyone can double-check.
- A **short model summary** ("model card") — if a prediction was involved, this explains in plain terms what it's good at, what it's bad at, and where to be careful trusting it.

Everything gets saved in the `outputs/` folder (or inside a project folder under `projects/`) so you can find it again later without re-running anything.

## Things you might worry about (and don't need to)

- **"What if I say the wrong thing?"** You can't. If your request is unclear, you'll be asked a follow-up question instead of getting a wrong answer.
- **"What if it changes my original file?"** It won't. Your raw data file is never modified or deleted — only copies and derived results are created.
- **"What if I don't understand a term it uses?"** Ask it to explain, right there in the conversation — "what does that mean in plain English?" It'll rephrase without the jargon.
- **"What if the answer seems wrong?"** Say so. Every step is a checkpoint specifically so you can push back, ask for a different approach, or say "that doesn't match what I know about the business" — and it will factor that in rather than ignore it.
- **"Do I need Python or Excel formulas?"** No. Those happen behind the scenes. You only ever see the results and the plain-language explanation.

## A realistic example already done for you

`projects/perishable-demand-forecast/` is a finished, real run of this whole process — a perishable-goods retail dataset, walked from "what is this data" through to a final report and a model that predicts demand so stores can reorder better before stock expires. Open `projects/perishable-demand-forecast/reports/report.html` in a browser to see what a finished output actually looks like before you start your own.

## Don't have Claude Code — only free Claude.ai chat?

This guide assumes Claude Code, where these skills install and run automatically. If your team only has access to free claude.ai chat, see [`free-chat-guide.md`](free-chat-guide.md) — a lighter, manual version of the same thinking using copy-paste prompts and a direct file upload, no installation needed.

## If you get stuck

Just say what's confusing, in your own words — "I don't know what to pick here" or "explain that differently" both work. There's also [`guides/decision-science-workflow.md`](decision-science-workflow.md), a more technical one-page map of the same flow, if you ever want to see the mechanics behind it.
