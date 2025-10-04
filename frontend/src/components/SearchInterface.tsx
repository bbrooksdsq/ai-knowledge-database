'use client'

import { useState } from 'react'
import { Search, Filter, Clock, FileText, Tag } from 'lucide-react'
import { Button } from './ui/button'

interface SearchResult {
  document: {
    id: number
    title: string
    content: string
    file_type: string
    tags: string[]
    created_at: string
    summary?: string
  }
  score: number
  snippet: string
}

interface SearchResponse {
  query: string
  results: SearchResult[]
  total_results: number
  execution_time: number
}

export default function SearchInterface() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const [searchType, setSearchType] = useState<'semantic' | 'keyword'>('semantic')
  const [executionTime, setExecutionTime] = useState(0)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || ''
      const endpoint = searchType === 'semantic' ? '/api/v1/documents/search' : '/api/v1/documents/search/keyword'
      const response = await fetch(`${apiUrl}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim(),
          limit: 20,
        }),
      })

      if (response.ok) {
        const data: SearchResponse = await response.json()
        setResults(data.results)
        setExecutionTime(data.execution_time)
      } else {
        console.error('Search failed')
      }
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
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

  return (
    <div className="space-y-6">
      {/* Search Form */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <form onSubmit={handleSearch} className="space-y-4">
          <div className="flex space-x-4">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search your knowledge base... (e.g., 'meeting notes about project timeline')"
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <Button type="submit" disabled={loading} className="px-8">
              {loading ? 'Searching...' : 'Search'}
            </Button>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <label className="flex items-center space-x-2">
                <input
                  type="radio"
                  name="searchType"
                  value="semantic"
                  checked={searchType === 'semantic'}
                  onChange={(e) => setSearchType(e.target.value as 'semantic' | 'keyword')}
                  className="text-blue-600"
                />
                <span className="text-sm font-medium">Semantic Search</span>
              </label>
              <label className="flex items-center space-x-2">
                <input
                  type="radio"
                  name="searchType"
                  value="keyword"
                  checked={searchType === 'keyword'}
                  onChange={(e) => setSearchType(e.target.value as 'semantic' | 'keyword')}
                  className="text-blue-600"
                />
                <span className="text-sm font-medium">Keyword Search</span>
              </label>
            </div>
            
            {executionTime > 0 && (
              <div className="text-sm text-gray-500">
                Found {results.length} results in {executionTime.toFixed(2)}s
              </div>
            )}
          </div>
        </form>
      </div>

      {/* Search Results */}
      {results.length > 0 && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">
              Search Results for "{query}"
            </h2>
            <div className="text-sm text-gray-500">
              {results.length} results
            </div>
          </div>
          
          <div className="space-y-4">
            {results.map((result) => (
              <div key={result.document.id} className="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">{getFileTypeIcon(result.document.file_type)}</span>
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-1">
                        {result.document.title}
                      </h3>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <span className="flex items-center space-x-1">
                          <FileText className="w-4 h-4" />
                          <span className="capitalize">{result.document.file_type}</span>
                        </span>
                        <span className="flex items-center space-x-1">
                          <Clock className="w-4 h-4" />
                          <span>{formatDate(result.document.created_at)}</span>
                        </span>
                        {searchType === 'semantic' && (
                          <span className="text-blue-600 font-medium">
                            {Math.round(result.score * 100)}% match
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mb-4">
                  <p className="text-gray-700 leading-relaxed">
                    {result.snippet}
                  </p>
                </div>
                
                {result.document.tags && result.document.tags.length > 0 && (
                  <div className="flex items-center space-x-2 mb-3">
                    <Tag className="w-4 h-4 text-gray-400" />
                    <div className="flex flex-wrap gap-1">
                      {result.document.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                
                {result.document.summary && (
                  <div className="mt-3 p-3 bg-gray-50 rounded-md">
                    <p className="text-sm text-gray-600">
                      <strong>Summary:</strong> {result.document.summary}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* No Results */}
      {results.length === 0 && query && !loading && (
        <div className="text-center py-12">
          <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
          <p className="text-gray-500">
            Try different keywords or check your spelling.
          </p>
        </div>
      )}

      {/* Welcome State */}
      {results.length === 0 && !query && (
        <div className="text-center py-12">
          <Search className="w-16 h-16 text-blue-500 mx-auto mb-6" />
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Search Your Knowledge Base
          </h3>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
            Ask questions in natural language to find relevant documents, 
            meeting notes, and team communications. Our AI understands context 
            and meaning, not just keywords.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Search className="w-6 h-6 text-blue-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Semantic Search</h4>
              <p className="text-sm text-gray-600">
                Find documents by meaning and context, not just exact words.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <FileText className="w-6 h-6 text-green-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Multiple Formats</h4>
              <p className="text-sm text-gray-600">
                Search across PDFs, documents, transcripts, and more.
              </p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-sm border">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <Tag className="w-6 h-6 text-purple-600" />
              </div>
              <h4 className="font-semibold text-gray-900 mb-2">Smart Tagging</h4>
              <p className="text-sm text-gray-600">
                Automatically tagged and categorized for easy discovery.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
