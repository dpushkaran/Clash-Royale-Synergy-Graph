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


@app.route('/cards', methods=['GET'])
def get_cards():
    """Get all cards in the dataset"""
    cards_list = cards_df.to_dict('records')
    return jsonify(cards_list)

