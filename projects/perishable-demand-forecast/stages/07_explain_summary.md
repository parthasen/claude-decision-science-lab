# Stage 07 — Explainability and validation

## How the model decides
Forecast for an article in any store = that article's average weekly units per store over the training weeks (Apr–Dec 2024). Nothing else (store, week, shelf life, recent sales) is used, because stage 05 showed none of them carries signal. SHAP/PDP would only restate this, so they were skipped.

## Where it is wrong (test, 12 weeks)
- **By volume:** lowest-selling quarter of series WAPE 0.63, top quarter 0.34. Small counts are mostly noise. Worst articles: Kiwi 0.85, Baby Corn 0.70, Organic Milk 0.65, Chocolate Milk 0.64, Greek Yoghurt 0.64. Best: Apple Royal Gala 0.28, Banana 0.30, Tomato 0.34.
- **By division:** Vegetables 0.41, Fruits 0.44, Dairy & Milk 0.50 (under-forecast by 7.9%). Chilled items 0.50 vs Ambient 0.39.
- **By store:** WAPE 0.42–0.47; East under-forecast 10.2%, Metro over-forecast 6.4%. With 60 series-weeks per article and 12 weeks these gaps are consistent with random variation, but were not formally tested.
- **By month:** flat, WAPE 0.43–0.45 with bias within ±1.7%; no drift.

## Calibration
- Point forecast tracks actuals across all 8 forecast-size bins (e.g. forecast 12.8 vs actual 13.7 in the 6th bin, 28.5 vs 27.2 in the top bin).
- P10–P90 band covers 80.6% overall, but not evenly: Vegetables 86%, Dairy 75%, East store 76%. The intervals use one ratio for all articles, so they are too wide for vegetables and slightly narrow for dairy.

## Stability
Series means from the first vs second half of training correlate at 0.96. Test WAPE is 0.450 or 0.449 when using only one half of the training data (0.444 for a store×article mean, 0.439 for the chosen pooled-article mean), so the result does not depend on the window.

## Fairness
Not applicable: the model forecasts product counts, not people or protected groups.

## Verdict
Reliable as an average-level forecast with honest, wide bands; it does not predict weekly ups and downs, because the data contains none. Do not read article-level biases of ±15% (e.g. Full Cream Milk −16.7%, Mango +15.4%) as model faults without more weeks of data.
Improvement options if wanted: dairy-specific interval ratios; retrain monthly; collect stock-out, promotion and holiday data.

Model card: reports/model_card.md. Figures: figures/07_error_article.png, figures/07_calibration.png.
