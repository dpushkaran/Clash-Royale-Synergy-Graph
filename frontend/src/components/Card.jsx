import './Card.css'

function Card({ card, onClick, isSelected = false, showDetails = false }) {
  const handleClick = () => {
    if (onClick) {
      onClick(card.name)
    }
  }

  return (
    <div
      className={`card ${isSelected ? 'selected' : ''}`}
      onClick={handleClick}
    >
      <img src={card.iconUrls} alt={card.name} className="card-image" />
      <div className="card-info">
        <h3 className="card-name">{card.name}</h3>
        {showDetails && (
          <div className="card-details">
            <span className="card-elixir">⚡ {card.elixirCost || 'N/A'}</span>
            <span className="card-type">{card.type}</span>
            {card.synergy_score !== undefined && (
              <span className="card-score">
                Synergy: {(card.synergy_score * 100).toFixed(1)}%
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Card

