import "./Round.css"
import img1 from "./visuals/somalijczyk.png"
import img2 from "./visuals/wsciekla-kula.png"
import img3 from "./visuals/slime-w-bloku.png"
import img4 from "./visuals/czad.png"
import { useEffect, useState } from "react"


// Reusing your Enemy interface structure for strict typing
interface Enemy {
  enemy_id: number;
  enemy_name: string;
  enemy_base_hp: number;
  enemy_current_hp: number;
  enemy_attack: number;
}

interface RoundProps {
    enemy: Enemy
    willAttack: boolean
    setWillAttack: (value: boolean) => void
}

export default function Round({ enemy, willAttack, setWillAttack }: RoundProps) {

    const [enemyImg, setEnemyImg] = useState<string>(img1)

    useEffect(() => {
        if (enemy.enemy_id === 1) {
        setEnemyImg(img1)
        } else if (enemy.enemy_id === 2) {
        setEnemyImg(img2)
        } else if (enemy.enemy_id === 3) {
        setEnemyImg(img3)
        } else if (enemy.enemy_id === 4) {
        setEnemyImg(img4)
        } else {
        setEnemyImg("")
        }
    }, [enemy.enemy_id])

    return (
        <div className="round-container">
            {/* CENTER MAIN CONTENT: IMAGE & INTERACTION */}
            <div className="round-center-content">
                <div className="enemy-image-wrapper">
                    {/* Placeholder container for the enemy graphic */}
                    <div className="enemy-image-placeholder">
                        <img src={enemyImg} />
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
                    {enemy.enemy_name || "Unknown Foe"}
                </div>

                {/* Reusing your structural list classes from Game.css */}
                <div className="stats-list">
                    <div className="stat-item">
                        <span className="stat-label">Health:</span>
                        <span className="stat-value">{enemy.enemy_current_hp}/{enemy.enemy_base_hp}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Attack:</span>
                        <span className="stat-value">{enemy.enemy_attack}</span>
                    </div>
                    <p>{"(every 5 turns enemy attacks)"}</p>
                </div>
            </aside>
        </div>
    )
}