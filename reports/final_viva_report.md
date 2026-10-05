# NBA MVP Prediction — Final Viva Report

> Comprehensive, self-explanatory report covering the full project: motivation, setup, data, methodology, models, results, analysis, improvements over the reference, limitations, and viva preparation.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Project Motivation](#2-project-motivation)
3. [What Was Implemented](#3-what-was-implemented)
4. [Dataset and Features](#4-dataset-and-features)
5. [Methodology and Workflow](#5-methodology-and-workflow)
6. [Models and Evaluation](#6-models-and-evaluation)
7. [Results and Analysis](#7-results-and-analysis)
8. [Improvements Over the Reference Sample](#8-improvements-over-the-reference-sample)
9. [Limitations and Future Work](#9-limitations-and-future-work)
10. [How to Run the Project](#10-how-to-run-the-project)
11. [Live Demo Script](#11-live-demo-script)
12. [Key Viva Questions and Answers](#12-key-viva-questions-and-answers)
13. [File Reference](#13-file-reference)
14. [Conclusion](#14-conclusion)

---

## 1. Executive Summary

| Item | Details |
|------|---------|
| **Course** | UE24CS352A — Machine Learning |
| **Project title** | Predicting the NBA MVP with Machine Learning |
| **Problem** | Can we predict the NBA MVP winner using only objective player statistics? |
| **Models used** | Gaussian Naive Bayes, Logistic Regression |
| **Dataset** | 20 seasons (2000-01 to 2019-20), top 3 MVP finalists per season |
| **Best result** | **Logistic Regression — 66.7% seasonal accuracy** |
| **Deliverables** | Code repository, HTML poster, PowerPoint slides, README, this report |

This project builds a complete, reproducible machine-learning pipeline to classify the NBA MVP from the top three finalists each season. Logistic Regression outperforms Naive Bayes, confirming that a discriminative linear boundary works better when basketball statistics are correlated.

---

## 2. Project Motivation

The NBA Most Valuable Player (MVP) award is decided by a panel of sportswriters and broadcasters. Human voters are influenced by:

- **Media narratives** and hype
- **Team success** and market size
- **Popularity** and star power
- **Recency bias** (late-season performance)

This makes MVP voting partly subjective. The project asks a concrete ML question:

> **Can machine learning predict the MVP using only objective, publicly available player statistics?**

We chose two classical algorithms — Naive Bayes and Logistic Regression — because they:
- Are interpretable and fast.
- Represent two major ML families: **generative** vs. **discriminative**.
- Match the scope and tools expected for a one-week mini-project.

---

## 3. What Was Implemented

A complete end-to-end pipeline was built under the `nba-mvp-ml/` folder:

### Infrastructure
- Clean project folder structure (`data/`, `src/`, `reports/`, `notebooks/`).
- Python virtual environment (`venv/`) with all dependencies pinned in `requirements.txt`.
- Local Git repository initialized and committed.

### Data Engineering
- Downloaded the Kaggle dataset *1982-2022 NBA Player Statistics with MVP Votes* using `kagglehub`.
- Filtered seasons 2000-01 to 2019-20.
- Selected the top 3 MVP finalists per season by `award_share`.
- Built binary labels: `MVP = 1` for the highest award share, `0` otherwise.
- Handled missing 3-point percentages by filling with `0.0` (players with no 3-point attempts).

### Modeling
- Trained **Gaussian Naive Bayes** on raw features.
- Trained **Logistic Regression** on standardized features.
- Evaluated both models in **pure** and **seasonal** prediction modes.

### Visualization and Reporting
- Generated accuracy comparison chart, confusion matrices, and feature-importance plot.
- Created a one-page HTML poster (`reports/poster.html`).
- Created a 20-slide PowerPoint deck (`reports/presentation/NBA_MVP_Prediction.pptx`).
- Wrote setup guide and this final viva report.

---

## 4. Dataset and Features

### Data Source
- **Original source:** [Basketball-Reference](https://www.basketball-reference.com/)
- **Downloaded from:** Kaggle — [NBA Player Season Statistics with MVP Win Share](https://www.kaggle.com/datasets/robertsunderhaft/nba-player-season-statistics-with-mvp-win-share)
- **Why this dataset:** It already contains MVP vote shares (`award_share`) for every player-season, so we can identify finalists and winners without scraping Basketball-Reference directly.

### Dataset Summary

| Property | Value |
|----------|-------|
| Seasons | 2000-01 to 2019-20 |
| Total rows | 60 |
| Rows per season | Top 3 MVP finalists |
| Training rows | 48 (2000-01 to 2015-16) |
| Test rows | 12 (2016-17 to 2019-20) |
| Features | 10 per-game statistics |
| Target | `MVP` = 1 (winner), 0 (runner-up) |

### Features Used

| Feature | Description | Why It Matters |
|---------|-------------|----------------|
| `g` | Games played | Availability and durability |
| `mp_per_g` | Minutes per game | Star players usually play more |
| `fg_pct` | Field goal percentage | Scoring efficiency |
| `fg3_pct` | 3-point percentage | Modern scoring skill |
| `ft_pct` | Free throw percentage | Free-throw efficiency |
| `trb_per_g` | Total rebounds per game | All-around contribution |
| `ast_per_g` | Assists per game | Playmaking ability |
| `stl_per_g` | Steals per game | Defensive activity |
| `blk_per_g` | Blocks per game | Rim protection |
| `pts_per_g` | Points per game | Most visible offensive stat |

### Train-Test Split
We used a **chronological split** rather than a random split. This mirrors real-world prediction: we train on past seasons and test on future seasons.

---

## 5. Methodology and Workflow

### End-to-End Workflow

```
Raw Kaggle Data
      ↓
Filter seasons (2000-01 to 2019-20)
      ↓
Select top 3 finalists per season by award_share
      ↓
Create MVP labels
      ↓
Split chronologically: train 2000-2016, test 2017-2020
      ↓
Train Naive Bayes + Logistic Regression
      ↓
Evaluate in pure and seasonal modes
      ↓
Analyze results, feature importance, limitations
      ↓
Generate poster, slides, and reports
```

### Why These Models?

| Aspect | Naive Bayes | Logistic Regression |
|--------|-------------|---------------------|
| Type | Generative | Discriminative |
| Learns | P(features | class) | P(class | features) |
| Independence assumption | Yes | No |
| Needs scaling | No | Yes |
| Speed | Very fast | Fast |
| Interpretability | Moderate | High (coefficients) |

### Evaluation Modes

1. **Pure MVP Prediction**
   - Binary classification of any finalist as MVP or not.
   - Decision threshold on predicted probability: 0.5.
   - Standard accuracy metric.

2. **Seasonal MVP Prediction**
   - Exactly one MVP must be chosen per season.
   - Select the finalist with the highest predicted probability within that season.
   - More realistic and stricter metric.

---

## 6. Models and Evaluation

### Gaussian Naive Bayes
- Used `sklearn.naive_bayes.GaussianNB`.
- Trained directly on the 10 raw features.
- Assumes each feature follows a Gaussian distribution conditioned on the class.

### Logistic Regression
- Used `sklearn.linear_model.LogisticRegression`.
- Features standardized using `StandardScaler`.
- `max_iter=1000`, `random_state=42`.
- Outputs probabilities used for both pure and seasonal modes.

### Code Files
- `src/data_preparation.py` — data download and cleaning.
- `src/models.py` — model training, evaluation, and metric saving.
- `src/visualizations.py` — result plots.
- `src/create_presentation_improved.py` — improved slide deck generator.

---

## 7. Results and Analysis

### Accuracy Table

| Model | Train (pure) | Test (pure) | Test (seasonal) |
|-------|--------------|-------------|-----------------|
| Naive Bayes | 60.4% | 41.7% | 50.0% |
| Logistic Regression | 79.2% | 50.0% | **66.7%** |

### Confusion Matrices (Pure Mode)

**Naive Bayes**
| | Pred Non-MVP | Pred MVP |
|---|:---:|:---:|
| Actual Non-MVP | 3 | 5 |
| Actual MVP | 2 | 2 |

**Logistic Regression**
| | Pred Non-MVP | Pred MVP |
|---|:---:|:---:|
| Actual Non-MVP | 2 | 6 |
| Actual MVP | 0 | 4 |

### Key Observations

- **Logistic Regression wins on the realistic seasonal task** (66.7% vs. 50.0%).
- **Naive Bayes underperforms** because basketball features are correlated, violating its independence assumption.
- Both models show a **train-test gap**, indicating some overfitting due to the small 48-row training set.
- Logistic Regression never misses an actual MVP in pure mode (0 false negatives), but it has more false positives.

### Feature Importance (Logistic Regression Coefficients)

Ranked by absolute coefficient:

| Rank | Feature | Direction | Interpretation |
|------|---------|-----------|----------------|
| 1 | Assists per game | + | Playmaking strongly signals MVP |
| 2 | Free throw % | + | Efficiency at the line matters |
| 3 | Points per game | + | High scoring is expected |
| 4 | Blocks per game | + | Defensive presence helps |
| 5 | Rebounds per game | + | All-around contribution |
| 6 | 3-point % | + | Outside shooting skill |
| 7 | Minutes per game | - | Raw minutes without production may hurt |
| 8 | Steals per game | - | Less predictive in this dataset |
| 9 | Field goal % | + | Mild positive effect |
| 10 | Games played | + | Mild positive effect |

### Why Predictions Differ from Actual Winners

- **Voter bias:** voters reward narrative, popularity, and team success.
- **Missing team features:** wins, playoff seed, and point differential are not included.
- **Missing advanced stats:** PER, win shares, VORP capture value better than raw per-game stats.
- **Small data:** only 60 rows limit model generalization.

---

## 8. Improvements Over the Reference Sample

The reference sample project (`ML Mini Project.pdf`) predicted the 2021 MVP using Naive Bayes and Logistic Regression. Our work improves upon it in several ways:

| Improvement | How We Did It |
|-------------|---------------|
| **Reproducibility** | Every step is scripted: data download, cleaning, training, evaluation, visualization, and slide generation. |
| **Data reliability** | Used a verified Kaggle dataset instead of manual scraping, with clear provenance. |
| **Evaluation rigor** | Added a second evaluation mode (seasonal) that reflects real MVP selection. |
| **Feature analysis** | Ranked and interpreted logistic regression coefficients. |
| **Visualizations** | Produced accuracy charts, confusion matrices, and feature-importance plots. |
| **Deliverables** | Created a professional HTML poster and a comprehensive 20-slide PowerPoint deck. |
| **Documentation** | Provided README, setup guide, and this detailed viva report with Q&A. |
| **Git readiness** | Initialized a local Git repository with a clean commit history. |

---

## 9. Limitations and Future Work

### Limitations

**Data limitations:**
- Very small dataset (60 rows).
- Only top 3 finalists considered; many valuable seasons ignored.
- No team-level statistics (wins, seed, point differential).
- No advanced metrics (PER, WS, VORP, BPM).
- No injury or load-management information.

**Modeling limitations:**
- Naive Bayes assumes feature independence, which is violated.
- Logistic Regression is linear and may miss non-linear patterns.
- No ensemble methods or hyperparameter tuning.
- Cannot capture voter subjectivity or media narrative.

### Future Work

- Add team-level features and advanced player metrics.
- Expand to all MVP vote-getters, not just the top 3.
- Use more recent seasons for testing.
- Apply cross-validation and hyperparameter tuning.
- Try ensemble models: Random Forest, Gradient Boosting, XGBoost.
- Use actual MVP vote counts as a continuous target for regression.

---

## 10. How to Run the Project

Open Git Bash in the `nba-mvp-ml/` folder:

```bash
# Activate environment
source venv/Scripts/activate

# Install dependencies (if needed)
pip install -r requirements.txt

# Download and prepare data
python src/data_preparation.py

# Train and evaluate models
python src/models.py

# Generate visualizations
python src/visualizations.py

# Generate improved slides
python src/create_presentation_improved.py
```

### Convert Poster to PDF

1. Open `reports/poster.html` in a browser.
2. Press `Ctrl + P`.
3. Destination: **Save as PDF**.
4. Layout: **Landscape** (recommended).
5. Click Save.

---

## 11. Live Demo Script

Use this flow during your review:

1. **Introduce the problem** — subjective MVP voting, objective stats.
2. **Show the dataset** — open `data/processed/mvp_finalists_2001_2020.csv`.
3. **Explain features** — the 10 per-game statistics.
4. **Run the pipeline:**
   ```bash
   python src/data_preparation.py
   python src/models.py
   ```
5. **Show results** — open `results/metrics.json` and explain the accuracy table.
6. **Show plots** — open the three PNG files in `reports/figures/`.
7. **Highlight the best result** — Logistic Regression, 66.7% seasonal accuracy.
8. **Discuss feature importance** — assists, FT%, points, blocks, rebounds.
9. **Show limitations** — small data, missing narrative/team features.
10. **Open poster and slides** for the panel.

---

## 12. Key Viva Questions and Answers

### Q1. What is the problem you are solving?
**A:** We predict the NBA MVP winner from the top three finalists each season using only objective player statistics, and we compare Naive Bayes with Logistic Regression.

### Q2. Why did you choose these two models?
**A:** They are interpretable, fast, and represent two important families: Naive Bayes is generative and Logistic Regression is discriminative. This lets us compare how each approach handles the same small, real-world dataset.

### Q3. What is the difference between generative and discriminative models?
**A:** Generative models learn how the data for each class is generated, P(features | class). Discriminative models learn the decision boundary directly, P(class | features).

### Q4. What are the features?
**A:** Ten per-game statistics: games played, minutes, FG%, 3P%, FT%, rebounds, assists, steals, blocks, and points.

### Q5. How did you split train and test?
**A:** Chronologically. Training: 2000-01 to 2015-16 (48 rows). Testing: 2016-17 to 2019-20 (12 rows). This mirrors real prediction where future seasons are unknown during training.

### Q6. What are the two evaluation modes?
**A:** Pure mode classifies each finalist independently. Seasonal mode picks exactly one MVP per season, which is closer to reality.

### Q7. Which model performed better and why?
**A:** Logistic Regression achieved 66.7% seasonal accuracy vs. 50.0% for Naive Bayes. Basketball stats are correlated, violating Naive Bayes' independence assumption. Logistic Regression learns a direct linear boundary and works better here.

### Q8. What are the most important features?
**A:** Assists per game, free-throw percentage, points per game, blocks per game, and rebounds per game.

### Q9. Why is accuracy not higher?
**A:** The dataset is very small (60 rows), and we excluded team success, advanced metrics, and voter narrative factors that strongly influence MVP voting.

### Q10. How did you improve upon the reference sample project?
**A:** We built a fully reproducible scripted pipeline, used a verified dataset, added seasonal evaluation, analyzed feature importance, created professional visualizations, and produced a poster, slides, and detailed documentation.

### Q11. What are the limitations?
**A:** Small data, only top-3 finalists, no team/advanced stats, and no modeling of voter bias.

### Q12. What would you do next?
**A:** Add team-level features and advanced metrics, expand the dataset, apply cross-validation, and try ensemble models like Random Forest or XGBoost.

---

## 13. File Reference

| File | Purpose |
|------|---------|
| `README.md` | Setup and project overview |
| `requirements.txt` | Python dependencies |
| `src/data_preparation.py` | Download and clean data |
| `src/models.py` | Train and evaluate models |
| `src/visualizations.py` | Generate plots |
| `src/create_presentation_improved.py` | Generate improved slides |
| `data/processed/mvp_finalists_2001_2020.csv` | Clean modeling dataset |
| `models/trained_models.pkl` | Saved trained models |
| `results/metrics.json` | Model accuracy metrics |
| `results/*_test_predictions.csv` | Detailed predictions |
| `results/logistic_regression_feature_importance.csv` | Feature rankings |
| `reports/figures/*.png` | Result plots |
| `reports/poster.html` | One-page poster (print to PDF) |
| `reports/presentation/NBA_MVP_Prediction.pptx` | Slide deck |
| `reports/project_setup_and_data_guide.md` | Setup and topic guide |
| `reports/final_viva_report.md` | This comprehensive report |

---

## 14. Conclusion

This project successfully built a reproducible machine-learning pipeline for NBA MVP prediction. Logistic Regression outperformed Naive Bayes with a **66.7% seasonal accuracy**, demonstrating that discriminative models handle correlated basketball statistics better than generative models that assume feature independence.

The results also highlight an important real-world lesson: while statistics are strong predictors, MVP voting remains partly subjective. Team success, media narrative, and voter bias are not captured by per-game player stats alone.

All deliverables — code, data, models, visualizations, poster, slides, and documentation — are ready for submission and viva presentation.

---

*Report generated for the UE24CS352A Machine Learning Mini Project viva.*
