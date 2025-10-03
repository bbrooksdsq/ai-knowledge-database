'use client'

import { useState, useEffect } from 'react'
import { Users, Calendar, Clock, CheckCircle, AlertCircle, Settings, RefreshCw } from 'lucide-react'
import { Button } from './ui/button'

interface TeamsStatus {
  configured: boolean
  authenticated: boolean
  message: string
  tenant_id?: string
  required_variables?: string[]
}

interface SyncResult {
  status: string
  message: string
  recordings_found?: number
  stored_count?: number
  documents?: Array<{
    id: number
    title: string
    created_at: string
    summary?: string
  }>
}

export default function TeamsIntegration() {
  const [status, setStatus] = useState<TeamsStatus | null>(null)
  const [syncing, setSyncing] = useState(false)
  const [syncResult, setSyncResult] = useState<SyncResult | null>(null)
  const [daysBack, setDaysBack] = useState(7)
  const [testingConnection, setTestingConnection] = useState(false)

  useEffect(() => {
    checkTeamsStatus()
  }, [])

  const checkTeamsStatus = async () => {
    try {
      const response = await fetch('/api/v1/teams/status')
      const data = await response.json()
      setStatus(data)
    } catch (error) {
      console.error('Failed to check Teams status:', error)
    }
  }

  const testConnection = async () => {
    setTestingConnection(true)
    try {
      const response = await fetch('/api/v1/teams/test-connection')
      const data = await response.json()
      
      if (data.status === 'success') {
        alert('✅ Microsoft Teams connection successful!')
      } else {
        alert(`❌ Connection failed: ${data.message}`)
      }
    } catch (error) {
      alert('❌ Could not test Teams connection')
    } finally {
      setTestingConnection(false)
    }
  }

  const syncRecordings = async () => {
    setSyncing(true)
    setSyncResult(null)
    
    try {
      const response = await fetch('/api/v1/teams/sync-and-store', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ days_back: daysBack }),
      })
      
      const data = await response.json()
      setSyncResult(data)
      
      if (data.status === 'success') {
        // Refresh status after successful sync
        checkTeamsStatus()
      }
    } catch (error) {
      setSyncResult({
        status: 'error',
        message: 'Failed to sync Teams recordings'
      })
    } finally {
      setSyncing(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Microsoft Teams Integration</h2>
            <p className="text-gray-600">
              Automatically sync and transcribe your Teams meeting recordings
            </p>
          </div>
          <div className="flex space-x-2">
            <Button 
              onClick={testConnection} 
              disabled={testingConnection}
              variant="outline"
              className="flex items-center space-x-2"
            >
              <RefreshCw className={`w-4 h-4 ${testingConnection ? 'animate-spin' : ''}`} />
              <span>Test Connection</span>
            </Button>
            <Button 
              onClick={checkTeamsStatus} 
              variant="outline"
              className="flex items-center space-x-2"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Refresh Status</span>
            </Button>
          </div>
        </div>
      </div>

      {/* Status Card */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
          <Settings className="w-5 h-5" />
          <span>Integration Status</span>
        </h3>
        
        {status ? (
          <div className="space-y-4">
            <div className="flex items-center space-x-3">
              {status.configured ? (
                <CheckCircle className="w-6 h-6 text-green-600" />
              ) : (
                <AlertCircle className="w-6 h-6 text-red-600" />
              )}
              <div>
                <p className={`font-medium ${status.configured ? 'text-green-900' : 'text-red-900'}`}>
                  {status.configured ? 'Configured' : 'Not Configured'}
                </p>
                <p className="text-sm text-gray-600">{status.message}</p>
              </div>
            </div>
            
            {status.authenticated !== undefined && (
              <div className="flex items-center space-x-3">
                {status.authenticated ? (
                  <CheckCircle className="w-6 h-6 text-green-600" />
                ) : (
                  <AlertCircle className="w-6 h-6 text-yellow-600" />
                )}
                <div>
                  <p className={`font-medium ${status.authenticated ? 'text-green-900' : 'text-yellow-900'}`}>
                    {status.authenticated ? 'Authenticated' : 'Authentication Required'}
                  </p>
                </div>
              </div>
            )}
            
            {status.tenant_id && (
              <div className="text-sm text-gray-600">
                <strong>Tenant ID:</strong> {status.tenant_id}
              </div>
            )}
            
            {status.required_variables && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h4 className="font-medium text-yellow-900 mb-2">Required Environment Variables:</h4>
                <ul className="space-y-1 text-sm text-yellow-800">
                  {status.required_variables.map((variable, index) => (
                    <li key={index} className="font-mono">• {variable}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-4">
            <RefreshCw className="w-6 h-6 text-gray-400 mx-auto animate-spin" />
            <p className="text-gray-500 mt-2">Checking status...</p>
          </div>
        )}
      </div>

      {/* Sync Controls */}
      {status?.configured && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Sync Teams Recordings</h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sync recordings from the last:
              </label>
              <select
                value={daysBack}
                onChange={(e) => setDaysBack(Number(e.target.value))}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value={1}>1 day</option>
                <option value={3}>3 days</option>
                <option value={7}>7 days</option>
                <option value={14}>14 days</option>
                <option value={30}>30 days</option>
              </select>
            </div>
            
            <Button
              onClick={syncRecordings}
              disabled={syncing || !status.configured}
              className="w-full"
            >
              {syncing ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  Syncing Recordings...
                </>
              ) : (
                <>
                  <Users className="w-4 h-4 mr-2" />
                  Sync Teams Recordings
                </>
              )}
            </Button>
          </div>
        </div>
      )}

      {/* Sync Results */}
      {syncResult && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center space-x-2">
            {syncResult.status === 'success' ? (
              <CheckCircle className="w-5 h-5 text-green-600" />
            ) : (
              <AlertCircle className="w-5 h-5 text-red-600" />
            )}
            <span>Sync Results</span>
          </h3>
          
          <div className={`p-4 rounded-lg ${
            syncResult.status === 'success' 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-red-50 border border-red-200'
          }`}>
            <p className={`font-medium ${
              syncResult.status === 'success' ? 'text-green-900' : 'text-red-900'
            }`}>
              {syncResult.message}
            </p>
            
            {syncResult.recordings_found !== undefined && (
              <p className="text-sm text-gray-600 mt-1">
                Found {syncResult.recordings_found} recordings
              </p>
            )}
            
            {syncResult.stored_count !== undefined && (
              <p className="text-sm text-gray-600 mt-1">
                Stored {syncResult.stored_count} documents in knowledge base
              </p>
            )}
          </div>
          
          {/* Document List */}
          {syncResult.documents && syncResult.documents.length > 0 && (
            <div className="mt-6">
              <h4 className="font-medium text-gray-900 mb-3">Processed Documents:</h4>
              <div className="space-y-3">
                {syncResult.documents.map((doc) => (
                  <div key={doc.id} className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg">
                    <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Calendar className="w-4 h-4 text-blue-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <h5 className="font-medium text-gray-900 truncate">{doc.title}</h5>
                      <div className="flex items-center space-x-4 text-sm text-gray-500 mt-1">
                        <span className="flex items-center space-x-1">
                          <Clock className="w-3 h-3" />
                          <span>{formatDate(doc.created_at)}</span>
                        </span>
                        <span>ID: {doc.id}</span>
                      </div>
                      {doc.summary && (
                        <p className="text-sm text-gray-600 mt-2">{doc.summary}</p>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Setup Instructions */}
      {!status?.configured && (
        <div className="bg-blue-50 rounded-lg p-6">
          <h3 className="font-semibold text-blue-900 mb-3">Setup Microsoft Teams Integration</h3>
          <div className="space-y-3 text-sm text-blue-800">
            <p><strong>1. Create Azure App Registration:</strong></p>
            <ul className="ml-4 space-y-1">
              <li>• Go to Azure Portal → App registrations → New registration</li>
              <li>• Name: "AI Knowledge Base Teams Integration"</li>
              <li>• Account types: "Accounts in this organizational directory only"</li>
              <li>• Redirect URI: Leave blank for now</li>
            </ul>
            
            <p><strong>2. Configure API Permissions:</strong></p>
            <ul className="ml-4 space-y-1">
              <li>• Add permissions → Microsoft Graph → Application permissions</li>
              <li>• Add: CallRecords.Read.All, Calls.Read.All</li>
              <li>• Grant admin consent</li>
            </ul>
            
            <p><strong>3. Create Client Secret:</strong></p>
            <ul className="ml-4 space-y-1">
              <li>• Certificates & secrets → New client secret</li>
              <li>• Copy the secret value (you won't see it again)</li>
            </ul>
            
            <p><strong>4. Set Environment Variables:</strong></p>
            <ul className="ml-4 space-y-1">
              <li>• TEAMS_CLIENT_ID: Application (client) ID from overview</li>
              <li>• TEAMS_CLIENT_SECRET: The secret you created</li>
              <li>• TEAMS_TENANT_ID: Directory (tenant) ID from overview</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}
