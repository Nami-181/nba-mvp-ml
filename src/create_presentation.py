"""
Generate a PowerPoint presentation for the NBA MVP prediction project.
"""

import os
import json
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor


RESULTS_DIR = "results"
FIGURES_DIR = "reports/figures"
OUTPUT_PATH = "reports/presentation/NBA_MVP_Prediction.pptx"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)


def add_title_slide(prs, title, subtitle):
    slide_layout = prs.slide_layouts[0]  # Title Slide
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = title
    slide.placeholders[1].text = subtitle
    return slide


def add_section_slide(prs, title, bullets):
    slide_layout = prs.slide_layouts[1]  # Title and Content
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = title
    tf = slide.placeholders[1].text_frame
    tf.clear()
    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = bullet
        p.level = 0
        p.font.size = Pt(20)
    return slide


def add_two_content_slide(prs, title, left_title, left_bullets, right_title, right_bullets):
    slide_layout = prs.slide_layouts[5]  # Blank
    slide = prs.slides.add_slide(slide_layout)

    # Title
    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    title_shape.text_frame.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(32)
    title_shape.text_frame.paragraphs[0].font.bold = True

    # Left column
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(4.3), Inches(6))
    tf = left_box.text_frame
    tf.text = left_title
    tf.paragraphs[0].font.size = Pt(24)
    tf.paragraphs[0].font.bold = True
    for bullet in left_bullets:
        p = tf.add_paragraph()
        p.text = bullet
        p.level = 0
        p.font.size = Pt(18)

    # Right column
    right_box = slide.shapes.add_textbox(Inches(5.0), Inches(1.3), Inches(4.3), Inches(6))
    tf = right_box.text_frame
    tf.text = right_title
    tf.paragraphs[0].font.size = Pt(24)
    tf.paragraphs[0].font.bold = True
    for bullet in right_bullets:
        p = tf.add_paragraph()
        p.text = bullet
        p.level = 0
        p.font.size = Pt(18)

    return slide


def add_image_slide(prs, title, image_path, left_text=None):
    slide_layout = prs.slide_layouts[5]  # Blank
    slide = prs.slides.add_slide(slide_layout)

    title_shape = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    title_shape.text_frame.text = title
    title_shape.text_frame.paragraphs[0].font.size = Pt(32)
    title_shape.text_frame.paragraphs[0].font.bold = True

    if left_text:
        text_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.3), Inches(3.0), Inches(6))
        tf = text_box.text_frame
        for i, line in enumerate(left_text):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(16)
        slide.shapes.add_picture(image_path, Inches(3.8), Inches(1.3), width=Inches(5.5))
    else:
        slide.shapes.add_picture(image_path, Inches(1.0), Inches(1.2), width=Inches(8.0))

    return slide


