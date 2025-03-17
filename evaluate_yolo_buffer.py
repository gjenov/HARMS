import pandas as pd
import numpy as np
import time
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Define file paths
# Arveen Movements = Ground Truth Data
# Arveen Sheets = YOLO Fixed Bounding Box Model Output
ground_truth_path = r"C:\Users\aizha\Downloads\Performance for EEC174\Arveen Movements 2 - Sheet1.csv"
yolo_fixed_bbox_output_path = r"C:\Users\aizha\Downloads\Performance for EEC174\Arveen Sheets - Arveen2.csv"

# Load the ground truth and YOLO model output CSVs
ground_truth_df = pd.read_csv(ground_truth_path)
yolo_fixed_bbox_df = pd.read_csv(yolo_fixed_bbox_output_path)

# Ensure columns are standardized
ground_truth_df.columns = ground_truth_df.columns.str.strip()
yolo_fixed_bbox_df.columns = yolo_fixed_bbox_df.columns.str.strip()

ground_truth_df = ground_truth_df[["Time (sec)", "Action"]]
yolo_fixed_bbox_df = yolo_fixed_bbox_df[["Time (sec)", "Action"]]

# Merge ground truth and YOLO predictions with a 10-second buffer
buffer = 10
matched_predictions = []

def find_closest_match(gt_time, gt_action, pred_df, buffer):
    close_matches = pred_df[(pred_df["Time (sec)"] >= gt_time - buffer) & (pred_df["Time (sec)"] <= gt_time + buffer)]
    if not close_matches.empty:
        for _, pred_row in close_matches.iterrows():
            if pred_row["Action"] == gt_action:
                return pred_row["Time (sec)"]  # Return the matched time if found
    return None

# Iterate over ground truth and find matches
yolo_fixed_bbox_df["Matched"] = False
for _, gt_row in ground_truth_df.iterrows():
    matched_time = find_closest_match(gt_row["Time (sec)"], gt_row["Action"], yolo_fixed_bbox_df, buffer)
    if matched_time is not None:
        matched_predictions.append((gt_row["Time (sec)"], gt_row["Action"], matched_time, "Correct"))
        yolo_fixed_bbox_df.loc[yolo_fixed_bbox_df["Time (sec)"] == matched_time, "Matched"] = True
    else:
        matched_predictions.append((gt_row["Time (sec)"], gt_row["Action"], None, "Missed"))

# Find false positives (predictions with no match in ground truth)
for _, pred_row in yolo_fixed_bbox_df.iterrows():
    if not pred_row["Matched"]:
        matched_predictions.append((None, None, pred_row["Time (sec)"], "False Positive"))

# Convert results into DataFrame
comparison_df = pd.DataFrame(matched_predictions, columns=["Ground Truth Time", "Ground Truth Action", "Predicted Time", "Status"])

# Compute evaluation metrics
correct_predictions = comparison_df[comparison_df["Status"] == "Correct"].shape[0]
false_positives = comparison_df[comparison_df["Status"] == "False Positive"].shape[0]
missed_predictions = comparison_df[comparison_df["Status"] == "Missed"].shape[0]

total_ground_truth = ground_truth_df.shape[0]
total_predictions = yolo_fixed_bbox_df.shape[0]

precision = correct_predictions / (correct_predictions + false_positives) if (correct_predictions + false_positives) > 0 else 0
recall = correct_predictions / total_ground_truth if total_ground_truth > 0 else 0
f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Print evaluation results
print("Evaluation Results:")
print(f"Total Ground Truth Actions: {total_ground_truth}")
print(f"Total YOLO Predictions: {total_predictions}")
print(f"Correct Predictions (within {buffer} sec): {correct_predictions}")
print(f"False Positives: {false_positives}")
print(f"Missed Predictions: {missed_predictions}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1-score: {f1_score:.2f}")

# Display final comparison dataframe
import ace_tools as tools
tools.display_dataframe_to_user(name="Comparison of Ground Truth vs. YOLO Fixed Bounding Box Output", dataframe=comparison_df)
