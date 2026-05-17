import { Navigate, Route, Routes, BrowserRouter as Router } from 'react-router-dom'
import Home from './Home'
import './index.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/home" replace />} />
        <Route path="/home" element={<Home />} />
      </Routes>
    </Router>
  );
}

export default App