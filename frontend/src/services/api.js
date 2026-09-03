import axios from 'axios'

const API_BASE_URL = '/api'

export const getMongoDBLogs = async (limit = 20) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/mongodb/logs`, {
      params: { limit }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching MongoDB logs:', error)
    throw error
  }
}

export const getUser01Documents = async (limit = 100) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/mongodb/user01`, {
      params: { limit }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching user01 documents:', error)
    throw error
  }
}

export const createUser01Document = async (document) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/mongodb/user01`, document)
    return response.data
  } catch (error) {
    console.error('Error creating user01 document:', error)
    throw error
  }
}

export const updateUser01Document = async (documentId, updates) => {
  try {
    const response = await axios.patch(`${API_BASE_URL}/mongodb/user01/${documentId}`, updates)
    return response.data
  } catch (error) {
    console.error('Error updating user01 document:', error)
    throw error
  }
}

export const deleteUser01Document = async (documentId) => {
  try {
    await axios.delete(`${API_BASE_URL}/mongodb/user01/${documentId}`)
    return true
  } catch (error) {
    console.error('Error deleting user01 document:', error)
    throw error
  }
}

// MySQL API calls
export const getMySQLStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/mysql/status`)
    return response.data
  } catch (error) {
    console.error('Error fetching MySQL status:', error)
    throw error
  }
}

export const getMySQLTables = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/mysql/tables`)
    return response.data
  } catch (error) {
    console.error('Error fetching MySQL tables:', error)
    throw error
  }
}

export const getMySQLTableData = async (tableName, limit = 100) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/mysql/table/${tableName}`, {
      params: { limit }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching MySQL table data:', error)
    throw error
  }
}

// PostgreSQL API calls
export const getPostgresStatus = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/postgres/status`)
    return response.data
  } catch (error) {
    console.error('Error fetching PostgreSQL status:', error)
    throw error
  }
}

export const getPostgresTables = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/postgres/tables`)
    return response.data
  } catch (error) {
    console.error('Error fetching PostgreSQL tables:', error)
    throw error
  }
}

export const getPostgresTableData = async (tableName, limit = 100) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/postgres/table/${tableName}`, {
      params: { limit }
    })
    return response.data
  } catch (error) {
    console.error('Error fetching PostgreSQL table data:', error)
    throw error
  }
}
