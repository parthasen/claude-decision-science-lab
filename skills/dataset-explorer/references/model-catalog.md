# Retail model catalog

| Objective (user wording) | Model type | Target / construction | Needs | Primary metric | Pitfalls |
|---|---|---|---|---|---|
| "How much will we sell next week?" | Demand forecast | units per store-SKU-day/week | ≥ 2 seasonal cycles; date, store, product, qty | WAPE, MAPE, bias | Stock-outs censor demand; promos and festivals need flags |
| "Who will stop buying?" | Churn / lapse classifier | 1 if no purchase in next N days after cut-off | Customer key (phone/loyalty ID), dates | PR-AUC, recall@top-k, lift | Anonymous walk-ins; label leakage from post-cut-off data |
| "Who are our customer types?" | RFM + K-Means segmentation | none | Customer key, dates, spend | Silhouette + business review | Wholesale/marketplace accounts skew clusters — separate them |
| "What is a customer worth?" | CLV (BG/NBD + Gamma-Gamma, or GBM) | spend in next 12 months | ≥ 1 year history | MAE, decile lift | Short history, one-time buyers |
| "What sells together?" | Basket analysis / recommender | none | Bill number + item | Support, confidence, lift | Carry-bag / non-inventory lines dominate — exclude |
| "How price-sensitive are we?" | Elasticity regression | log(qty) ~ log(price) + controls | Price variation over time | Elasticity CI, holdout error | Endogenous pricing; promotions confound |
| "Which promos work?" | Uplift / diff-in-diff | incremental sales vs control | Promo flags, control stores | Incremental margin | No random assignment |
| "Reduce waste / markdowns" | Forecast + newsvendor / markdown optimiser | units sold, units wasted | Expiry, stock, sales | Waste %, service level | Needs stock and expiry data, not just sales |
| "Spot bad bills / fraud" | Anomaly detection | none | Bill-level amounts, returns, cashier | Precision@k on reviewed cases | Legit bulk purchases flagged |
| "Which products should we stock?" | ABC/XYZ classification + forecast | value share, variability | Sales by SKU | Coverage of revenue | Seasonality mislabels items |
| "What will this return?" | Return-propensity classifier | Return bill link | Return bills linked to sale | ROC-AUC, PR-AUC | Return bills often unlinked |

## Selection rules
- Prefer the simplest model that beats a naive baseline (last-period, seasonal-naive, majority class) on a time-ordered holdout.
- Unsupervised objectives (segmentation, basket) are judged by usefulness to a decision, not accuracy.
- If the needed columns are missing, say which, and suggest which external data could fill them (weather, holiday calendar, footfall, competitor prices).
