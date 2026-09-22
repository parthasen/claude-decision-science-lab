"""Build reports/report.html (self-contained) from stage outputs. Run from the project folder."""
import base64, json
from pathlib import Path
import pandas as pd

m = json.loads(Path("models/final_metrics.json").read_text())
means = pd.read_csv("models/article_means.csv")
err = pd.read_csv("reports/tables/07_error_by_article.csv")
cv = pd.read_csv("reports/tables/06_cv_results.csv")
art = means.merge(err[["ARTICLE", "wape", "bias"]], on="ARTICLE")
q = m["ratio_quantiles"]
img = lambda f: "data:image/png;base64," + base64.b64encode(Path(f"figures/{f}.png").read_bytes()).decode()
data = {"rows": art.round(4).to_dict("records"), "q": q, "cv": cv.round(3).to_dict("records")}
b = m["baselines_test_wape"]

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Perishable Demand Forecast</title>
<style>
:root{{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--line:#e1e0d9;--card:#fff;--a:#2a78d6;--o:#eb6834}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151514;--ink:#f1f0ec;--ink2:#b5b3ab;--line:#33322f;--card:#1d1d1b;--a:#6da7ec;--o:#ec835a}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 -apple-system,Helvetica Neue,Arial,sans-serif}}
main{{max-width:880px;margin:0 auto;padding:32px 16px 64px}}h1{{font-size:28px;margin:0 0 4px}}h2{{font-size:20px;margin:40px 0 8px}}
p.sub{{color:var(--ink2);margin:0 0 24px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}}.kpi b{{display:block;font-size:26px}}.kpi span{{color:var(--ink2);font-size:13px}}
img{{width:100%;height:auto;border:1px solid var(--line);border-radius:8px;background:#fcfcfb}}table{{border-collapse:collapse;width:100%;font-size:14px}}
th,td{{padding:6px 8px;border-bottom:1px solid var(--line);text-align:right}}th:first-child,td:first-child{{text-align:left}}th{{cursor:pointer;color:var(--ink2);font-weight:600;user-select:none}}
select,input{{font:inherit;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--ink)}}
.bands{{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}}.bands div{{flex:1;min-width:90px;text-align:center;border:1px solid var(--line);border-radius:8px;padding:8px}}.bands b{{display:block;font-size:22px}}
.note{{border-left:3px solid var(--o);padding:8px 12px;margin:16px 0;background:var(--card)}}ul{{padding-left:20px}}small{{color:var(--ink2)}}
</style></head><body><main>
<h1>Weekly demand forecast: fresh produce and dairy</h1>
<p class="sub">Question: how many units of each article will each store sell next week? Decision: weekly replenishment. Data: perishable_45k.csv, <b>synthetic</b> POS lines, Apr 2024 – Mar 2025, 5 stores × 29 articles.</p>

<div class="card"><b>Answer in one sentence.</b> Each article sells a fairly steady number of units per store per week; a plain per-article average forecasts as well as anything we tried (WAPE {m['test_wape']:.3f}), and no model could do meaningfully better because the remaining variation is random.</div>

<div class="kpis" style="margin-top:16px">
<div class="card kpi"><b>{m['test_wape']:.3f}</b><span>Test WAPE (lower is better). Best baseline {b['baseline: expanding mean']:.3f}</span></div>
<div class="card kpi"><b>{m['test_bias']*100:+.1f}%</b><span>Bias on test (total forecast vs actual)</span></div>
<div class="card kpi"><b>{m['coverage_p10_p90']*100:.0f}%</b><span>of weeks fall inside the P10–P90 band (target 80%)</span></div>
<div class="card kpi"><b>{m['test_mae']:.1f}</b><span>units average miss per store × article per week (mean demand 11.4)</span></div></div>

<h2>Forecast lookup</h2>
<div class="card"><label>Article <select id="art"></select></label>
<div class="bands" id="bands"></div>
<small>Units per store per week. P80 is a sensible replenishment level: demand stays at or below it in about 4 of 5 weeks. Same forecast in every store (store made no difference).</small></div>

<h2>What we found</h2>
<ul>
<li><b>Article is the only driver.</b> It explains 54% of weekly variation. Store, month, shelf life and last week's sales explain almost nothing.</li>
<li><b>No trend or seasonality</b> in one year: total demand is flat at about 1,600 units per week.</li>
<li><b>Complex models add nothing.</b> LightGBM and Poisson models are within 1–2% of the plain average (differences smaller than fold-to-fold noise).</li>
<li><b>Small sellers are unpredictable.</b> Error is 0.63 for the slowest quarter of series versus 0.34 for the fastest.</li>
</ul>
<img alt="Average weekly units by article and the flat weekly total" src="{img('05_signal')}">

<h2>Model comparison</h2>
<img alt="Cross-validated WAPE by model" src="{img('06_cv')}">
<p>Rolling-origin cross-validation inside the training weeks. The orange bar is the chosen model: the simplest one within 1% of the best.</p>
<div class="card"><b>Test result (12 weeks, used once).</b> Chosen {m['test_wape']:.3f} · expanding mean {b['baseline: expanding mean']:.3f} · 8-week mean {b['baseline: 8-week mean']:.3f} · last week {b['baseline: last week']:.3f}. Difference to the expanding mean: {m['wape_diff_vs_best_baseline']['mean']:+.3f} (95% CI {m['wape_diff_vs_best_baseline']['ci95'][0]:+.3f} to {m['wape_diff_vs_best_baseline']['ci95'][1]:+.3f}), so <b>not distinguishable</b>. The original stretch goal (WAPE ≤ 0.40) was not met and is not realistic on this data.</div>

<h2>Where it is wrong</h2>
<table id="tbl"><thead><tr><th data-k="ARTICLE">Article</th><th data-k="mean_weekly_units_per_store">Avg units / store / week</th><th data-k="wape">Test WAPE</th><th data-k="bias">Bias</th></tr></thead><tbody></tbody></table>
<small>Click a header to sort. Article biases of ±15% come from 60 store-weeks each and may be noise.</small>
<img style="margin-top:16px" alt="Forecast error by article" src="{img('07_error_article')}">
<div class="note">The P10–P90 band is not equally reliable everywhere: Vegetables 86%, Dairy 75%, East store 76% coverage.</div>

<h2>Limitations</h2>
<ul><li>The data is synthetic (generated 2026-05-22). It tests the method, not real demand.</li>
<li>One year: no annual seasonality can be learned. 8% of sale lines lacked an article and were dropped; returns are excluded.</li>
<li>No stock, promotion or holiday data; stock-outs would hide true demand.</li></ul>

<h2>Next steps</h2>
<ul><li>Re-run the same pipeline on real POS data (it will pick up trend, seasonality and store effects if they exist).</li>
<li>Collect stock levels, promotions and holidays. Use division-specific bands for Dairy.</li>
<li>Score weekly with <code>models/score.py</code>; retrain monthly; alert if WAPE &gt; 0.55 for 4 weeks.</li></ul>

<h2>Reproducibility</h2>
<p><small>Project projects/perishable-demand-forecast · stages 01–08 notebooks in notebooks/ · seed 42 · time-ordered split (train to 2024-12-30, test 2025-01-06 → 2025-03-24) · decisions in DECISIONS.md · model card in reports/model_card.md.</small></p>
</main>
<script>
const D={json.dumps(data)};
const sel=document.getElementById('art'),bands=document.getElementById('bands');
D.rows.slice().sort((a,b)=>a.ARTICLE.localeCompare(b.ARTICLE)).forEach(r=>sel.add(new Option(r.ARTICLE,r.ARTICLE)));
function show(){{const r=D.rows.find(x=>x.ARTICLE===sel.value),m=r.mean_weekly_units_per_store;
bands.innerHTML=[['Average',m,1],['P10',m,D.q['0.1']],['P50',m,D.q['0.5']],['P80',m,D.q['0.8']],['P90',m,D.q['0.9']]].map(([l,a,k])=>`<div><small>${{l}}</small><b>${{(a*k).toFixed(1)}}</b></div>`).join('');}}
sel.onchange=show;show();
let key='wape',dir=-1;const tb=document.querySelector('#tbl tbody');
function draw(){{tb.innerHTML=D.rows.slice().sort((a,b)=>(typeof a[key]==='string'?a[key].localeCompare(b[key]):a[key]-b[key])*dir).map(r=>`<tr><td>${{r.ARTICLE}}</td><td>${{r.mean_weekly_units_per_store.toFixed(1)}}</td><td>${{r.wape.toFixed(2)}}</td><td>${{(r.bias*100).toFixed(1)}}%</td></tr>`).join('');}}
document.querySelectorAll('#tbl th').forEach(th=>th.onclick=()=>{{const k=th.dataset.k;dir=k===key?-dir:-1;key=k;draw();}});draw();
</script></body></html>"""
Path("reports/report.html").write_text(html)
print("reports/report.html", len(html) // 1024, "KB")
