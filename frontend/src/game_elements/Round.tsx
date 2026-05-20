import "./Round.css"
import img from "./visuals/example-enemy.png"

// Reusing your Enemy interface structure for strict typing
interface Enemy {
    enemyId: number
    name: string
    maxHp: number
    currentHp: number
    atk: number
}

interface RoundProps {
    enemy: Enemy
    willAttack: boolean
    setWillAttack: (value: boolean) => void
}

export default function Round({ enemy, willAttack, setWillAttack }: RoundProps) {

    return (
        <div className="round-container">
            {/* CENTER MAIN CONTENT: IMAGE & INTERACTION */}
            <div className="round-center-content">
                <div className="enemy-image-wrapper">
                    {/* Placeholder container for the enemy graphic */}
                    <div className="enemy-image-placeholder">
                        <img src={img} />
                    </div>
                </div>

                {/* Turn Strategy Toggle */}
                <div className="attack-control-panel">
                    <label className="toggle-layout">
                        <input 
                            type="checkbox" 
                            className="toggle-input"
                            checked={willAttack}
                            onChange={(e) => setWillAttack(e.target.checked)}
                        />
                        <span className="toggle-label-text">Attack this turn</span>
                    </label>
                </div>
            </div>

            {/* RIGHT SIDEBAR: ENEMY STATS */}
            <aside className="enemy-sidebar">
                <h2>Enemy Info</h2>
                <hr className="sidebar-divider" />
                
                <div className="enemy-name-display">
                    {enemy.name || "Unknown Foe"}
                </div>

                {/* Reusing your structural list classes from Game.css */}
                <div className="stats-list">
                    <div className="stat-item">
                        <span className="stat-label">Health:</span>
                        <span className="stat-value">{enemy.currentHp}/{enemy.maxHp}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Attack:</span>
                        <span className="stat-value">{enemy.atk}</span>
                    </div>
                </div>
            </aside>
        </div>
    )
}