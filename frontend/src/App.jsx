import { useState, useEffect } from 'react'
import './App.css'
import CardSelector from './components/CardSelector'
import Recommendations from './components/Recommendations'

const API_BASE_URL = 'http://localhost:5000'

function App() {
  const [cards, setCards] = useState([])
  const [selectedCards, setSelectedCards] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchCards()
  }, [])

  const fetchCards = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/cards`)
      if (!response.ok) {
        throw new Error(`Backend returned error: ${response.status} ${response.statusText}`)
      }
      const data = await response.json()
      setCards(data)
      setError(null)
    } catch (err) {
      const errorMessage = err.message.includes('fetch') 
        ? 'Cannot connect to backend server. Make sure the backend is running on http://localhost:5000'
        : err.message
      setError(errorMessage)
      console.error('Error fetching cards:', err)
    }
  }

  const handleCardSelection = (cardNames) => {
    setSelectedCards(cardNames)
  }

  const handleGetRecommendations = async () => {
    if (selectedCards.length === 0) {
      setError('Please select at least one card')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE_URL}/recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          cards: selectedCards,
          top_n: 12,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error || `Backend returned error: ${response.status}`)
      }
      const data = await response.json()
      setRecommendations(data.recommendations || [])
      setError(null)
    } catch (err) {
      const errorMessage = err.message.includes('fetch') 
        ? 'Cannot connect to backend server. Make sure the backend is running on http://localhost:5000'
        : err.message
      setError(errorMessage)
      console.error('Error fetching recommendations:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleClearSelection = () => {
    setSelectedCards([])
    setRecommendations([])
    setError(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>⚔️ Clash Royale Card Synergy Recommender</h1>
        <p>Select your core cards and discover synergistic combinations</p>
      </header>

      <main className="app-main">
        <div className="selector-section">
          <CardSelector
            cards={cards}
            selectedCards={selectedCards}
            onSelectionChange={handleCardSelection}
          />
          
          <div className="action-buttons">
            <button
              onClick={handleGetRecommendations}
              disabled={selectedCards.length === 0 || loading}
              className="btn-primary"
            >
              {loading ? 'Finding Synergies...' : 'Get Recommendations'}
            </button>
            <button
              onClick={handleClearSelection}
              disabled={selectedCards.length === 0}
              className="btn-secondary"
            >
              Clear Selection
            </button>
          </div>

          {error && <div className="error-message">{error}</div>}
        </div>

        {selectedCards.length > 0 && (
          <div className="selected-cards-section">
            <h2>Selected Cards ({selectedCards.length})</h2>
            <div className="selected-cards-grid">
              {selectedCards.map((cardName) => {
                const card = cards.find((c) => c.name === cardName)
                return card ? (
                  <div key={cardName} className="selected-card">
                    <img src={card.iconUrls} alt={card.name} />
                    <span>{card.name}</span>
                  </div>
                ) : null
              })}
            </div>
          </div>
        )}

        {recommendations.length > 0 && (
          <Recommendations recommendations={recommendations} />
        )}
      </main>
    </div>
  )
}

export default App
