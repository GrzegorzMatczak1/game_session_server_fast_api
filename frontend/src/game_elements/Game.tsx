import { useEffect, useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import "./Game.css"
import Round from "./Round"

interface Player {
    player_id: number,
    username: string,
    player_base_hp: number,
    Player_current_hp: number,
    player_attack: number,
    mana: number
}

interface Enemy {
    enemy_id: number;
    enemy_name: string;
    enemy_base_hp: number;
    enemy_current_hp: number;
    enemy_attack: number;
}

export default function Game() {
    const navigate = useNavigate()
    const location = useLocation()

    const username: string = location.state?.username ?? location.state
    const [isAlive, setIsAlive] = useState<boolean>(true)
    const [showGameOver, setShowGameOver] = useState(false)
    const [isCodeBuffering, setIsCodeBuffering] = useState(false)
    const [currentRound, setCurrentRound] = useState<number>(1)

    const [willAttack, setWillAttack] = useState<boolean>(false)

    const [player, setPlayer] = useState<Player>({
        player_id: 0,
        username: "skibidi",
        player_base_hp: 0,
        Player_current_hp: 0,
        player_attack: 0,
        mana: 0
    })

    const [enemy, setEnemy] = useState<Enemy>({
        "enemy_id": 1,
        "enemy_name": "Larp Larp Sahur",
        "enemy_base_hp": 10,
        "enemy_current_hp": 10,
        "enemy_attack": 3
    })

    const getPlayerData = async () => {
        const res = await fetch('http://localhost:8000/player/get')
        const data: Player = await res.json()
        setPlayer(data)
        if (data.Player_current_hp <= 0) {
            setIsAlive(false)
        }
    }

    const getEnemyData = async () => {
        const res = await fetch('http://localhost:8000/enemy/get')
        const data: Enemy = await res.json()
        setEnemy(data)
    }

    const getCurrentRound = async () => {
        const response = await fetch("http://localhost:8000/round/get")
        const data: number = await response.json()
        setCurrentRound(data)
    }

    const startMatch = async () => {
        try {
            const response = await fetch(`http://localhost:8000/match/start?logged_username=${encodeURIComponent(username)}`, {
                method: "POST"
            })

            if (!response.ok) {
                console.error("Responce error")
                return
            }

            const data = await response.json()

            getEnemyData()
            setPlayer(data)

        } catch (err) {
            console.log(err)
        }
    }

    const handleUpgradeHealth = async () => {
        if (!(player.mana < 2)) {
            try {
                const response = await fetch(`http://localhost:8000/player/upgrade?stat_index=${1}`,
                    { method: "POST" }
                )

                if (!response.ok) {
                    console.error("Responce error")
                    return
                }

                getPlayerData()
            } catch (error) {
                console.error("Upgrade error:", error);
                return false;
            }
        }
    }

    const handleUpgradeAttack = async () => {
        if (!(player.mana < 3)) {
            try {
                const response = await fetch(`http://localhost:8000/player/upgrade?stat_index=${2}`,
                    { method: "POST" }
                )

                if (!response.ok) {
                    console.error("Responce error")
                    return
                }

                getPlayerData()
            } catch (error) {
                console.error("Upgrade error:", error);
                return false;
            }
        }
    }

    const handleNextTurn = async () => {
        setIsCodeBuffering(true)
        const response = await fetch(`http://localhost:8000/turn/progres?player_attacked=${Boolean(willAttack)}`, { method: "POST" })
        const hasEnded: boolean = await response.json()
        
        await getPlayerData()
        await getEnemyData()
        await getCurrentRound()

        setIsCodeBuffering(false)
        if (hasEnded) {
            setIsAlive(false) // this triggers showGameOver via useEffect
        }
    }

    useEffect(() => {
        if (!username) {
            navigate("/home")
            return
        }

        console.log(username)

        const init = async () => {
            await startMatch()
            await getPlayerData()
            await getEnemyData()
            await getCurrentRound()
        }

        init()
    }, [])

    useEffect(() => {
        if (!isAlive) {
            setShowGameOver(true)
        }
    }, [isAlive])

    useEffect(() => {
        console.log(willAttack)
    }, [willAttack])

    return (
        <div className="game-container">
            {/* LEFT SIDEBAR: STATS */}
            <aside className="stats-sidebar">
                <h2>Game Stats</h2>
                <hr className="sidebar-divider" />

                <div className="round-display">
                    Round: <span className="round-value">{currentRound}</span>
                </div>

                <h3>Player Stats</h3>
                <div className="stats-list">
                    <h3>{username}</h3>
                    <div className="stat-item">
                        <span className="stat-label">Health:</span>
                        <span className="stat-value">{player.Player_current_hp}/{player.player_base_hp}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Attack:</span>
                        <span className="stat-value">{player.player_attack}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Mana:</span>
                        <span className="stat-value">{player.mana}</span>
                    </div>

                </div>
            </aside>

            {/* MAIN CONTENT AREA */}
            <main className="main-content">
                {/* GAME PLAY AREA */}
                <div className="round-wrapper">
                    <div className="round-placeholder">
                        <Round enemy={enemy} willAttack={willAttack} setWillAttack={setWillAttack} />
                    </div>
                </div>

                {/* BOTTOM ACTION BUTTONS */}
                <footer className="action-bar">
                    <button className="action-btn" onClick={handleUpgradeHealth} disabled={player.mana < 2}>
                        <span>Health{"(2)"}</span>
                        <svg viewBox="0 0 24 24" className="btn-icon" fill="currentColor">
                            <path d="M12 7l-7 7h14z" />
                        </svg>
                    </button>
                    <button className="action-btn" onClick={handleUpgradeAttack} disabled={player.mana < 3}>
                        <span>Attack{"(3)"}</span>
                        <svg viewBox="0 0 24 24" className="btn-icon" fill="currentColor">
                            <path d="M12 7l-7 7h14z" />
                        </svg>
                    </button>
                    <button className="action-btn important" onClick={handleNextTurn}>Next Turn</button>
                </footer>
            </main>

            {showGameOver && (
                <div style={{
                    position: 'fixed',
                    inset: 0,
                    backgroundColor: 'rgba(0, 0, 0, 0.75)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    zIndex: 9999,
                }}>
                    <div style={{
                        background: '#1a1a2e',
                        border: '2px solid #e24b4a',
                        borderRadius: '12px',
                        padding: '2rem 2.5rem',
                        textAlign: 'center',
                        minWidth: '260px',
                    }}>
                        <h2 style={{ color: '#f09595', marginBottom: '0.5rem' }}>Game Over</h2>
                        <p style={{ color: '#888', marginBottom: '1.5rem', fontSize: '14px' }}>
                            Better luck next time!
                        </p>
                        <button
                            onClick={() => navigate('/home')}
                            style={{
                                padding: '0.6rem 1.5rem',
                                background: '#e24b4a',
                                color: '#fff',
                                border: 'none',
                                borderRadius: '8px',
                                fontSize: '15px',
                                cursor: 'pointer',
                            }}
                        >
                            Return to Home
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}