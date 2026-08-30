import { useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:8000'

const DEMO_MESSAGE =
  'I was charged twice for my subscription and need help getting one charge refunded.'

function App() {
  const [message, setMessage] = useState(DEMO_MESSAGE)
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    setError('')
    setResponse(null)
    setLoading(true)

    try {
      const res = await fetch(`${API_URL}/support/handle`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data.detail || 'Support request failed.')
      }

      setResponse(data)
    } catch (err) {
      setError(
        err.message || 'Unable to connect to the support service.',
      )
    } finally {
      setLoading(false)
    }
  }

  const categoryLabel = response?.category
    ? response.category.toUpperCase()
    : ''

  return (
    <main className="app">
      <header className="header">
        <div className="eyebrow">
          <span className="status-dot" />
          MULTI-AGENT CUSTOMER SUPPORT
        </div>

        <div className="header-content">
          <div>
            <h1>
              Support that
              <br />
              knows where to go.
            </h1>

            <p className="subtitle">
              An AI support system that routes every request
              to the right specialist agent.
            </p>
          </div>

          <div className="header-meta">
            <span>AI-POWERED</span>
            <span>MULTI-AGENT</span>
            <span>STRUCTURED OUTPUT</span>
          </div>
        </div>
      </header>

      <section className="workspace">
        <div className="input-panel">
          <div className="section-label">
            <span>01</span>
            CUSTOMER REQUEST
          </div>

          <div className="panel-heading">
            <h2>How can we help?</h2>
            <p>
              Describe the issue and the routing agent will
              determine the right specialist.
            </p>
          </div>

          <textarea
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="Describe your support issue..."
            aria-label="Customer support message"
          />

          <div className="input-footer">
            <span className="character-count">
              {message.length} characters
            </span>

            <button
              type="button"
              onClick={handleSubmit}
              disabled={loading || !message.trim()}
            >
              {loading ? 'Routing...' : 'Get support'}
              <span className="arrow">→</span>
            </button>
          </div>

          {error && (
            <div className="error-message">
              <strong>Request failed</strong>
              <span>{error}</span>
            </div>
          )}
        </div>

        <div className="output-panel">
          <div className="section-label">
            <span>02</span>
            AI RESPONSE
          </div>

          <div className="panel-heading">
            <h2>Support intelligence</h2>
            <p>
              {response
                ? 'The request was routed and handled by a specialist agent.'
                : 'The routed response will appear here.'}
            </p>
          </div>

          {!response && !loading && (
            <div className="empty-state">
              <div className="empty-mark">AI</div>
              <p>
                Submit a customer request to see the routing
                decision and specialist response.
              </p>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="loader" />
              <p>Routing request to the right agent...</p>
            </div>
          )}

          {response && !loading && (
            <div className="results">
              <section className="result-section routing-section">
                <div className="result-header">
                  <div className="result-label">
                    ROUTING DECISION
                  </div>

                  <span className="category-badge">
                    {categoryLabel}
                  </span>
                </div>

                <div className="routing-card">
                  <div className="routing-agent">
                    <span className="routing-icon">AI</span>

                    <div>
                      <span className="meta-label">
                        SPECIALIST AGENT
                      </span>
                      <strong>
                        {response.agent}
                      </strong>
                    </div>
                  </div>

                  <div className="routing-reason">
                    <span className="meta-label">
                      WHY THIS AGENT
                    </span>
                    <p>
                      {response.routing_reason}
                    </p>
                  </div>
                </div>
              </section>

              <section className="result-section">
                <div className="result-header">
                  <div className="result-label">
                    SUPPORT RESPONSE
                  </div>

                  <span
                    className={
                      response.resolved
                        ? 'status-badge resolved'
                        : 'status-badge escalated'
                    }
                  >
                    {response.resolved
                      ? 'RESOLVED'
                      : 'ESCALATED'}
                  </span>
                </div>

                <div className="response-card">
                  <p>{response.message}</p>
                </div>

                {response.escalated &&
                  response.escalation_reason && (
                    <div className="escalation-card">
                      <span className="meta-label">
                        ESCALATION REASON
                      </span>
                      <p>
                        {response.escalation_reason}
                      </p>
                    </div>
                  )}
              </section>
            </div>
          )}
        </div>
      </section>

      <footer className="footer">
        <span>MULTI-AGENT CUSTOMER SUPPORT</span>
        <span>FASTAPI · REACT · LLM</span>
      </footer>
    </main>
  )
}

export default App
