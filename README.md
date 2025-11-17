# ⚔️ Clash Royale Card Synergy Recommender

A web application that recommends synergistic Clash Royale cards based on feature engineering and similarity metrics. Select your core cards (win conditions or deck foundation) and discover complementary cards that fill missing roles in your deck.

## 🎯 Features

- **Feature Engineering**: Converts card attributes (type, mobility, targets, attack type, rarity, elixir cost, hitpoints, usage rate) into numeric feature vectors using one-hot encoding and normalization
- **Synergy Scoring**: Combines cosine similarity with gap analysis to identify cards that complement your selection
- **Gap Analysis**: Identifies missing roles (air defense, splash damage, tanks, buildings, cheap cycle, spells, flying units) and prioritizes cards that fill them
- **Interactive UI**: Modern React interface with card search, filtering, and visual recommendations
- **REST API**: Flask backend with endpoints for fetching cards and getting recommendations

## 🏗️ Architecture

### Backend (Python/Flask)
- **Data Loading** (`data_loader.py`): Loads and preprocesses the card dataset
- **Feature Engineering** (`feature_engineering.py`): Creates numeric feature vectors from card attributes
- **Similarity Computation** (`similarity.py`): Computes cosine similarity between cards
- **Recommendation Algorithm** (`recommender.py`): Combines similarity with gap analysis for synergy scoring
- **API** (`app.py`): Flask REST API with CORS support

### Frontend (React/Vite)
- **Card Component**: Displays individual card information with icons
- **CardSelector Component**: Multi-select interface with search and type filtering
- **Recommendations Component**: Displays ranked recommendations with synergy scores and explanations
- **App Component**: Main application with API integration and state management

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

Or use the helper script:
```bash
./run.sh
```

The API will be available at `http://localhost:5001`

**Note:** Port 5000 is often used by macOS AirPlay Receiver, so we use port 5001 instead.

**Verify the backend is running:**
- Visit `http://localhost:5001/health` in your browser - you should see `{"status":"healthy","cards_loaded":120}`
- Or check the terminal for: `Initialized: 120 cards loaded`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173` (or the port Vite assigns)

## 📡 API Endpoints

### GET /cards
Returns all cards in the dataset.

**Response:**
```json
[
  {
    "name": "Archer Queen",
    "elixirCost": 5,
    "iconUrls": "https://...",
    "type": "troop",
    "rarity": "champion",
    ...
  }
]
```

### POST /recommendations
Get card recommendations based on selected cards.

**Request Body:**
```json
{
  "cards": ["Hog Rider", "Fireball"],
  "top_n": 10
}
```

**Response:**
```json
{
  "selected_cards": ["Hog Rider", "Fireball"],
  "recommendations": [
    {
      "name": "Ice Spirit",
      "synergy_score": 0.85,
      "explanation": "cheap cycle support, adds spell utility",
      "elixirCost": 1,
      "type": "troop",
      ...
    }
  ]
}
```

## 🧮 Algorithm Details

The recommendation algorithm uses a two-part scoring system:

1. **Similarity Score (60% weight)**: Cosine similarity between the average feature vector of selected cards and candidate cards
2. **Gap Bonus (40% weight)**: Rewards cards that fill missing roles:
   - Air defense (targets air/both)
   - Splash damage
   - Tank/building support
   - Building defense
   - Cheap cycle cards (≤2 elixir)
   - Spell utility
   - Flying units

The final synergy score combines both metrics to provide balanced recommendations.

## 📊 Dataset

The project uses `clash_royale_cards.csv` which includes:
- Card name, rarity, elixir cost
- Type (troop/spell/building)
- Mobility (ground/flying)
- Targets (ground/air/both/buildings)
- Attack type (single/splash)
- Hitpoints, usage rate
- Icon URLs

## 🛠️ Technologies Used

- **Backend**: Python, Flask, pandas, NumPy, scikit-learn
- **Frontend**: React, Vite, CSS3
- **Data Processing**: Feature engineering, similarity metrics, gap analysis

## 📝 Project Structure

```
.
├── backend/
│   ├── app.py                 # Flask API
│   ├── data_loader.py         # Data loading
│   ├── feature_engineering.py # Feature vector creation
│   ├── similarity.py          # Similarity computation
│   ├── recommender.py         # Recommendation algorithm
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Card.jsx
│   │   │   ├── CardSelector.jsx
│   │   │   └── Recommendations.jsx
│   │   ├── App.jsx
│   │   └── App.css
│   └── package.json
├── clash_royale_cards.csv     # Dataset
└── README.md
```

## 🎨 Features Showcase

- **Multi-select card selection** with visual feedback
- **Search and filter** cards by name and type
- **Ranked recommendations** with synergy scores and explanations
- **Responsive design** with modern gradient UI
- **Real-time updates** as you select/deselect cards

## 🤝 Contributing

This project was built to showcase:
- Feature engineering and data preprocessing
- Similarity-based recommendation systems
- REST API design and implementation
- Modern React frontend development
- Game strategy-focused UX design

## 🔧 Troubleshooting

### "Failed to fetch" Error

If you see "Failed to fetch" or "Cannot connect to backend server" in the frontend:

**Note:** On macOS, port 5000 is often used by AirPlay Receiver. The app uses port 5001 to avoid conflicts.

1. **Check if backend is running:**
   ```bash
   # In the backend directory
   python app.py
   ```
   You should see: `Running on http://127.0.0.1:5001`

2. **Verify backend is accessible:**
   - Open `http://localhost:5001/health` in your browser
   - You should see: `{"status":"healthy","cards_loaded":120}`

3. **Check for port conflicts:**
   - Make sure nothing else is using port 5001
   - If needed, change the port in `backend/app.py` (line 109)

4. **CORS issues:**
   - The backend has CORS enabled, but if you still have issues, check that `flask-cors` is installed

5. **Check browser console:**
   - Open browser DevTools (F12) and check the Console tab for detailed error messages

### Backend Won't Start

- Make sure all dependencies are installed: `pip3 install -r requirements.txt`
- Check Python version: `python3 --version` (should be 3.8+)
- Verify the CSV file exists: `ls ../clash_royale_cards.csv`

### Frontend Issues

- Clear browser cache and hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Check that `npm install` completed successfully
- Verify Vite is running on the expected port (usually 5173)

## 📄 License

This project is for educational and portfolio purposes.

