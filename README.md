# NBA MVP Prediction — Machine Learning Mini Project

Predict the NBA Most Valuable Player (MVP) using historical player statistics and two classical ML algorithms: **Naive Bayes** and **Logistic Regression**.

## Project Overview

The NBA MVP is decided by a panel of sportswriters and broadcasters, which makes it partly subjective. This project asks: **can machine learning predict the MVP using only objective season statistics?** We compare a generative model (Naive Bayes) and a discriminative model (Logistic Regression) on the task of classifying the top three MVP finalists each season.

## Deliverables

- **Source code** in this GitHub repository.
- **One-page write-up / poster** (`reports/`).
- **Slide deck** for presentation + live demo.

## Repository Structure

```
nba-mvp-ml/
├── data/
│   ├── raw/                # Original downloaded dataset
│   └── processed/          # Cleaned dataset ready for modeling
├── notebooks/              # Jupyter notebooks for exploration
├── src/
│   └── data_preparation.py # Downloads and cleans the data
├── reports/                # Write-up and presentation files
├── README.md               # This file
├── requirements.txt        # Python dependencies
└── .gitignore
```

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd nba-mvp-ml
   ```

2. **Create and activate the virtual environment**

   ```bash
   python -m venv venv
   source venv/Scripts/activate   # On Windows Git Bash
   # venv\Scripts\activate         # On Windows CMD/PowerShell
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download and prepare the data**

   ```bash
   python src/data_preparation.py
   ```

   This downloads the Kaggle dataset *1982-2022 NBA Player Statistics with MVP Votes* and produces `data/processed/mvp_finalists_2001_2020.csv`.

## Dataset

- **Source:** Kaggle — [NBA Player Season Statistics with MVP Win Share](https://www.kaggle.com/datasets/robertsunderhaft/nba-player-season-statistics-with-mvp-win-share), originally scraped from [Basketball-Reference](https://www.basketball-reference.com/).
- **Timeframe:** 2000-01 to 2019-20 seasons.
- **Rows:** 60 (20 seasons × top 3 MVP finalists).
- **Train split:** 2000-01 to 2015-16 (48 rows).
- **Test split:** 2016-17 to 2019-20 (12 rows).

### Features Used

| Feature     | Description                  |
|-------------|------------------------------|
| `g`         | Games played                 |
| `mp_per_g`  | Minutes per game             |
| `fg_pct`    | Field goal percentage        |
| `fg3_pct`   | 3-point percentage           |
| `ft_pct`    | Free throw percentage        |
| `trb_per_g` | Total rebounds per game      |
| `ast_per_g` | Assists per game             |
| `stl_per_g` | Steals per game              |
| `blk_per_g` | Blocks per game              |
| `pts_per_g` | Points per game              |

### Target

- `MVP = 1` for the finalist with the highest MVP award share that season.
- `MVP = 0` for the other two finalists.

## Next Steps

1. Train Naive Bayes and Logistic Regression models.
2. Evaluate in two modes:
   - **Pure MVP:** classify any finalist as MVP or not.
   - **Seasonal MVP:** pick exactly one MVP from the three finalists each season.
3. Generate results, write-up, and slides.

## Team

- <Your Name>
- <Partner Name>
