import { useState } from 'react'
import './Home.css'
import Status from './Status'
import { useNavigate } from 'react-router-dom'

function Home() {
  const [username, setUsername] = useState('')
  const navigate = useNavigate()

  const handleSubmit = () => {
    if (!username.trim()) return
  
    navigate("/game", { state: {username: username} })
    console.log('Username submitted:', username)
  }

  return (
    <div className="home-wrapper">
      <div className="home-card">

        <div>
          <h1 className="home-card__title">Welcome</h1>
          <h4 className="home-card__subtitle">Enter a username to continue</h4>
        </div>

        <div className="home-form">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            placeholder="enter username…"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
            autoComplete="off"
            autoFocus
          />
        </div>

        <button
          className="home-btn-submit"
          onClick={handleSubmit}
          disabled={!username.trim()}
        >
          Enter
        </button>
      </div>

      <Status />
    </div>
  )
}

export default Home