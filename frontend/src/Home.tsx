import { useState } from 'react'
import './Home.css'
import Status from './Status'

function Home() {
  const [username, setUsername] = useState('')

  const handleSubmit = () => {
    if (!username.trim()) return
    // TODO: handle login / navigation
    console.log('Username submitted:', username)
  }

  return (
    <div className="home-wrapper">
      <div className="home-card">
        <span className="home-card__eyebrow">Browser Game</span>

        <div>
          <h1 className="home-card__title">Welcome</h1>
          <h4 className="home-card__subtitle">Sign in to continue</h4>
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