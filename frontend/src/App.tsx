import { useEffect, useState } from 'react';
import './App.css'; // Assuming you port your styles here

// Define the structure of the expected API response
interface HealthResponse {
  status: string;
  message: string;
}

function App() {
  const [data, setData] = useState<HealthResponse | null>(null);
  const [connected, setConnected] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Call the FastAPI health endpoint
    fetch('http://localhost:8000/api/health')
      .then((res) => {
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        return res.json();
      })
      .then((jsonData: HealthResponse) => {
        setData(jsonData);
        setConnected(jsonData && jsonData.status === 'ok');
        setLoading(false);
      })
      .catch((error) => {
        console.error('Fetch error:', error);
        setConnected(false);
        setLoading(false);
      });
  }, []);

  return (
    <div className="app-container">
      <h1>Browser Game</h1>

      {loading ? (
        <div className="status loading">Checking backend status...</div>
      ) : (
        <div className={`status ${connected ? 'ok' : 'fail'}`}>
          {connected && data ? (
            <>✅ Backend connected — {data.message}</>
          ) : (
            <>❌ Backend not reachable — is FastAPI running on port 8000?</>
          )}
        </div>
      )}
    </div>
  );
}

export default App;