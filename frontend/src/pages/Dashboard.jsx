import { useState, useEffect } from 'react'
import StatCard from '../components/StatCard'
import { getMongoDBLogs, getUser01Documents } from '../services/api'

function formatDocumentId(id) {
  if (typeof id === 'string') return id
  if (id && typeof id.$oid === 'string') return id.$oid
  return String(id ?? '')
}

function Dashboard() {
  const [logs, setLogs] = useState([])
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCollection, setSelectedCollection] = useState('user01')
  const [autoRefresh, setAutoRefresh] = useState(true)

  useEffect(() => {
    fetchData()
    let interval
    if (autoRefresh) {
      interval = setInterval(fetchData, 5000) // Refresh every 5 seconds
    }
    return () => clearInterval(interval)
  }, [autoRefresh, selectedCollection])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [logsData, docsData] = await Promise.all([
        getMongoDBLogs(20),
        getUser01Documents(100)
      ])
      setLogs(logsData)
      setDocuments(docsData)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const stats = [
    { title: 'MongoDB Status', value: 'CONNECTED', color: '#00ff00' },
    { title: 'Total Documents', value: documents.length, color: '#ff9500' },
    { title: 'Connection Logs', value: logs.length, color: '#00d4ff' },
    { title: 'Auto Refresh', value: autoRefresh ? 'ON' : 'OFF', color: autoRefresh ? '#00ff00' : '#ff0000' }
  ]

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1 className="terminal-title">DATABASE MONITOR</h1>
        <div className="timestamp">{new Date().toLocaleString()}</div>
      </div>

      <div className="stats-grid">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} />
        ))}
      </div>

      <div className="dashboard-grid">
        <div className="panel panel-logs">
          <div className="panel-header">
            <h3>CONNECTION LOGS</h3>
            <button onClick={fetchData} className="refresh-btn">REFRESH</button>
          </div>
          <div className="panel-content">
            {loading ? (
              <div className="loading">Loading...</div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>TIME</th>
                    <th>STATUS</th>
                    <th>DATABASE</th>
                    <th>COMMAND</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log, index) => (
                    <tr key={index} className={log.status === 'success' ? 'row-success' : 'row-error'}>
                      <td>{new Date(log.checked_at).toLocaleTimeString()}</td>
                      <td>{log.status.toUpperCase()}</td>
                      <td>{log.request.database}</td>
                      <td>{log.request.command}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        <div className="panel panel-documents">
          <div className="panel-header">
            <h3>USER_01 COLLECTION</h3>
            <div className="panel-controls">
              <button 
                onClick={() => setAutoRefresh(!autoRefresh)}
                className={`toggle-btn ${autoRefresh ? 'active' : ''}`}
              >
                AUTO: {autoRefresh ? 'ON' : 'OFF'}
              </button>
            </div>
          </div>
          <div className="panel-content">
            {loading ? (
              <div className="loading">Loading...</div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>DATA PREVIEW</th>
                    <th>ACTIONS</th>
                  </tr>
                </thead>
                <tbody>
                  {documents.slice(0, 15).map((doc, index) => (
                    <tr key={index}>
                      <td className="cell-id">{formatDocumentId(doc._id).substring(0, 8)}...</td>
                      <td className="cell-preview">
                        {JSON.stringify(doc, null, 2).substring(0, 100)}...
                      </td>
                      <td className="cell-actions">
                        <button className="action-btn">VIEW</button>
                        <button className="action-btn">EDIT</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
