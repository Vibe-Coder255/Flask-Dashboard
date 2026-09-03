import { Link, useLocation } from 'react-router-dom'

function Sidebar() {
  const location = useLocation()

  const menuItems = [
    { path: '/', label: 'DASHBOARD', icon: '📊' },
    { path: '/analytics', label: 'ANALYTICS', icon: '📈' },
    { path: '/databases', label: 'DATABASES', icon: '🗄️' },
    { path: '/settings', label: 'SETTINGS', icon: '⚙️' }
  ]

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h3>NAVIGATION</h3>
      </div>
      <ul className="sidebar-menu">
        {menuItems.map((item) => (
          <li key={item.path} className={location.pathname === item.path ? 'active' : ''}>
            <Link to={item.path}>
              <span className="menu-icon">{item.icon}</span>
              <span className="menu-label">{item.label}</span>
            </Link>
          </li>
        ))}
      </ul>
      <div className="sidebar-footer">
        <div className="system-info">
          <div className="info-item">
            <span className="info-label">SERVER:</span>
            <span className="info-value">LOCALHOST</span>
          </div>
          <div className="info-item">
            <span className="info-label">PORT:</span>
            <span className="info-value">5000</span>
          </div>
          <div className="info-item">
            <span className="info-label">DB:</span>
            <span className="info-value">MONGODB</span>
          </div>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
