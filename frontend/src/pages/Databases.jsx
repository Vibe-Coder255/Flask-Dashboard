import { useState, useEffect } from 'react'
import { 
  getMongoDBLogs, 
  getUser01Documents,
  getMySQLStatus, 
  getMySQLTables, 
  getMySQLTableData,
  getPostgresStatus,
  getPostgresTables,
  getPostgresTableData
} from '../services/api'

function Databases() {
  const [activeDatabase, setActiveDatabase] = useState('mongodb')
  const [dbStatus, setDbStatus] = useState({})
  const [tables, setTables] = useState([])
  const [tableData, setTableData] = useState([])
  const [selectedTable, setSelectedTable] = useState(null)
  const [loading, setLoading] = useState(false)

  const databases = [
    { id: 'mongodb', name: 'MongoDB', icon: '🍃' },
    { id: 'mysql', name: 'MySQL', icon: '🐬' },
    { id: 'postgres', name: 'PostgreSQL', icon: '🐘' }
  ]

  useEffect(() => {
    fetchDatabaseStatus()
  }, [activeDatabase])

  useEffect(() => {
    if (activeDatabase !== 'mongodb') {
      fetchTables()
    }
  }, [activeDatabase])

  const fetchDatabaseStatus = async () => {
    setLoading(true)
    try {
      let status
      if (activeDatabase === 'mongodb') {
        const logs = await getMongoDBLogs(1)
        status = { 
          status: logs[0]?.status || 'unknown',
          database: 'flask_db',
          host: 'localhost',
          port: 27017
        }
      } else if (activeDatabase === 'mysql') {
        status = await getMySQLStatus()
      } else if (activeDatabase === 'postgres') {
        status = await getPostgresStatus()
      }
      setDbStatus(status)
    } catch (error) {
      console.error('Error fetching database status:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchTables = async () => {
    setLoading(true)
    try {
      let tablesData
      if (activeDatabase === 'mysql') {
        tablesData = await getMySQLTables()
      } else if (activeDatabase === 'postgres') {
        tablesData = await getPostgresTables()
      }
      setTables(tablesData || [])
    } catch (error) {
      console.error('Error fetching tables:', error)
      setTables([])
    } finally {
      setLoading(false)
    }
  }

  const fetchTableData = async (tableName) => {
    setLoading(true)
    setSelectedTable(tableName)
    try {
      let data
      if (activeDatabase === 'mysql') {
        data = await getMySQLTableData(tableName, 100)
      } else if (activeDatabase === 'postgres') {
        data = await getPostgresTableData(tableName, 100)
      }
      setTableData(data || [])
    } catch (error) {
      console.error('Error fetching table data:', error)
      setTableData([])
    } finally {
      setLoading(false)
    }
  }

  const fetchMongoDBData = async () => {
    setLoading(true)
    try {
      const data = await getUser01Documents(100)
      setTableData(data)
      setSelectedTable('user_01')
    } catch (error) {
      console.error('Error fetching MongoDB data:', error)
      setTableData([])
    } finally {
      setLoading(false)
    }
  }

  const renderTableHeaders = () => {
    if (tableData.length === 0) return null
    const headers = Object.keys(tableData[0] || {})
    return headers.map(header => (
      <th key={header}>{header.toUpperCase()}</th>
    ))
  }

  const renderTableRows = () => {
    if (tableData.length === 0) return null
    return tableData.map((row, index) => (
      <tr key={index}>
        {Object.values(row).map((value, cellIndex) => (
          <td key={cellIndex}>
            {typeof value === 'object' ? JSON.stringify(value).substring(0, 50) + '...' : String(value).substring(0, 50)}
          </td>
        ))}
      </tr>
    ))
  }

  return (
    <div className="databases">
      <div className="dashboard-header">
        <h1 className="terminal-title">DATABASE MANAGEMENT</h1>
        <div className="timestamp">{new Date().toLocaleString()}</div>
      </div>

      <div className="database-selector">
        {databases.map(db => (
          <button
            key={db.id}
            className={`db-btn ${activeDatabase === db.id ? 'active' : ''}`}
            onClick={() => {
              setActiveDatabase(db.id)
              setSelectedTable(null)
              setTableData([])
            }}
          >
            <span className="db-icon">{db.icon}</span>
            <span className="db-name">{db.name}</span>
          </button>
        ))}
      </div>

      <div className="dashboard-grid">
        <div className="panel panel-status">
          <div className="panel-header">
            <h3>CONNECTION STATUS</h3>
          </div>
          <div className="panel-content">
            {loading ? (
              <div className="loading">Loading...</div>
            ) : (
              <div className="status-info">
                <div className="status-item">
                  <span className="status-label">STATUS:</span>
                  <span className={`status-value ${dbStatus.status === 'success' ? 'success' : 'error'}`}>
                    {dbStatus.status?.toUpperCase() || 'UNKNOWN'}
                  </span>
                </div>
                <div className="status-item">
                  <span className="status-label">DATABASE:</span>
                  <span className="status-value">{dbStatus.database || 'N/A'}</span>
                </div>
                <div className="status-item">
                  <span className="status-label">HOST:</span>
                  <span className="status-value">{dbStatus.host || 'N/A'}</span>
                </div>
                <div className="status-item">
                  <span className="status-label">PORT:</span>
                  <span className="status-value">{dbStatus.port || 'N/A'}</span>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="panel panel-tables">
          <div className="panel-header">
            <h3>TABLES / COLLECTIONS</h3>
          </div>
          <div className="panel-content">
            {loading ? (
              <div className="loading">Loading...</div>
            ) : activeDatabase === 'mongodb' ? (
              <div className="mongodb-collections">
                <button 
                  className="collection-btn"
                  onClick={fetchMongoDBData}
                >
                  user_01
                </button>
              </div>
            ) : tables.length > 0 ? (
              <ul className="table-list">
                {tables.map((table, index) => (
                  <li key={index}>
                    <button 
                      className="table-btn"
                      onClick={() => fetchTableData(table.name)}
                    >
                      {table.name}
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="no-data">No tables found</div>
            )}
          </div>
        </div>

        <div className="panel panel-data">
          <div className="panel-header">
            <h3>DATA VIEWER - {selectedTable || 'SELECT TABLE'}</h3>
            <button 
              onClick={() => selectedTable && (activeDatabase === 'mongodb' ? fetchMongoDBData() : fetchTableData(selectedTable))}
              className="refresh-btn"
            >
              REFRESH
            </button>
          </div>
          <div className="panel-content">
            {loading ? (
              <div className="loading">Loading...</div>
            ) : tableData.length > 0 ? (
              <table className="data-table">
                <thead>
                  <tr>
                    {renderTableHeaders()}
                  </tr>
                </thead>
                <tbody>
                  {renderTableRows()}
                </tbody>
              </table>
            ) : (
              <div className="no-data">Select a table to view data</div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Databases
