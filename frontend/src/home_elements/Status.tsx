import { useState, useCallback } from 'react'

interface HealthResponse {
  status: string
  message: string
}

type CheckState = 'idle' | 'loading' | 'ok' | 'fail'

export default function Status() {
  const [checkState, setCheckState] = useState<CheckState>('idle')
  const [message, setMessage] = useState<string>('')
  const [open, setOpen] = useState(false)

  const check = useCallback(async () => {
    setCheckState('loading')
    setOpen(true)
    try {
      const res = await fetch('http://localhost:8000/api/health')
      if (!res.ok) throw new Error('Non-OK response')
      const data: HealthResponse = await res.json()
      const isOk = data?.status === 'ok'
      setCheckState(isOk ? 'ok' : 'fail')
      setMessage(isOk ? data.message : 'Unexpected response from server.')
    } catch {
      setCheckState('fail')
      setMessage('Backend not reachable — is FastAPI running on port 8000?')
    }
  }, [])

  const handleClick = () => {
    if (open && checkState !== 'loading') {
      // Re-check on subsequent clicks
      check()
    } else if (!open) {
      check()
    }
  }

  const btnClass = `status-btn ${checkState === 'ok' ? 'ok' : checkState === 'fail' ? 'fail' : ''}`

  const tooltipClass = `status-tooltip ${checkState === 'ok' ? 'ok' : checkState === 'fail' ? 'fail' : ''}`

  const tooltipText =
    checkState === 'loading' ? 'Checking…' :
    checkState === 'ok'      ? `✓ ${message}` :
    checkState === 'fail'    ? `✗ ${message}` :
    ''

  return (
    <>
      {open && checkState !== 'idle' && (
        <div className={tooltipClass}>{tooltipText}</div>
      )}
      <button className={btnClass} onClick={handleClick} title="Check backend status">
        <span className="status-dot" />
        {checkState === 'loading' ? 'Checking…' : 'Server Status'}
      </button>
    </>
  )
}