def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # Load metrics
    with open(os.path.join(RESULTS_DIR, "metrics.json")) as f:
        metrics = json.load(f)

    nb_test_seasonal = metrics["naive_bayes"]["test_accuracy_seasonal"]
    lr_test_seasonal = metrics["logistic_regression"]["test_accuracy_seasonal"]

    # 1. Title slide
    add_title_slide(
        prs,
        "Predicting the NBA MVP with Machine Learning",
        "A comparison of Naive Bayes and Logistic Regression\n\nUE24CS352A — Machine Learning Mini Project"
    )

    # 2. Motivation
    add_section_slide(
        prs,
        "Motivation & Problem Statement",
        [
            "The NBA MVP is voted by sportswriters and broadcasters.",
            "Human voters are influenced by popularity, media narratives, and recency bias.",
            "Can machine learning predict the MVP using only objective player statistics?",
            "We compare a generative model (Naive Bayes) with a discriminative model (Logistic Regression)."
        ]
    )

    # 3. Dataset
    add_section_slide(
        prs,
        "Dataset",
        [
            "Source: Kaggle dataset scraped from Basketball-Reference",
            "Timeframe: 2000-01 to 2019-20 (20 seasons)",
            "Rows: 60 (top 3 MVP finalists per season)",
            "Train: 2000-01 to 2015-16 → 48 rows",
            "Test: 2016-17 to 2019-20 → 12 rows",
            "Target: MVP = 1 for the winner, 0 for the runners-up"
        ]
    )

    # 4. Features
    add_section_slide(
        prs,
        "Features Used",
        [
            "Games played (g)",
            "Minutes per game (mp_per_g)",
            "Field goal percentage (fg_pct)",
            "3-point percentage (fg3_pct)",
            "Free throw percentage (ft_pct)",
            "Rebounds per game (trb_per_g)",
            "Assists per game (ast_per_g)",
            "Steals per game (stl_per_g)",
            "Blocks per game (blk_per_g)",
            "Points per game (pts_per_g)"
        ]
    )

    # 5. Methodology
    add_two_content_slide(
        prs,
        "Methodology",
        "Naive Bayes",
        [
            "Generative probabilistic classifier",
            "Assumes features are independent",
            "Fast and works well on small data",
            "No feature scaling needed"
        ],
        "Logistic Regression",
        [
            "Discriminative linear classifier",
            "Learns a direct decision boundary",
            "Outputs class probabilities",
            "Features standardized before training"
        ]
    )

    # 6. Evaluation modes
    add_two_content_slide(
        prs,
        "Evaluation Modes",
        "Pure MVP Prediction",
        [
            "Binary classification task",
            "Each finalist independently classified as MVP or not",
            "Threshold on predicted probability: 0.5"
        ],
        "Seasonal MVP Prediction",
        [
            "One MVP must be chosen per season",
            "Select the finalist with highest probability in that season",
            "Closer to real-world voting"
        ]
    )

    # 7. Results table
    add_section_slide(
        prs,
        "Results",
        [
            f"Naive Bayes — Train (pure): 60.4%, Test (pure): 41.7%, Test (seasonal): {nb_test_seasonal:.1%}",
            f"Logistic Regression — Train (pure): 79.2%, Test (pure): 50.0%, Test (seasonal): {lr_test_seasonal:.1%}",
            "Logistic Regression performs best in seasonal mode.",
            "Small dataset and high voter subjectivity limit accuracy."
        ]
    )

    # 8. Accuracy comparison figure
    add_image_slide(
        prs,
        "Accuracy Comparison",
        os.path.join(FIGURES_DIR, "accuracy_comparison.png"),
        left_text=[
            "Logistic Regression generalizes better in seasonal mode.",
            "Naive Bayes struggles with correlated features.",
            "Both models show a train-test gap, indicating limited data."
        ]
    )

    # 9. Confusion matrices
    add_image_slide(
        prs,
        "Confusion Matrices (Pure Mode)",
        os.path.join(FIGURES_DIR, "confusion_matrices.png")
    )

    # 10. Feature importance
    add_image_slide(
        prs,
        "Feature Importance — Logistic Regression",
        os.path.join(FIGURES_DIR, "feature_importance.png"),
        left_text=[
            "Top positive predictors:",
            "• Assists per game",
            "• Free throw %",
            "• Points per game",
            "• Blocks per game",
            "• Rebounds per game",
            "",
            "Negative:",
            "• Minutes per game"
        ]
    )

    # 11. Discussion
    add_section_slide(
        prs,
        "Discussion",
        [
            "Logistic Regression outperforms Naive Bayes, especially for seasonal prediction.",
            "Naive Bayes' independence assumption is violated by correlated basketball stats.",
            "The dataset is very small (60 rows), leading to overfitting.",
            "Models miss non-statistical factors: team wins, media narrative, voter bias.",
            "Results are comparable to the reference sample project."
        ]
    )

    # 12. Future work
    add_section_slide(
        prs,
        "Conclusion & Future Work",
        [
            "ML can partially predict MVP voting, but human bias remains a major factor.",
            "Future improvements:",
            "  • Add team-level features (wins, playoff seed, point differential)",
            "  • Include advanced metrics (PER, win shares, VORP)",
            "  • Expand dataset to more seasons",
            "  • Try ensemble models (Random Forest, XGBoost)"
        ]
    )

    # 13. Thank you
    add_title_slide(
        prs,
        "Thank You",
        "Questions?"
    )

    prs.save(OUTPUT_PATH)
    print(f"Presentation saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    create_presentation()
