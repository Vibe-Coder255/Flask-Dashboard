import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

function Login() {
  const [credentials, setCredentials] = useState({ username: '', password: '' })
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    // Simple authentication - in production, this would call an API
    if (credentials.username && credentials.password) {
      navigate('/')
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1 className="terminal-title">BLOOMBERG TERMINAL</h1>
        <h2>LOGIN</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>USERNAME</label>
            <input
              type="text"
              value={credentials.username}
              onChange={(e) => setCredentials({...credentials, username: e.target.value})}
              className="terminal-input"
            />
          </div>
          <div className="form-group">
            <label>PASSWORD</label>
            <input
              type="password"
              value={credentials.password}
              onChange={(e) => setCredentials({...credentials, password: e.target.value})}
              className="terminal-input"
            />
          </div>
          <button type="submit" className="terminal-btn">LOGIN</button>
        </form>
      </div>
    </div>
  )
}

export default Login
