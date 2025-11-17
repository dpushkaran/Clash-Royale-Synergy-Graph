import Card from './Card'
import './Recommendations.css'

function Recommendations({ recommendations }) {
  if (!recommendations || recommendations.length === 0) {
    return null
  }

  return (
    <div className="recommendations">
      <div className="recommendations-header">
        <h2>Recommended Synergies</h2>
        <p>Top cards that complement your selection</p>
      </div>

      <div className="recommendations-grid">
        {recommendations.map((card, index) => (
          <div key={card.name} className="recommendation-item">
            <div className="recommendation-rank">#{index + 1}</div>
            <Card card={card} showDetails={true} />
            <div className="recommendation-explanation">
              {card.explanation}
            </div>
            <div className="recommendation-stats">
              <span>⚡ {card.elixirCost || 'N/A'}</span>
              <span className="synergy-badge">
                {(card.synergy_score * 100).toFixed(1)}% match
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Recommendations

