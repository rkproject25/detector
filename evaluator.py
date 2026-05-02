import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from detector import encode_reference_image
from matcher import match_faces
import time

def evaluate_on_image_pairs(test_pairs, threshold=0.75):
    y_true, y_pred, scores = [], [], []
    for pair in test_pairs:
        try:
            ref_emb = encode_reference_image(pair['ref_path'])
            test_emb = encode_reference_image(pair['test_path'])
            is_match, score = match_faces(ref_emb, test_emb, threshold)
            y_true.append(pair['label'])
            y_pred.append(1 if is_match else 0)
            scores.append(score)
        except ValueError:
            continue
    if not y_true:
        return {}
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0,1]).ravel()
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    accuracy = np.mean(y_true == y_pred)
    far = fp / (fp + tn) if (fp+tn)>0 else 0.0
    frr = fn / (fn + tp) if (fn+tp)>0 else 0.0
    metrics = {
        "threshold": threshold,
        "total_pairs": len(y_true),
        "accuracy": round(accuracy,4),
        "precision": round(precision,4),
        "recall": round(recall,4),
        "f1_score": round(f1,4),
        "false_accept_rate_FAR": round(far,4),
        "false_reject_rate_FRR": round(frr,4),
        "true_positives": int(tp),
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "avg_score_same_person": round(np.mean([scores[i] for i in range(len(y_true)) if y_true[i]==1]),4) if any(y_true==1) else 0,
        "avg_score_diff_person": round(np.mean([scores[i] for i in range(len(y_true)) if y_true[i]==0]),4) if any(y_true==0) else 0,
        "avg_processing_time_ms": 0.0
    }
    return metrics