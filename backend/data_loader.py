"""Data loading and preprocessing module for Clash Royale cards"""
import pandas as pd
import os


def load_cards_data():
    """Load the Clash Royale cards dataset from CSV"""
    csv_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'clash_royale_cards.csv'
    )
    
    df = pd.read_csv(csv_path)
    
    # Fill missing values
    df['hitpoints'] = df['hitpoints'].fillna(0)
    df['usage'] = df['usage'].fillna(0)
    df['elixirCost'] = df['elixirCost'].fillna(0)
    
    return df


def create_card_lookup(df):
    """Create a dictionary for quick card lookup by name"""
    return {row['name']: row.to_dict() for _, row in df.iterrows()}

