"""Similarity computation module using cosine similarity"""
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def compute_cosine_similarity(selected_features, candidate_features):
    """
    Compute cosine similarity between selected cards' average features
    and a candidate card's features
    """
    # Average feature vector of selected cards
    avg_selected = np.mean(selected_features, axis=0)
    
    # Compute cosine similarity
    similarity = cosine_similarity([avg_selected], [candidate_features])[0][0]
    
    return similarity

