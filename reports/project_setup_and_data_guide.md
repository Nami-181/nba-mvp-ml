# NBA MVP Prediction Project — Setup & Topic Guide

> Use this document to understand what has been prepared so far and what to say during your college viva.

---

## 1. What Is This Project About?

**Problem Statement:**  
The NBA Most Valuable Player (MVP) award is decided by human voters (sportswriters and broadcasters). Human voters can be influenced by popularity, team success, media narratives, and recent performance. This project asks:

> **Can we predict the MVP winner using only objective player statistics and machine learning?**

We use two classical ML algorithms taught in class:
- **Naive Bayes** — a generative probabilistic classifier.
- **Logistic Regression** — a discriminative linear classifier.

We compare them to see which one better captures how voters actually pick the MVP.

---

## 2. Why This Topic?

- Basketball produces rich, structured statistics.
- MVP voting is subjective, making it an interesting ML case study.
- It lets us compare a **generative** model (Naive Bayes) vs. a **discriminative** model (Logistic Regression) on the same real-world task.
- The dataset is small and manageable, perfect for a one-week mini-project.

---

## 3. What Has Been Set Up So Far?

### 3.1 Project Folder Structure

Created a clean Python project:

```
nba-mvp-ml/
├── data/raw/              # Original downloaded data
├── data/processed/        # Clean dataset for modeling
├── notebooks/             # Jupyter notebooks
├── src/                   # Python scripts
├── reports/               # Write-up, slides, and this guide
├── README.md              # Setup instructions
├── requirements.txt       # Python packages
└── venv/                  # Virtual environment
```

### 3.2 Virtual Environment & Packages

- Created a Python virtual environment (`venv/`).
- Installed core ML/data libraries:
  - `pandas`, `numpy` — data handling
  - `scikit-learn` — Naive Bayes and Logistic Regression
  - `matplotlib`, `seaborn` — visualization
  - `jupyter` — notebooks for exploration
  - `kagglehub` — to download the dataset

### 3.3 Data Source

- **Original source:** [Basketball-Reference](https://www.basketball-reference.com/) (manually scraped by the Kaggle dataset author).
- **Downloaded from:** Kaggle — [*1982-2022 NBA Player Statistics with MVP Votes*](https://www.kaggle.com/datasets/robertsunderhaft/nba-player-season-statistics-with-mvp-win-share).
- **Why this source?** It already contains MVP vote shares (`award_share`) for every player-season, so we can identify finalists and winners without scraping Basketball-Reference ourselves.

### 3.4 Data Preparation

The script `src/data_preparation.py` does the following:

1. Downloads the dataset via `kagglehub`.
2. Filters seasons from **2000-01 to 2019-20**.
3. For each season, selects the **top 3 players by MVP award share** — these are the finalists.
4. Labels the finalist with the highest `award_share` as `MVP = 1`, the other two as `MVP = 0`.
5. Keeps only the 10 features used in the sample project.
6. Saves the result to `data/processed/mvp_finalists_2001_2020.csv`.

### 3.5 Final Dataset Summary

| Property            | Value                                    |
|---------------------|------------------------------------------|
| Total rows          | 60 (20 seasons × 3 finalists)            |
| Training rows       | 48 (2000-01 to 2015-16)                  |
| Test rows           | 12 (2016-17 to 2019-20)                  |
| Features            | 10 per-game statistics                   |
| Target              | MVP (1 = winner, 0 = runner-up)          |

### 3.6 Features Used

| Feature     | Full Name                    | Why It Matters for MVP                |
|-------------|------------------------------|----------------------------------------|
| `g`         | Games played                 | Availability matters to voters         |
| `mp_per_g`  | Minutes per game             | Star players play more                 |
| `fg_pct`    | Field goal percentage        | Scoring efficiency                     |
| `fg3_pct`   | 3-point percentage           | Modern scoring skill                   |
| `ft_pct`    | Free throw percentage        | Free-throw efficiency                  |
| `trb_per_g` | Total rebounds per game      | All-around contribution                |
| `ast_per_g` | Assists per game             | Playmaking ability                     |
| `stl_per_g` | Steals per game              | Defensive impact                       |
| `blk_per_g` | Blocks per game              | Defensive presence                     |
| `pts_per_g` | Points per game              | Most visible offensive stat            |

---

## 4. How to Run What Has Been Prepared

Open Git Bash / terminal in the project folder:

```bash
# Activate the virtual environment
source venv/Scripts/activate

# Re-run data preparation (if needed)
python src/data_preparation.py

# Check the processed data
python -c "import pandas as pd; print(pd.read_csv('data/processed/mvp_finalists_2001_2020.csv').head())"
```

---

## 5. Key Talking Points for the Viva

### What is the MVP?
- The NBA MVP is awarded to the best performing player of the regular season.
- Voted by a panel of ~100 sportswriters and broadcasters.
- Each voter ranks 5 players; points are assigned 10-7-5-3-1. The player with the most points wins.

### Why Use Machine Learning?
- Remove human bias (popularity, media hype, recency bias).
- Identify which statistics are most predictive of MVP voting.
- Build a reproducible decision rule.

### Why Naive Bayes?
- **Generative model**: learns how the data for each class (MVP vs. non-MVP) is generated.
- Fast to train, works well with small datasets.
- Assumes feature independence (the "naive" part).

### Why Logistic Regression?
- **Discriminative model**: directly learns the decision boundary between MVP and non-MVP.
- Outputs probabilities.
- Works well when classes are roughly linearly separable.

### What Are the Two Prediction Modes?
1. **Pure MVP:** The model classifies any finalist as MVP or not, without the constraint of one winner per season.
2. **Seasonal MVP:** The model must pick exactly one MVP from the three finalists each season.

### Expected Challenges
- **Small dataset:** only 60 rows, so models can overfit.
- **Voter subjectivity:** statistics do not capture team record, narrative, or popularity.
- **Feature correlation:** basketball stats are often correlated (e.g., minutes and points), which violates Naive Bayes' independence assumption.

---

## 6. What Comes Next?

The next phases of the project are:

1. **Model Training** — train Gaussian Naive Bayes and Logistic Regression.
2. **Evaluation** — compute accuracy for both pure and seasonal modes.
3. **Analysis** — compare models, list top predictive features, discuss errors.
4. **Report** — create the one-page poster / write-up.
5. **Slides** — prepare the PPT and live demo.

---

## 7. Files You Should Know

| File                                              | Purpose                                   |
|---------------------------------------------------|-------------------------------------------|
| `README.md`                                       | Setup and project overview                |
| `src/data_preparation.py`                         | Downloads and cleans the dataset          |
| `data/processed/mvp_finalists_2001_2020.csv`      | Clean dataset for modeling                |
| `requirements.txt`                                | List of Python packages                   |
| `reports/project_setup_and_data_guide.md`         | This viva-prep guide                      |

---

*Prepared for the UE24CS352A Machine Learning Mini Project.*
