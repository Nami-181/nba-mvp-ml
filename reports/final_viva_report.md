# NBA MVP Prediction — Final Viva Report

> Comprehensive report covering the full project: setup, data, models, results, deliverables, and viva talking points.

---

## 1. Project Summary

| Item | Details |
|------|---------|
| **Course** | UE24CS352A — Machine Learning |
| **Topic** | Predicting the NBA MVP using Naive Bayes and Logistic Regression |
| **Team size** | 2 (per assignment guidelines) |
| **Dataset** | Kaggle / Basketball-Reference, 2000-01 to 2019-20 |
| **Models** | Gaussian Naive Bayes, Logistic Regression |
| **Best result** | Logistic Regression — 66.7% seasonal accuracy |
| **Deliverables** | Code repo, one-page poster (HTML), PPT slides, README, this report |

---

## 2. What Was Implemented

### 2.1 Project Setup

- Created a clean Python project structure under `nba-mvp-ml/`.
- Created a virtual environment `venv/`.
- Installed all required packages and pinned them in `requirements.txt`.
- Wrote `README.md` with setup and run instructions.

### 2.2 Data Collection & Preparation

- Downloaded the Kaggle dataset **"1982-2022 NBA Player Statistics with MVP Votes"** using `kagglehub`.
- The dataset was originally scraped from Basketball-Reference and contains per-game player statistics plus MVP award share.
- Processed the data with `src/data_preparation.py`:
  - Filtered seasons 2000-01 to 2019-20.
  - Selected the top 3 MVP finalists per season using `award_share`.
  - Labeled the finalist with the highest `award_share` as MVP (`1`), others as non-MVP (`0`).
  - Kept the 10 features used in the sample project.
  - Filled missing 3P% values with `0.0` (players with no 3-point attempts).
  - Saved the clean dataset to `data/processed/mvp_finalists_2001_2020.csv`.

**Final dataset:**
- 60 rows total
- 48 training rows (2000-01 to 2015-16)
- 12 test rows (2016-17 to 2019-20)

### 2.3 Model Training & Evaluation

Implemented in `src/models.py`:

- **Gaussian Naive Bayes** (`sklearn.naive_bayes.GaussianNB`)
  - Trained on raw features.
- **Logistic Regression** (`sklearn.linear_model.LogisticRegression`)
  - Features standardized with `StandardScaler`.
  - `max_iter=1000`, `random_state=42`.

**Two evaluation modes:**
1. **Pure MVP prediction** — binary classification of any finalist as MVP or not (threshold = 0.5).
2. **Seasonal MVP prediction** — for each season, pick the finalist with the highest predicted probability as the MVP.

### 2.4 Results

| Model | Train (pure) | Test (pure) | Test (seasonal) |
|-------|--------------|-------------|-----------------|
| Naive Bayes | 60.4% | 41.7% | 50.0% |
| Logistic Regression | 79.2% | 50.0% | **66.7%** |

**Confusion matrices (pure mode):**
- **Naive Bayes:** 3 true negatives, 5 false positives, 2 false negatives, 2 true positives.
- **Logistic Regression:** 2 true negatives, 6 false positives, 0 false negatives, 4 true positives.

**Feature importance (Logistic Regression coefficients):**
1. Assists per game (+)
2. Free throw percentage (+)
3. Points per game (+)
4. Blocks per game (+)
5. Rebounds per game (+)
6. 3-point percentage (+)
7. Minutes per game (−)
8. Steals per game (−)
9. Field goal percentage (+)
10. Games played (+)

### 2.5 Visualizations

Generated in `reports/figures/`:
- `accuracy_comparison.png` — bar chart comparing all accuracies.
- `confusion_matrices.png` — confusion matrices for both models.
- `feature_importance.png` — logistic regression coefficients.

### 2.6 Deliverables

- `reports/poster.html` — one-page academic poster (open in browser and print to PDF).
- `reports/presentation/NBA_MVP_Prediction.pptx` — 13-slide PowerPoint deck.
- `reports/project_setup_and_data_guide.md` — setup and topic guide.
- `reports/final_viva_report.md` — this document.

---

## 3. How to Run the Project

