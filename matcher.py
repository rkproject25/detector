import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_THRESHOLD = 0.75


def match_faces(ref_embedding, detected_embedding, threshold=DEFAULT_THRESHOLD):
    
    ref = ref_embedding.reshape(1, -1)
    det = detected_embedding.reshape(1, -1)

    score = cosine_similarity(ref, det)[0][0]
    score = float(np.clip(score, 0.0, 1.0))

    return score >= threshold, score


def match_against_database(ref_embeddings_dict, detected_embedding, threshold=DEFAULT_THRESHOLD):
    
    best_name = None
    best_score = 0.0

    for name, ref_emb in ref_embeddings_dict.items():
        is_match, score = match_faces(ref_emb, detected_embedding, threshold)
        if is_match and score > best_score:
            best_score = score
            best_name = name

    return best_name, best_score  