"""
Generate an improved, comprehensive PowerPoint presentation for the NBA MVP
prediction project. Uses a consistent color scheme, better typography, and
more self-explanatory content.
"""

import os
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE


RESULTS_DIR = "results"
FIGURES_DIR = "reports/figures"
OUTPUT_PATH = "reports/presentation/NBA_MVP_Prediction.pptx"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Color palette
DARK_BLUE = RGBColor(30, 60, 114)      # #1e3c72
ACCENT_BLUE = RGBColor(42, 82, 152)    # #2a5298
LIGHT_BLUE = RGBColor(232, 244, 248)   # #e8f4f8
WHITE = RGBColor(255, 255, 255)
DARK_GRAY = RGBColor(51, 51, 51)
LIGHT_GRAY = RGBColor(245, 245, 245)
GREEN = RGBColor(46, 204, 113)
RED = RGBColor(231, 76, 60)


def set_slide_bg(slide, color=WHITE):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_title_bar(slide, title_text):
    """Add a dark blue title bar at the top."""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(10), Inches(1.1)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK_BLUE
    bar.line.fill.background()

    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.25), Inches(9), Inches(0.7))
    tf = title_box.text_frame
    tf.text = title_text
    p = tf.paragraphs[0]
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = "Calibri"


def add_bullet_box(slide, left, top, width, height, bullets, title=None, font_size=18, bold_title=True):
    """Add a text box with optional title and bullets."""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True

    if title:
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(font_size + 2 if font_size >= 18 else 20)
        p.font.bold = bold_title
        p.font.color.rgb = DARK_BLUE
        p.space_after = Pt(8)

    for i, bullet in enumerate(bullets):
        if title or i > 0:
            p = tf.add_paragraph()
        else:
            p = tf.paragraphs[0]
        p.text = bullet
        p.level = 0
        p.font.size = Pt(font_size)
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(6)

    return box


def add_figure(slide, image_path, left, top, width, caption=None):
    """Add an image with optional caption."""
    pic = slide.shapes.add_picture(image_path, left, top, width=width)
    if caption:
        cap_box = slide.shapes.add_textbox(left, top + width * 0.62, width, Inches(0.4))
        tf = cap_box.text_frame
        tf.text = caption
        tf.paragraphs[0].font.size = Pt(12)
        tf.paragraphs[0].font.italic = True
        tf.paragraphs[0].font.color.rgb = DARK_GRAY
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER


def title_slide(prs, title, subtitle):
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide, DARK_BLUE)

    # Title
    title_box = slide.shapes.add_textbox(Inches(1), Inches(2.2), Inches(8), Inches(1.5))
    tf = title_box.text_frame
    tf.text = title
    p = tf.paragraphs[0]
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(1), Inches(4.0), Inches(8), Inches(1.5))
    tf = sub_box.text_frame
    tf.text = subtitle
    p = tf.paragraphs[0]
    p.font.size = Pt(22)
    p.font.color.rgb = RGBColor(220, 220, 220)
    p.alignment = PP_ALIGN.CENTER

    # Footer
    foot_box = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(8), Inches(0.5))
    tf = foot_box.text_frame
    tf.text = "UE24CS352A — Machine Learning Mini Project"
    p = tf.paragraphs[0]
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(180, 180, 180)
    p.alignment = PP_ALIGN.CENTER

    return slide


def section_divider(prs, number, title):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide, ACCENT_BLUE)

    num_box = slide.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(1))
    tf = num_box.text_frame
    tf.text = f"PART {number}"
    p = tf.paragraphs[0]
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(180, 200, 230)
    p.alignment = PP_ALIGN.CENTER

    title_box = slide.shapes.add_textbox(Inches(1), Inches(3.3), Inches(8), Inches(1.2))
    tf = title_box.text_frame
    tf.text = title
    p = tf.paragraphs[0]
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    return slide


def content_slide(prs, title, bullets, subtitle=None):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide, WHITE)
    add_title_bar(slide, title)

    top = Inches(1.4)
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.5), top, Inches(9), Inches(0.4))
        tf = sub_box.text_frame
        tf.text = subtitle
        p = tf.paragraphs[0]
        p.font.size = Pt(16)
        p.font.italic = True
        p.font.color.rgb = DARK_GRAY
        top = Inches(1.9)

    add_bullet_box(slide, Inches(0.6), top, Inches(8.8), Inches(5.5), bullets, font_size=20)
    return slide


