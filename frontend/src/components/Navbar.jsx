import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <span className="brand-icon">⬡</span>
        <span className="brand-text">FLASK DASHBOARD</span>
      </div>
      <div className="navbar-links">
        <Link to="/" className="nav-link">DASHBOARD</Link>
        <Link to="/analytics" className="nav-link">ANALYTICS</Link>
        <Link to="/login" className="nav-link">LOGIN</Link>
      </div>
      <div className="navbar-status">
        <span className="status-indicator online"></span>
        <span className="status-text">SYSTEM ONLINE</span>
      </div>
    </nav>
  )
}

export default Navbar
