import { useState } from 'react'
import Card from './Card'
import './CardSelector.css'

function CardSelector({ cards, selectedCards, onSelectionChange }) {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterType, setFilterType] = useState('all')

  const handleCardClick = (cardName) => {
    const newSelection = selectedCards.includes(cardName)
      ? selectedCards.filter(name => name !== cardName)
      : [...selectedCards, cardName]
    onSelectionChange(newSelection)
  }

  const filteredCards = cards.filter(card => {
    const matchesSearch = card.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesType = filterType === 'all' || card.type === filterType
    return matchesSearch && matchesType
  })

  const uniqueTypes = ['all', ...new Set(cards.map(card => card.type))]

  return (
    <div className="card-selector">
      <div className="selector-header">
        <h2>Select Your Core Cards</h2>
        <p>Choose one or more cards to find synergistic combinations</p>
      </div>

      <div className="selector-filters">
        <input
          type="text"
          placeholder="Search cards..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="type-filter"
        >
          {uniqueTypes.map(type => (
            <option key={type} value={type}>
              {type === 'all' ? 'All Types' : type.charAt(0).toUpperCase() + type.slice(1)}
            </option>
          ))}
        </select>
      </div>

      <div className="cards-grid">
        {filteredCards.map(card => (
          <Card
            key={card.name}
            card={card}
            onClick={handleCardClick}
            isSelected={selectedCards.includes(card.name)}
          />
        ))}
      </div>

      {filteredCards.length === 0 && (
        <div className="no-results">No cards found matching your search.</div>
      )}
    </div>
  )
}

export default CardSelector

