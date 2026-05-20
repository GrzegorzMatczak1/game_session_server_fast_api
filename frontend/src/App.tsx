import { Navigate, Route, Routes, BrowserRouter as Router } from 'react-router-dom'
import './index.css'
import Home from './home_elements/Home';
import Game from './game_elements/Game';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/home" replace />} />
        <Route path="/home" element={<Home />} />
        <Route path='/game' element={<Game />} />
      </Routes>
    </Router>
  );
}

export default App