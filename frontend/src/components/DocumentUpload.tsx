'use client'

import { useState, useRef } from 'react'
import { Upload, FileText, X, CheckCircle } from 'lucide-react'
import { Button } from './ui/button'

interface UploadedFile {
  file: File
  id: string
  status: 'uploading' | 'success' | 'error'
  progress: number
  error?: string
}

export default function DocumentUpload() {
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFiles = (selectedFiles: FileList | null) => {
    if (!selectedFiles) return

    const newFiles = Array.from(selectedFiles).map(file => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      status: 'uploading' as const,
      progress: 0,
    }))

    setFiles(prev => [...prev, ...newFiles])

    // Simulate upload process
    newFiles.forEach(fileItem => {
      uploadFile(fileItem.id)
    })
  }

  const uploadFile = async (fileId: string) => {
    const fileIndex = files.findIndex(f => f.id === fileId)
    if (fileIndex === -1) return

    const file = files[fileIndex]
    
    // Set initial progress
    setFiles(prev => prev.map(f => 
      f.id === fileId 
        ? { ...f, progress: 10 }
        : f
    ))

    try {
      const formData = new FormData()
      formData.append('title', file.file.name)
      formData.append('file_type', getFileType(file.file.name))
      formData.append('source', 'upload')
      formData.append('file', file.file)

      console.log('Starting upload for:', file.file.name)
      
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || ''
      const response = await fetch(`${apiUrl}/api/v1/documents/`, {
        method: 'POST',
        body: formData,
      })

      console.log('Upload response status:', response.status)
      
      if (response.ok) {
        const result = await response.json()
        console.log('Upload successful:', result)
        setFiles(prev => prev.map(f => 
          f.id === fileId 
            ? { ...f, status: 'success', progress: 100 }
            : f
        ))
      } else {
        const errorText = await response.text()
        console.error('Upload failed:', response.status, errorText)
        throw new Error(`Upload failed: ${response.status} - ${errorText}`)
      }
    } catch (error) {
      console.error('Upload error:', error)
      const errorMessage = error instanceof Error ? error.message : 'Upload failed'
      setFiles(prev => prev.map(f => 
        f.id === fileId 
          ? { ...f, status: 'error', error: errorMessage }
          : f
      ))
    }
  }

  const getFileType = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase()
    switch (ext) {
      case 'pdf':
        return 'pdf'
      case 'doc':
      case 'docx':
        return 'docx'
      case 'txt':
        return 'txt'
      case 'mp3':
      case 'wav':
      case 'm4a':
        return 'audio'
      case 'mp4':
      case 'avi':
      case 'mov':
        return 'video'
      default:
        return 'document'
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId))
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files)
    }
  }

  return (
    <div className="space-y-6">
      {/* Upload Area */}
      <div className="bg-white rounded-lg shadow-sm border p-8">
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors ${
            dragActive 
              ? 'border-blue-500 bg-blue-50' 
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <Upload className="w-16 h-16 text-gray-400 mx-auto mb-6" />
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Upload Documents to Your Knowledge Base
          </h3>
          <p className="text-gray-600 mb-6">
            Drag and drop files here, or click to browse. Supports PDFs, documents, 
            audio files, and more.
          </p>
          <div className="space-y-3">
            <Button
              onClick={() => fileInputRef.current?.click()}
              className="px-8"
            >
              Choose Files
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              multiple
              onChange={(e) => handleFiles(e.target.files)}
              className="hidden"
              accept=".pdf,.doc,.docx,.txt,.mp3,.wav,.m4a,.mp4,.avi,.mov"
            />
            <p className="text-sm text-gray-500">
              Maximum file size: 50MB
            </p>
          </div>
        </div>
      </div>

      {/* File List */}
      {files.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border">
          <div className="p-6 border-b">
            <h3 className="text-lg font-semibold text-gray-900">
              Upload Progress ({files.length} files)
            </h3>
          </div>
          <div className="divide-y">
            {files.map((file) => (
              <div key={file.id} className="p-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                      <FileText className="w-6 h-6 text-gray-600" />
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900">{file.file.name}</h4>
                      <p className="text-sm text-gray-500">
                        {formatFileSize(file.file.size)} • {getFileType(file.file.name).toUpperCase()}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-4">
                    {file.status === 'uploading' && (
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${file.progress}%` }}
                        />
                      </div>
                    )}
                    
                    {file.status === 'success' && (
                      <div className="flex items-center space-x-2 text-green-600">
                        <CheckCircle className="w-5 h-5" />
                        <span className="text-sm font-medium">Uploaded</span>
                      </div>
                    )}
                    
                    {file.status === 'error' && (
                      <div className="text-red-600 text-sm">
                        {file.error}
                      </div>
                    )}
                    
                    <button
                      onClick={() => removeFile(file.id)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Upload Tips */}
      <div className="bg-blue-50 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-3">Upload Tips</h3>
        <ul className="space-y-2 text-sm text-blue-800">
          <li>• Documents will be automatically processed and made searchable</li>
          <li>• AI will extract key topics, entities, and generate summaries</li>
          <li>• Audio files will be transcribed using speech recognition</li>
          <li>• Large files may take a few minutes to process</li>
        </ul>
      </div>
    </div>
  )
}
