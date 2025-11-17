"""Recommendation algorithm with gap analysis for deck synergy"""
import pandas as pd
import numpy as np
from similarity import compute_cosine_similarity


def compute_gap_bonus(selected_df, candidate_row):
    """
    Compute bonus score for cards that fill missing roles in the deck
    Returns a value between 0 and 1
    """
    bonus = 0.0
    
    # Check what roles are already covered
    has_air_defense = (
        selected_df['targets'].isin(['air', 'both']).any() and 
        selected_df['type'].isin(['troop', 'building']).any()
    )
    has_splash = selected_df['attack_type'].isin(['splash']).any()
    has_tank = (
        (selected_df['hitpoints'] > 2000).any() or 
        selected_df['type'].eq('building').any()
    )
    has_building = selected_df['type'].eq('building').any()
    has_cheap_cycle = (selected_df['elixirCost'] <= 2).any()
    has_spell = selected_df['type'].eq('spell').any()
    has_flying = selected_df['mobility'].eq('flying').any()
    
    # Reward filling gaps
    if not has_air_defense and candidate_row['targets'] in ['air', 'both']:
        bonus += 0.3
    if not has_splash and candidate_row['attack_type'] == 'splash':
        bonus += 0.2
    if not has_tank and (
        candidate_row['hitpoints'] > 2000 or candidate_row['type'] == 'building'
    ):
        bonus += 0.2
    if not has_building and candidate_row['type'] == 'building':
        bonus += 0.15
    if not has_cheap_cycle and candidate_row['elixirCost'] <= 2:
        bonus += 0.15
    if not has_spell and candidate_row['type'] == 'spell':
        bonus += 0.1
    if not has_flying and candidate_row['mobility'] == 'flying':
        bonus += 0.1
    
    return min(bonus, 1.0)


def generate_explanation(selected_df, candidate_row):
    """Generate human-readable explanation for why a card synergizes"""
    explanations = []
    
    # Check gaps and explain
    has_air_defense = (
        selected_df['targets'].isin(['air', 'both']).any() and 
        selected_df['type'].isin(['troop', 'building']).any()
    )
    has_splash = selected_df['attack_type'].isin(['splash']).any()
    has_tank = (
        (selected_df['hitpoints'] > 2000).any() or 
        selected_df['type'].eq('building').any()
    )
    has_building = selected_df['type'].eq('building').any()
    has_cheap_cycle = (selected_df['elixirCost'] <= 2).any()
    has_spell = selected_df['type'].eq('spell').any()
    has_flying = selected_df['mobility'].eq('flying').any()
    
    if not has_air_defense and candidate_row['targets'] in ['air', 'both']:
        explanations.append("covers air defense")
    if not has_splash and candidate_row['attack_type'] == 'splash':
        explanations.append("provides splash damage")
    if not has_tank and (
        candidate_row['hitpoints'] > 2000 or candidate_row['type'] == 'building'
    ):
        explanations.append("adds tank/building support")
    if not has_building and candidate_row['type'] == 'building':
        explanations.append("adds building defense")
    if not has_cheap_cycle and candidate_row['elixirCost'] <= 2:
        explanations.append("cheap cycle support")
    if not has_spell and candidate_row['type'] == 'spell':
        explanations.append("adds spell utility")
    if not has_flying and candidate_row['mobility'] == 'flying':
        explanations.append("adds flying unit")
    
    if not explanations:
        explanations.append("complements deck composition")
    
    return ", ".join(explanations)


def compute_synergy_score(selected_cards, candidate_idx, cards_df, feature_vectors):
    """
    Compute overall synergy score combining similarity and gap analysis
    """
    if len(selected_cards) == 0:
        return 0.0
    
    # Get feature vectors for selected cards
    selected_indices = [
        cards_df[cards_df['name'] == name].index[0] 
        for name in selected_cards
    ]
    selected_features = feature_vectors[selected_indices]
    
    # Candidate card feature vector
    candidate_features = feature_vectors[candidate_idx]
    
    # Compute cosine similarity
    similarity = compute_cosine_similarity(selected_features, candidate_features)
    
    # Identify gaps in the deck
    selected_df = cards_df[cards_df['name'].isin(selected_cards)]
    candidate_row = cards_df.iloc[candidate_idx]
    gap_bonus = compute_gap_bonus(selected_df, candidate_row)
    
    # Combine similarity with gap bonus (weighted)
    synergy_score = (similarity * 0.6) + (gap_bonus * 0.4)
    
    return synergy_score

