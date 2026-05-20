import { useEffect, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import "./Game.css"
import Round from "./Round"

interface Player {
    playerId: number,
    username: string,
    maxHp: number,
    currentHp: number,
    atk: number,
    mana: number
}

interface Enemy {
    enemyId: number,
    name: string,
    maxHp: number,
    currentHp: number,
    atk: number
}

export default function Game() {
    const navigate = useNavigate()
    const location = useLocation()

    const username: string = location.state

    const [willAttack, setWillAttack] = useState<boolean>(false)

    const [player, setPlayer] = useState<Player>({
        playerId: 0,
        username: "skibidi",
        maxHp: 0,
        currentHp: 0,
        atk: 0,
        mana: 0
    })

    const [enemy, setEnemy] = useState<Enemy>(
        { enemyId: 1, name: "Zenek", maxHp: 50, currentHp: 50, atk: 12 }
    )

    const getPlayerData = async () => {
        await fetch('http://localhost:8000/player/get')
        .then(res => res.json())
        .then(data => setPlayer(data));

        console.log(player)
    }

    const startMatch = async () => {
        const name: { username: string } = { username }
        try {
            const responce = await fetch("http://localhost:8000/match/start", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(name)
            })

            if (!responce.ok) {
                console.error("Responce error")
                return
            }

            const data = responce.json()
            console.log(data)

        
        } catch (err) {
            console.log(err)
        }
    }

    useEffect(() => {
        if (!username) navigate("/home")

        getPlayerData()
    }, [])

    return (
        <div className="game-container">
            {/* LEFT SIDEBAR: STATS */}
            <aside className="stats-sidebar">
                <h2>Game Stats</h2>
                <hr className="sidebar-divider" />
                
                <div className="round-display">
                    Round: <span className="round-value">{1}</span>
                </div>

                <h3>Player Stats</h3>
                <div className="stats-list">
                    {/* You can easily duplicate, add more, or map over these elements */}
                    <div className="stat-item">
                        <span className="stat-label">Health:</span>
                        <span className="stat-value">{/*CURRENT HP*/ 20}/{/*MAX HP*/20}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Attack:</span>
                        <span className="stat-value">8</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Mana:</span>
                        <span className="stat-value">25</span>
                    </div>
                </div>
            </aside>

            {/* MAIN CONTENT AREA */}
            <main className="main-content">
                {/* GAME PLAY AREA */}
                <div className="round-wrapper">
                    {/* <Round /> component will live here safely */}
                    <div className="round-placeholder">
                        <Round enemy={enemy} willAttack={willAttack} setWillAttack={setWillAttack} />
                    </div>
                </div>

                {/* BOTTOM ACTION BUTTONS */}
                <footer className="action-bar">
                    <button className="action-btn">
                        <span>Health{"(2)"}</span>
                        <svg viewBox="0 0 24 24" className="btn-icon" fill="currentColor">
                            <path d="M12 7l-7 7h14z" />
                        </svg>
                    </button>
                    <button className="action-btn">
                        <span>Attack{"(3)"}</span>
                        <svg viewBox="0 0 24 24" className="btn-icon" fill="currentColor">
                            <path d="M12 7l-7 7h14z" />
                        </svg>
                    </button>
                    <button className="action-btn important">Next Turn</button>
                    {/* Add as many buttons as your gameplay needs */}
                </footer>
            </main>
        </div>
    )
}