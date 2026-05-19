import { Navigate, Route, Routes, BrowserRouter as Router } from 'react-router-dom'
import './index.css'
import Home from './home_elements/Home';

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