"use client"

import { type FormEvent, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface SearchFormProps {
  onSearch: (url: string, query: string) => void
  disabled: boolean
}

export default function SearchForm({ onSearch, disabled }: SearchFormProps) {
  const [url, setUrl] = useState("https://example.com")
  const [query, setQuery] = useState("")

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (url.trim() && query.trim()) {
      onSearch(url.trim(), query.trim())
    }
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-2xl mx-auto">
      <div className="bg-white rounded-2xl shadow-lg p-8 border border-border">
        <div className="space-y-6">
          {/* Website URL Input */}
          <div>
            <label htmlFor="url" className="block text-sm font-medium text-primary mb-2">
              Website URL
            </label>
            <Input
              id="url"
              type="url"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={disabled}
              required
              className="w-full"
            />
            <p className="text-xs text-accent mt-2">Enter the URL of the website you want to search</p>
          </div>

          {/* Search Query Input */}
          <div>
            <label htmlFor="query" className="block text-sm font-medium text-primary mb-2">
              Search Query
            </label>
            <Input
              id="query"
              type="text"
              placeholder="What are you looking for?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={disabled}
              required
              className="w-full"
            />
            <p className="text-xs text-accent mt-2">Enter keywords or phrases to search the HTML content</p>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            disabled={disabled || !url.trim() || !query.trim()}
            className="w-full bg-primary hover:bg-primary/90 text-white font-medium py-2.5 rounded-lg transition-colors"
          >
            {disabled ? "Searching..." : "Search"}
          </Button>
        </div>
      </div>
    </form>
  )
}
