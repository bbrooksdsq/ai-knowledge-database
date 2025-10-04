'use client'

import { useState, useEffect } from 'react'
import { Clock, FileText, Tag, Search } from 'lucide-react'

interface Document {
  id: number
  title: string
  content: string
  file_type: string
  tags: string[]
  created_at: string
  summary?: string
}

export default function RecentDocuments() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchRecentDocuments()
  }, [])

  const fetchRecentDocuments = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://ai-knowledge-database-production.up.railway.app'
      const response = await fetch(`${apiUrl}/api/v1/documents/?limit=20`)
      if (response.ok) {
        const data = await response.json()
        setDocuments(data)
      }
    } catch (error) {
      console.error('Failed to fetch recent documents:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))
    
    if (diffInHours < 24) {
      return `${diffInHours} hours ago`
    } else if (diffInHours < 168) {
      const days = Math.floor(diffInHours / 24)
      return `${days} days ago`
    } else {
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      })
    }
  }

  const getFileTypeIcon = (fileType: string) => {
    switch (fileType.toLowerCase()) {
      case 'pdf':
        return '📄'
      case 'docx':
      case 'doc':
        return '📝'
      case 'txt':
        return '📃'
      case 'audio':
        return '🎵'
      case 'video':
        return '🎥'
      default:
        return '📄'
    }
  }

  const truncateText = (text: string, maxLength: number = 200) => {
    if (text.length <= maxLength) return text
    return text.substring(0, maxLength) + '...'
  }

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow-sm border p-6 animate-pulse">
            <div className="flex items-start space-x-4">
              <div className="w-12 h-12 bg-gray-200 rounded-lg" />
              <div className="flex-1 space-y-3">
                <div className="h-4 bg-gray-200 rounded w-3/4" />
                <div className="h-3 bg-gray-200 rounded w-1/2" />
                <div className="space-y-2">
                  <div className="h-3 bg-gray-200 rounded" />
                  <div className="h-3 bg-gray-200 rounded w-5/6" />
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Recent Documents</h2>
            <p className="text-gray-600">
              Latest additions to your knowledge base
            </p>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <Clock className="w-4 h-4" />
            <span>Last updated: {new Date().toLocaleDateString()}</span>
          </div>
        </div>
      </div>

      {/* Documents List */}
      {documents.length > 0 ? (
        <div className="space-y-4">
          {documents.map((doc) => (
            <div key={doc.id} className="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                  <span className="text-2xl">{getFileTypeIcon(doc.file_type)}</span>
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-lg font-medium text-gray-900 truncate">
                      {doc.title}
                    </h3>
                    <span className="text-sm text-gray-500 ml-4 flex-shrink-0">
                      {formatDate(doc.created_at)}
                    </span>
                  </div>
                  
                  <div className="flex items-center space-x-4 text-sm text-gray-500 mb-3">
                    <span className="flex items-center space-x-1">
                      <FileText className="w-4 h-4" />
                      <span className="capitalize">{doc.file_type}</span>
                    </span>
                    <span className="flex items-center space-x-1">
                      <Clock className="w-4 h-4" />
                      <span>Added {formatDate(doc.created_at)}</span>
                    </span>
                  </div>
                  
                  {doc.summary && (
                    <p className="text-gray-700 mb-3 leading-relaxed">
                      {truncateText(doc.summary)}
                    </p>
                  )}
                  
                  {doc.tags && doc.tags.length > 0 && (
                    <div className="flex items-center space-x-2">
                      <Tag className="w-4 h-4 text-gray-400" />
                      <div className="flex flex-wrap gap-1">
                        {doc.tags.slice(0, 5).map((tag, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                          >
                            {tag}
                          </span>
                        ))}
                        {doc.tags.length > 5 && (
                          <span className="text-xs text-gray-500">
                            +{doc.tags.length - 5} more
                          </span>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <FileText className="w-16 h-16 text-gray-400 mx-auto mb-6" />
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            No Documents Yet
          </h3>
          <p className="text-gray-600 mb-8 max-w-md mx-auto">
            Upload your first document to start building your knowledge base. 
            Documents will appear here once they're processed.
          </p>
          <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Upload Document
          </button>
        </div>
      )}

      {/* Quick Actions */}
      {documents.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <Search className="w-5 h-5 text-blue-600" />
              <div className="text-left">
                <div className="font-medium text-gray-900">Advanced Search</div>
                <div className="text-sm text-gray-500">Filter by date, type, tags</div>
              </div>
            </button>
            
            <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <FileText className="w-5 h-5 text-green-600" />
              <div className="text-left">
                <div className="font-medium text-gray-900">Export Data</div>
                <div className="text-sm text-gray-500">Download your knowledge base</div>
              </div>
            </button>
            
            <button className="flex items-center space-x-3 p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <Tag className="w-5 h-5 text-purple-600" />
              <div className="text-left">
                <div className="font-medium text-gray-900">Manage Tags</div>
                <div className="text-sm text-gray-500">Organize your content</div>
              </div>
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
