'use client'

import { useState, useRef } from 'react'
import { Mic, Upload, FileText, Clock, Users, CheckCircle } from 'lucide-react'
import { Button } from './ui/button'

interface TranscriptionResult {
  document: {
    id: number
    title: string
    content: string
    file_type: string
    tags: string[]
    created_at: string
    summary?: string
  }
  speakers?: string[]
  processing_time?: number
}

export default function AudioTranscription() {
  const [file, setFile] = useState<File | null>(null)
  const [title, setTitle] = useState('')
  const [withSpeakers, setWithSpeakers] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState<TranscriptionResult | null>(null)
  const [error, setError] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile)
    setError('')
    setResult(null)
    
    // Auto-generate title if not provided
    if (!title) {
      const timestamp = new Date().toLocaleString()
      setTitle(`Meeting Recording - ${timestamp}`)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select an audio file')
      return
    }

    setUploading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('title', title)
      formData.append('source', 'audio_upload')
      formData.append('with_speakers', withSpeakers.toString())

      const response = await fetch('/api/v1/transcription/audio', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        setResult({
          document: data,
          speakers: data.speakers || [],
          processing_time: Date.now() - Date.now() // We could track this better
        })
        setFile(null)
        setTitle('')
      } else {
        const errorData = await response.json()
        setError(errorData.detail || 'Transcription failed')
      }
    } catch (err) {
      setError('Network error occurred')
    } finally {
      setUploading(false)
    }
  }

  const testWhisperAPI = async () => {
    try {
      const response = await fetch('/api/v1/transcription/test-audio')
      const data = await response.json()
      
      if (data.status === 'success') {
        alert('✅ Whisper API is working! OpenAI transcription is ready.')
      } else {
        alert(`❌ Whisper API test failed: ${data.message}`)
      }
    } catch (err) {
      alert('❌ Could not test Whisper API')
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileTypeIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase()
    switch (ext) {
      case 'mp3':
      case 'wav':
      case 'm4a':
      case 'flac':
        return '🎵'
      default:
        return '🎤'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Audio Transcription</h2>
            <p className="text-gray-600">
              Upload audio files to automatically transcribe with OpenAI Whisper
            </p>
          </div>
          <Button onClick={testWhisperAPI} variant="outline" className="flex items-center space-x-2">
            <Mic className="w-4 h-4" />
            <span>Test Whisper API</span>
          </Button>
        </div>
      </div>

      {/* Upload Form */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="space-y-4">
          {/* File Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Audio File
            </label>
            <div
              className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-gray-400 transition-colors cursor-pointer"
              onClick={() => fileInputRef.current?.click()}
            >
              {file ? (
                <div className="space-y-2">
                  <div className="text-2xl">{getFileTypeIcon(file.name)}</div>
                  <div className="font-medium text-gray-900">{file.name}</div>
                  <div className="text-sm text-gray-500">{formatFileSize(file.size)}</div>
                </div>
              ) : (
                <div className="space-y-2">
                  <Upload className="w-8 h-8 text-gray-400 mx-auto" />
                  <div className="text-gray-600">Click to select audio file</div>
                  <div className="text-sm text-gray-500">MP3, WAV, M4A, FLAC supported</div>
                </div>
              )}
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="audio/*"
              onChange={(e) => e.target.files?.[0] && handleFileSelect(e.target.files[0])}
              className="hidden"
            />
          </div>

          {/* Title Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Document Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter a title for this transcript..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Speaker Identification */}
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="withSpeakers"
              checked={withSpeakers}
              onChange={(e) => setWithSpeakers(e.target.checked)}
              className="text-blue-600"
            />
            <label htmlFor="withSpeakers" className="text-sm font-medium text-gray-700">
              Identify speakers (requires OpenAI API)
            </label>
          </div>

          {/* Upload Button */}
          <Button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="w-full"
          >
            {uploading ? (
              <>
                <Clock className="w-4 h-4 mr-2 animate-spin" />
                Transcribing...
              </>
            ) : (
              <>
                <Mic className="w-4 h-4 mr-2" />
                Transcribe Audio
              </>
            )}
          </Button>

          {/* Error Display */}
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <div className="flex items-center space-x-2 mb-4">
            <CheckCircle className="w-5 h-5 text-green-600" />
            <h3 className="text-lg font-semibold text-gray-900">Transcription Complete</h3>
          </div>

          <div className="space-y-4">
            {/* Document Info */}
            <div className="border-b pb-4">
              <h4 className="font-medium text-gray-900 mb-2">{result.document.title}</h4>
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <span className="flex items-center space-x-1">
                  <FileText className="w-4 h-4" />
                  <span>Audio Transcript</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Clock className="w-4 h-4" />
                  <span>{new Date(result.document.created_at).toLocaleString()}</span>
                </span>
              </div>
            </div>

            {/* Speakers */}
            {result.speakers && result.speakers.length > 0 && (
              <div>
                <h5 className="font-medium text-gray-900 mb-2 flex items-center space-x-2">
                  <Users className="w-4 h-4" />
                  <span>Speakers Identified</span>
                </h5>
                <div className="flex flex-wrap gap-2">
                  {result.speakers.map((speaker, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full"
                    >
                      {speaker}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Summary */}
            {result.document.summary && (
              <div>
                <h5 className="font-medium text-gray-900 mb-2">AI Summary</h5>
                <p className="text-gray-700 bg-gray-50 p-3 rounded-lg">
                  {result.document.summary}
                </p>
              </div>
            )}

            {/* Tags */}
            {result.document.tags && result.document.tags.length > 0 && (
              <div>
                <h5 className="font-medium text-gray-900 mb-2">Auto-Generated Tags</h5>
                <div className="flex flex-wrap gap-2">
                  {result.document.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Transcript Preview */}
            <div>
              <h5 className="font-medium text-gray-900 mb-2">Transcript Preview</h5>
              <div className="bg-gray-50 p-4 rounded-lg max-h-64 overflow-y-auto">
                <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                  {result.document.content.substring(0, 500)}
                  {result.document.content.length > 500 && '...'}
                </pre>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-3">How Audio Transcription Works</h3>
        <ul className="space-y-2 text-sm text-blue-800">
          <li>• Upload audio files (MP3, WAV, M4A, FLAC) up to 25MB</li>
          <li>• OpenAI Whisper automatically transcribes speech to text</li>
          <li>• AI identifies different speakers in meetings</li>
          <li>• Documents are automatically tagged and summarized</li>
          <li>• Transcripts become searchable in your knowledge base</li>
        </ul>
      </div>
    </div>
  )
}
