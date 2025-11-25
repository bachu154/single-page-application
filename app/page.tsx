"use client"

import { useState } from "react"
import SearchForm from "@/components/search-form"
import SearchResults from "@/components/search-results"
import Header from "@/components/header"

export default function Home() {
  const [results, setResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (url: string, query: string) => {
    setLoading(true)
    setError(null)
    setHasSearched(true)

    try {
      const response = await fetch("http://localhost:8000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url, query }),
      })

      if (!response.ok) {
        throw new Error(`API error: ${response.statusText}`)
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
      setResults([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-background to-secondary">
      <Header />
      <div className="container mx-auto px-4 py-12">
        <SearchForm onSearch={handleSearch} disabled={loading} />

        {loading && (
          <div className="mt-12 text-center">
            <div className="inline-block">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
            <p className="mt-4 text-accent">Processing your search...</p>
          </div>
        )}

        {error && (
          <div className="mt-12 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-800 font-medium">Error: {error}</p>
            <p className="text-red-600 text-sm mt-2">
              Make sure the backend server is running at http://localhost:8000
            </p>
          </div>
        )}

        {hasSearched && !loading && !error && <SearchResults results={results} />}
      </div>
    </main>
  )
}