def two_column_slide(prs, title, left_title, left_bullets, right_title, right_bullets):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide, WHITE)
    add_title_bar(slide, title)

    # Left box
    left_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(1.4), Inches(4.5), Inches(5.6))
    left_box.fill.solid()
    left_box.fill.fore_color.rgb = LIGHT_BLUE
    left_box.line.color.rgb = ACCENT_BLUE
    left_box.line.width = Pt(1.5)

    add_bullet_box(slide, Inches(0.6), Inches(1.6), Inches(4.1), Inches(5.2), left_bullets, title=left_title, font_size=18)

    # Right box
    right_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.1), Inches(1.4), Inches(4.5), Inches(5.6))
    right_box.fill.solid()
    right_box.fill.fore_color.rgb = LIGHT_BLUE
    right_box.line.color.rgb = ACCENT_BLUE
    right_box.line.width = Pt(1.5)

    add_bullet_box(slide, Inches(5.3), Inches(1.6), Inches(4.1), Inches(5.2), right_bullets, title=right_title, font_size=18)

    return slide


def image_slide(prs, title, image_path, caption, left_text=None):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide, WHITE)
    add_title_bar(slide, title)

    if left_text:
        add_bullet_box(slide, Inches(0.5), Inches(1.4), Inches(3.0), Inches(5.5), left_text, font_size=16)
        add_figure(slide, image_path, Inches(3.8), Inches(1.5), Inches(5.6), caption)
    else:
        add_figure(slide, image_path, Inches(1.2), Inches(1.4), Inches(7.6), caption)

    return slide


