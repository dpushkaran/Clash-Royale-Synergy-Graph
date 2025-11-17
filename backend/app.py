"""Flask API for Clash Royale Card Synergy Recommender"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from data_loader import load_cards_data, create_card_lookup
from feature_engineering import create_feature_vectors
from recommender import compute_synergy_score, generate_explanation

app = Flask(__name__)
CORS(app)

# Global variables for data and models
cards_df = None
feature_vectors = None
scaler = None
card_dict = {}


def initialize_data():
    """Load and preprocess data on startup"""
    global cards_df, feature_vectors, scaler, card_dict
    
    cards_df = load_cards_data()
    card_dict = create_card_lookup(cards_df)
    feature_vectors, scaler = create_feature_vectors(cards_df)
    
    print(f"Initialized: {len(cards_df)} cards loaded")


# Initialize on startup
initialize_data()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'cards_loaded': len(cards_df) if cards_df is not None else 0
    })


@app.route('/cards', methods=['GET'])
def get_cards():
    """Get all cards in the dataset"""
    cards_list = cards_df.to_dict('records')
    return jsonify(cards_list)


@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    """Get card recommendations based on selected cards"""
    data = request.json
    selected_cards = data.get('cards', [])
    top_n = data.get('top_n', 10)
    
    if not selected_cards:
        return jsonify({'error': 'No cards selected'}), 400
    
    # Validate selected cards exist
    valid_cards = [
        card for card in selected_cards 
        if card in cards_df['name'].values
    ]
    if not valid_cards:
        return jsonify({'error': 'No valid cards found'}), 400
    
    # Compute synergy scores for all cards (excluding selected ones)
    recommendations = []
    selected_indices = set(
        cards_df[cards_df['name'].isin(valid_cards)].index
    )
    
    for idx, row in cards_df.iterrows():
        if idx in selected_indices:
            continue
        
        score = compute_synergy_score(
            valid_cards, idx, cards_df, feature_vectors
        )
        explanation = generate_explanation(
            cards_df[cards_df['name'].isin(valid_cards)], row
        )
        
        recommendations.append({
            'name': row['name'],
            'synergy_score': float(score),
            'explanation': explanation,
            'elixirCost': int(row['elixirCost']) if pd.notna(row['elixirCost']) else None,
            'type': row['type'],
            'rarity': row['rarity'],
            'iconUrls': row['iconUrls'],
            'hitpoints': int(row['hitpoints']) if pd.notna(row['hitpoints']) else None,
            'usage': float(row['usage']) if pd.notna(row['usage']) else None
        })
    
    # Sort by synergy score and return top N
    recommendations.sort(key=lambda x: x['synergy_score'], reverse=True)
    top_recommendations = recommendations[:top_n]
    
    return jsonify({
        'selected_cards': valid_cards,
        'recommendations': top_recommendations
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)

