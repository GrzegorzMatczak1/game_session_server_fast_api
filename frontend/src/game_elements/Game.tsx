import { useEffect } from "react"
import { useLocation, useNavigate } from "react-router-dom"
import "./Game.css"

export default function Game() {
    const navigate = useNavigate()
    const location = useLocation()

    const username: string = location.state

    const startMatch = async () => {
        const name: {username: string} = { username }
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

        startMatch()
    }, [])

    return (
        <div className="game-container">
            {/* LEFT SIDEBAR: STATS */}
            <aside className="stats-sidebar">
            <h2>Game Stats</h2>
            <div className="stats-list">
                {/* You can easily duplicate or map over your stats here */}
                <div className="stat-item">
                <span className="stat-label">Stat Name:</span>
                <span className="stat-value">Value</span>
                </div>
                <div className="stat-item">
                <span className="stat-label">Another Stat:</span>
                <span className="stat-value">0</span>
                </div>
            </div>
            </aside>

            {/* MAIN CONTENT AREA */}
            <main className="main-content">
            {/* GAME PLAY AREA */}
            <div className="round-wrapper">
                {/* <Round /> component will live here safely */}
                <div className="round-placeholder">
                <h3>[Round Content Area]</h3>
                <p>Your Round.tsx component will render here and expand to fill the space.</p>
                </div>
            </div>

            {/* BOTTOM ACTION BUTTONS */}
            <footer className="action-bar">
                <button className="action-btn primary">Action 1</button>
                <button className="action-btn">Action 2</button>
                <button className="action-btn">Action 3</button>
                {/* Add as many buttons as your gameplay needs */}
            </footer>
            </main>
        </div>
    )
}