"use client"

interface SearchResult {
  chunk_index: number
  content: string
  score: number
  url: string
}

interface SearchResultsProps {
  results: SearchResult[]
}

export default function SearchResults({ results }: SearchResultsProps) {
  if (!results || results.length === 0) {
    return (
      <div className="mt-12 text-center">
        <p className="text-lg text-accent">No results found for your query.</p>
      </div>
    )
  }

  return (
    <div className="mt-12">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-primary">Results ({results.length})</h2>
        <p className="text-accent text-sm mt-2">Showing top 10 matched HTML chunks sorted by similarity score</p>
      </div>

      <div className="grid gap-4">
        {results.map((result, index) => (
          <div key={index} className="bg-white rounded-lg border border-border p-6 hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <div>
                <p className="text-xs font-medium text-accent uppercase tracking-wide">Chunk {result.chunk_index}</p>
                <p className="text-xs text-accent mt-1">Score: {(1 - result.score / 100).toFixed(3)}</p>
              </div>
              <a
                href={result.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs font-medium text-primary hover:underline"
              >
                Visit URL →
              </a>
            </div>

            <div className="bg-secondary rounded p-4 mb-3 max-h-32 overflow-y-auto">
              <p className="text-sm text-foreground leading-relaxed line-clamp-6">{result.content}</p>
            </div>

            <p className="text-xs text-accent">Max tokens: 500 | Content preview</p>
          </div>
        ))}
      </div>
    </div>
  )
}
