"""Feature engineering module for creating numeric feature vectors from card attributes"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def create_feature_vectors(df):
    """
    Create numeric feature vectors for each card using one-hot encoding
    and normalized numeric features
    """
    # One-hot encode categorical features
    type_encoded = pd.get_dummies(df['type'], prefix='type')
    mobility_encoded = pd.get_dummies(df['mobility'], prefix='mobility')
    targets_encoded = pd.get_dummies(df['targets'], prefix='targets')
    attack_type_encoded = pd.get_dummies(df['attack_type'], prefix='attack_type')
    rarity_encoded = pd.get_dummies(df['rarity'], prefix='rarity')
    
    # Boolean features
    group_card = df['groupCard'].astype(int).values.reshape(-1, 1)
    
    # Normalize numeric features
    scaler = StandardScaler()
    numeric_features = df[['elixirCost', 'hitpoints', 'usage']].fillna(0)
    numeric_normalized = scaler.fit_transform(numeric_features)
    
    # Combine all features
    feature_matrix = np.hstack([
        type_encoded.values,
        mobility_encoded.values,
        targets_encoded.values,
        attack_type_encoded.values,
        rarity_encoded.values,
        group_card,
        numeric_normalized
    ])
    
    return feature_matrix, scaler

