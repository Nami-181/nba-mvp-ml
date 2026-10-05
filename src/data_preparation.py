"""
Data preparation script for NBA MVP prediction project.

This script downloads the NBA player statistics dataset from Kaggle
(1982-2022 NBA Player Statistics with MVP Votes) and processes it to
create a clean dataset containing the top 3 MVP finalists per season
from 2000-01 to 2019-20, with the 10 features used in the analysis.

Features used (matching the sample project):
- g: games played
- mp_per_g: minutes per game
- fg_pct: field goal percentage
- fg3_pct: 3-point percentage
- ft_pct: free throw percentage
- trb_per_g: total rebounds per game
- ast_per_g: assists per game
- stl_per_g: steals per game
- blk_per_g: blocks per game
- pts_per_g: points per game

The MVP label is 1 for the player with the highest award_share in a season,
and 0 for the other two finalists.
"""

import os
import shutil
import glob
import pandas as pd
import kagglehub


def download_dataset(cache_dir="data/raw/kaggle_mvp_dataset"):
    """Download the Kaggle NBA MVP dataset to the raw data directory."""
    os.makedirs(cache_dir, exist_ok=True)

    # Download using kagglehub
    src_path = kagglehub.dataset_download(
        "robertsunderhaft/nba-player-season-statistics-with-mvp-win-share"
    )

    # Copy CSV files from the downloaded cache to our project folder
    for f in glob.glob(os.path.join(src_path, "*")):
        if os.path.isfile(f):
            shutil.copy2(f, cache_dir)
            print(f"Copied: {os.path.basename(f)}")

    csv_files = glob.glob(os.path.join(cache_dir, "*.csv"))
    if not csv_files:
        raise FileNotFoundError("No CSV files found after download.")

    return csv_files[0]


def prepare_mvp_dataset(raw_csv_path, output_path="data/processed/mvp_finalists_2001_2020.csv"):
    """Process raw Kaggle data into top-3 finalists dataset."""
    df = pd.read_csv(raw_csv_path)

    # Filter seasons: 2000-01 to 2019-20 (stored as 2001 to 2020 in the dataset)
    df = df[(df["season"] >= 2001) & (df["season"] <= 2020)].copy()

    # Select top 3 MVP finalists per season by award_share
    top3_rows = []
    for season, group in df.groupby("season"):
        top3 = group.nlargest(3, "award_share")
        top3_rows.append(top3)
    top3 = pd.concat(top3_rows).reset_index(drop=True)

    # Label MVP: player with highest award_share in each season
    top3["MVP"] = 0
    mvp_idx = top3.groupby("season")["award_share"].idxmax()
    top3.loc[mvp_idx, "MVP"] = 1

    # Keep only the 10 features + metadata + label
    features = [
        "g", "mp_per_g", "fg_pct", "fg3_pct", "ft_pct",
        "trb_per_g", "ast_per_g", "stl_per_g", "blk_per_g", "pts_per_g",
    ]
    cols = ["season", "player", "team_id", "award_share"] + features + ["MVP"]
    final_df = top3[cols].copy()

    # Handle missing 3P% for players with no 3-point attempts (e.g., Shaq 2005)
    final_df["fg3_pct"] = final_df["fg3_pct"].fillna(0.0)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_df.to_csv(output_path, index=False)
    print(f"Processed dataset saved to: {output_path}")
    print(f"Total rows: {len(final_df)} ({final_df['season'].nunique()} seasons x top 3 finalists)")
    print(f"Training rows (2001-2016): {len(final_df[final_df['season'] <= 2016])}")
    print(f"Test rows (2017-2020): {len(final_df[final_df['season'] >= 2017])}")

    return final_df


if __name__ == "__main__":
    raw_csv = download_dataset()
    prepare_mvp_dataset(raw_csv)
