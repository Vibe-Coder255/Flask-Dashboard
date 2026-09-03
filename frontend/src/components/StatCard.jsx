function StatCard({ title, value, color }) {
  return (
    <div className="stat-card">
      <div className="stat-header">
        <span className="stat-title">{title}</span>
        <div className="stat-indicator" style={{ backgroundColor: color }}></div>
      </div>
      <div className="stat-value" style={{ color }}>
        {value}
      </div>
    </div>
  )
}

export default StatCard