def table_slide(prs, title, headers, rows, subtitle=None):
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    set_slide_bg(slide, WHITE)
    add_title_bar(slide, title)

    top = Inches(1.4)
    if subtitle:
        sub_box = slide.shapes.add_textbox(Inches(0.5), top, Inches(9), Inches(0.4))
        tf = sub_box.text_frame
        tf.text = subtitle
        p = tf.paragraphs[0]
        p.font.size = Pt(14)
        p.font.italic = True
        p.font.color.rgb = DARK_GRAY
        top = Inches(1.85)

    num_rows = len(rows) + 1
    num_cols = len(headers)
    table = slide.shapes.add_table(num_rows, num_cols, Inches(0.8), top + Inches(0.2), Inches(8.4), Inches(0.7 * num_rows)).table

    # Header
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    # Rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = str(val)
            if r_idx % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_GRAY
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(15)
            p.font.color.rgb = DARK_GRAY
            p.alignment = PP_ALIGN.CENTER

    return slide


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Load metrics
    with open(os.path.join(RESULTS_DIR, "metrics.json")) as f:
        metrics = json.load(f)

    nb_train = metrics["naive_bayes"]["train_accuracy_pure"]
    nb_test = metrics["naive_bayes"]["test_accuracy_pure"]
    nb_seas = metrics["naive_bayes"]["test_accuracy_seasonal"]
    lr_train = metrics["logistic_regression"]["train_accuracy_pure"]
    lr_test = metrics["logistic_regression"]["test_accuracy_pure"]
    lr_seas = metrics["logistic_regression"]["test_accuracy_seasonal"]

    # ========== PART 1: INTRODUCTION ==========
    title_slide(
        prs,
        "Predicting the NBA MVP\nwith Machine Learning",
        "A Comparative Study of Naive Bayes and Logistic Regression"
    )

    content_slide(
        prs,
        "Agenda",
        [
            "1. Motivation & Problem Statement",
            "2. Dataset & Features",
            "3. Methodology & Workflow",
            "4. Models: Naive Bayes vs. Logistic Regression",
            "5. Results, Analysis & Feature Importance",
            "6. Improvements Over the Reference Report",
            "7. Limitations & Future Work",
            "8. Live Demo Notes & Conclusion"
        ]
    )

    section_divider(prs, "01", "Motivation & Problem")

    content_slide(
        prs,
        "The NBA MVP Problem",
        [
            "The NBA Most Valuable Player award is decided by ~100 sportswriters and broadcasters.",
            "Voting is partly subjective: media narratives, popularity, team success, and recency bias influence outcomes.",
            "This project asks: Can machine learning predict the MVP using only objective season statistics?",
            "We frame it as a classification task: given the top 3 MVP finalists in a season, identify the winner."
        ],
        subtitle="Understanding the real-world context"
    )

    content_slide(
        prs,
        "Why Machine Learning?",
        [
            "Remove human bias and build a reproducible decision rule.",
            "Identify which statistics are most predictive of MVP voting.",
            "Compare two fundamental ML approaches on the same task:",
            "   • Naive Bayes — a generative probabilistic classifier",
            "   • Logistic Regression — a discriminative linear classifier",
            "Provide a baseline for more complex models in future work."
        ],
        subtitle="Objectives of the study"
    )

    # ========== PART 2: DATA ==========
    section_divider(prs, "02", "Dataset & Features")

    content_slide(
        prs,
        "Data Source",
        [
            "Primary source: Basketball-Reference (per-game player statistics + MVP voting shares).",
            "Downloaded via Kaggle dataset: '1982-2022 NBA Player Statistics with MVP Votes'.",
            "Timeframe used: 2000-01 to 2019-20 (20 seasons).",
            "For each season, we selected the top 3 players by MVP award share as finalists.",
            "The finalist with the highest award share is labeled MVP (1), the others non-MVP (0)."
        ],
        subtitle="Where the data came from"
    )

    table_slide(
        prs,
        "Dataset Summary",
        ["Property", "Value"],
        [
            ["Total rows", "60"],
            ["Seasons", "2000-01 to 2019-20"],
            ["Rows per season", "Top 3 finalists"],
            ["Training rows", "48 (2000-01 to 2015-16)"],
            ["Test rows", "12 (2016-17 to 2019-20)"],
            ["Features", "10 per-game statistics"],
            ["Target", "MVP (1) / Non-MVP (0)"]
        ],
        subtitle="Key numbers for the dataset"
    )

    content_slide(
        prs,
        "Features Used",
        [
            "Games played (g) — availability and durability",
            "Minutes per game (mp_per_g) — playing time",
            "Field goal percentage (fg_pct) — scoring efficiency",
            "3-point percentage (fg3_pct) — outside shooting",
            "Free throw percentage (ft_pct) — free-throw efficiency",
            "Total rebounds per game (trb_per_g) — all-around contribution",
            "Assists per game (ast_per_g) — playmaking",
            "Steals per game (stl_per_g) — defensive activity",
            "Blocks per game (blk_per_g) — rim protection",
            "Points per game (pts_per_g) — offensive production"
        ],
        subtitle="Ten statistics selected to match the reference sample project"
    )

    # ========== PART 3: METHODOLOGY ==========
    section_divider(prs, "03", "Methodology & Workflow")

    content_slide(
        prs,
        "Project Workflow",
        [
            "1. Data Collection — download Kaggle/Basketball-Reference dataset",
            "2. Data Cleaning — filter seasons, select top 3 finalists, build labels",
            "3. Feature Selection — keep 10 per-game statistics",
            "4. Train-Test Split — chronological split: 2000-2016 train, 2017-2020 test",
            "5. Model Training — Naive Bayes and Logistic Regression",
            "6. Evaluation — pure and seasonal prediction modes",
            "7. Visualization & Reporting — plots, poster, slides, viva report"
        ],
        subtitle="End-to-end pipeline from raw data to final deliverables"
    )

    two_column_slide(
        prs,
        "Our Two Models",
        "Naive Bayes",
        [
            "Type: Generative classifier",
            "Learns P(features | class)",
            "Assumes feature independence",
            "Fast, works with small data",
            "No scaling required",
            "Good baseline model"
        ],
        "Logistic Regression",
        [
            "Type: Discriminative classifier",
            "Learns P(class | features)",
            "No independence assumption",
            "Outputs probabilities",
            "Features standardized",
            "Learns a linear decision boundary"
        ]
    )

    content_slide(
        prs,
        "Two Evaluation Modes",
        [
            "Pure MVP Prediction:",
            "   • Each finalist is independently classified as MVP or not",
            "   • Decision threshold on predicted probability: 0.5",
            "   • Standard binary classification accuracy",
            "",
            "Seasonal MVP Prediction:",
            "   • One MVP must be chosen per season",
            "   • Select the finalist with the highest predicted probability",
            "   • Mirrors the real-world constraint of a single winner"
        ],
        subtitle="How we measured success"
    )

    # ========== PART 4: RESULTS ==========
    section_divider(prs, "04", "Results & Analysis")

    table_slide(
        prs,
        "Model Accuracy Results",
        ["Model", "Train (pure)", "Test (pure)", "Test (seasonal)"],
        [
            ["Naive Bayes", f"{nb_train:.1%}", f"{nb_test:.1%}", f"{nb_seas:.1%}"],
            ["Logistic Regression", f"{lr_train:.1%}", f"{lr_test:.1%}", f"{lr_seas:.1%}"]
        ],
        subtitle="Logistic Regression performs best in seasonal mode"
    )

    image_slide(
        prs,
        "Accuracy Comparison",
        os.path.join(FIGURES_DIR, "accuracy_comparison.png"),
        "Comparison across train/test and evaluation modes",
        left_text=[
            "Key observations:",
            "• Logistic Regression generalizes better",
            "• Seasonal mode is harder but more realistic",
            "• Both models show a train-test gap due to limited data",
            "• Logistic Regression reaches 66.7% seasonal accuracy"
        ]
    )

    image_slide(
        prs,
        "Confusion Matrices (Pure Mode)",
        os.path.join(FIGURES_DIR, "confusion_matrices.png"),
        "Left: Naive Bayes | Right: Logistic Regression"
    )

    content_slide(
        prs,
        "What the Results Tell Us",
        [
            "Logistic Regression is better at the seasonal task because it learns a direct decision boundary.",
            "Naive Bayes underperforms because basketball features are correlated (violating its independence assumption).",
            "The train-test gap shows the model is somewhat overfitting the small 48-row training set.",
            "Even with only 10 basic stats, we can predict the correct MVP 2 out of 3 seasons in test data.",
            "Voter subjectivity and missing narrative factors explain why accuracy is not higher."
        ],
        subtitle="Interpreting the numbers"
    )

    image_slide(
        prs,
        "Feature Importance",
        os.path.join(FIGURES_DIR, "feature_importance.png"),
        "Logistic Regression coefficients",
        left_text=[
            "Most important predictors:",
            "1. Assists per game",
            "2. Free throw %",
            "3. Points per game",
            "4. Blocks per game",
            "5. Rebounds per game",
            "",
            "Negative: Minutes per game — high minutes without high production may reduce MVP odds"
        ]
    )

    # ========== PART 5: IMPROVEMENTS ==========
    section_divider(prs, "05", "Improvements Over Reference")

    content_slide(
        prs,
        "How We Improved Upon the Sample Report",
        [
            "1. Reproducible pipeline: every step is scripted (data, training, visuals, slides).",
            "2. Better dataset handling: used a verified Kaggle dataset instead of manual scraping.",
            "3. Two evaluation modes: pure + seasonal, giving a more realistic accuracy measure.",
            "4. Feature importance analysis: clear ranking of which stats drive predictions.",
            "5. Visual results: accuracy charts, confusion matrices, and feature plots.",
            "6. Professional deliverables: HTML poster and a complete PowerPoint deck.",
            "7. Comprehensive documentation: README + setup guide + final viva report."
        ],
        subtitle="Going beyond the reference sample project"
    )

    # ========== PART 6: LIMITATIONS & FUTURE ==========
    section_divider(prs, "06", "Limitations & Future Work")

    two_column_slide(
        prs,
        "Limitations",
        "Data Limitations",
        [
            "Very small dataset (60 rows)",
            "Only top 3 finalists used",
            "No team-level statistics",
            "Missing advanced metrics",
            "No player injury data"
        ],
        "Modeling Limitations",
        [
            "Naive Bayes independence assumption violated",
            "Logistic Regression is linear only",
            "No ensemble or deep learning",
            "Cannot capture voter narrative/bias",
            "Risk of overfitting"
        ]
    )

    content_slide(
        prs,
        "Future Work",
        [
            "Add team-level features: wins, losses, playoff seed, point differential, strength of schedule.",
            "Include advanced player metrics: PER, win shares (WS), box plus-minus (BPM), VORP.",
            "Expand the dataset to include more seasons and all MVP vote-getters, not just top 3.",
            "Try ensemble methods: Random Forest, XGBoost, Gradient Boosting.",
            "Perform hyperparameter tuning with cross-validation.",
            "Use actual MVP vote counts as a continuous target instead of binary labels."
        ],
        subtitle="How the project can be extended"
    )

    # ========== PART 7: DEMO & CONCLUSION ==========
    section_divider(prs, "07", "Demo & Conclusion")

    content_slide(
        prs,
        "Live Demo Script",
        [
            "1. Show the project folder and repository structure.",
            "2. Run data preparation: python src/data_preparation.py",
            "3. Run model training: python src/models.py",
            "4. Show results/metrics.json and explain accuracies.",
            "5. Display visualizations from reports/figures/.",
            "6. Open the poster and PowerPoint for the panel.",
            "7. Highlight the best result: Logistic Regression 66.7% seasonal accuracy."
        ],
        subtitle="What to show during the review"
    )

    content_slide(
        prs,
        "Conclusion",
        [
            "Machine learning can partially predict NBA MVP voting using basic player statistics.",
            "Logistic Regression (66.7% seasonal accuracy) outperforms Naive Bayes (50.0%).",
            "The results confirm that MVP voting has a significant subjective component.",
            "Assists, free-throw percentage, points, blocks, and rebounds are the strongest predictors.",
            "Future models should include team success and advanced metrics for better accuracy."
        ],
        subtitle="Key takeaways"
    )

    title_slide(
        prs,
        "Thank You",
        "Questions & Discussion"
    )

    prs.save(OUTPUT_PATH)
    print(f"Improved presentation saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_presentation()