Open Git Bash in the `nba-mvp-ml/` folder:

```bash
# 1. Activate the virtual environment
source venv/Scripts/activate

# 2. (Optional) Re-install dependencies
pip install -r requirements.txt

# 3. Prepare the data
python src/data_preparation.py

# 4. Train and evaluate models
python src/models.py

# 5. Generate visualizations
python src/visualizations.py

# 6. Generate PPT
python src/create_presentation.py
```

The poster is at `reports/poster.html` (open in browser → Print → Save as PDF).

---

## 4. Key Viva Questions & Answers

### Q1: What is the problem you are solving?
**A:** We are predicting the NBA MVP winner using historical player statistics. Specifically, we compare Naive Bayes and Logistic Regression to see if machine learning can replicate or predict human MVP voting.

### Q2: Why did you choose Naive Bayes and Logistic Regression?
**A:** The assignment/sample project suggested these two classical algorithms. They also represent two important families:
- Naive Bayes is a **generative** probabilistic model.
- Logistic Regression is a **discriminative** linear model.
Comparing them shows which approach works better for this small, subjective dataset.

### Q3: What is the difference between generative and discriminative models?
**A:**
- **Generative** models learn how the data for each class is generated (e.g., P(features|MVP)).
- **Discriminative** models learn the decision boundary directly (e.g., P(MVP|features)).

### Q4: What are the features you used?
**A:** Ten per-game statistics: games played, minutes, FG%, 3P%, FT%, rebounds, assists, steals, blocks, and points.

### Q5: How did you handle the small dataset?
**A:** We used only the top 3 finalists per season to avoid extreme class imbalance. This gives 60 rows, which is small but manageable for classical ML. We also report both pure and seasonal accuracy to better reflect real-world MVP selection.

### Q6: Why does Logistic Regression perform better than Naive Bayes?
**A:** Basketball statistics are correlated (e.g., minutes and points, rebounds and blocks). Naive Bayes assumes feature independence, which is violated. Logistic Regression does not make this assumption and learns a direct decision boundary, so it generalizes better.

### Q7: What are the limitations?
**A:**
- Very small dataset (60 rows).
- Missing non-statistical factors: team wins, media narrative, voter bias, injuries.
- Models may overfit due to limited data.

### Q8: What is the real-world significance?
**A:** It shows that while statistics are important, MVP voting is partly subjective. ML can support but not fully replace human judgment in awards voting.

### Q9: What would you do in future work?
**A:**
- Add team-level features (wins, seed, point differential).
- Include advanced stats (PER, win shares, VORP).
- Use more seasons.
- Try ensemble models like Random Forest and XGBoost.

### Q10: How did you split train and test?
**A:** Training data: 2000-01 to 2015-16 (48 rows). Test data: 2016-17 to 2019-20 (12 rows). This is a chronological split, which mirrors real prediction where future seasons are unknown during training.

---

## 5. File Reference

| File | Purpose |
|------|---------|
| `README.md` | Setup and overview |
| `requirements.txt` | Python dependencies |
| `src/data_preparation.py` | Download & clean data |
| `src/models.py` | Train & evaluate models |
| `src/visualizations.py` | Generate plots |
| `src/create_presentation.py` | Generate PPT |
| `data/processed/mvp_finalists_2001_2020.csv` | Clean modeling dataset |
| `results/metrics.json` | Model accuracy metrics |
| `results/*_test_predictions.csv` | Detailed predictions |
| `reports/figures/*.png` | Result plots |
| `reports/poster.html` | One-page poster |
| `reports/presentation/NBA_MVP_Prediction.pptx` | Slide deck |
| `reports/project_setup_and_data_guide.md` | Setup/topic guide |
| `reports/final_viva_report.md` | This report |

---

## 6. Conclusion

The project successfully implemented a machine learning pipeline to predict NBA MVP winners. Logistic Regression achieved the best seasonal accuracy of **66.7%**, outperforming Naive Bayes. The results confirm that MVP voting has a strong subjective component that pure statistics cannot fully capture. All required deliverables — code, data, report, poster, and slides — have been prepared.

---

*Report generated for the UE24CS352A Machine Learning Mini Project viva.*
