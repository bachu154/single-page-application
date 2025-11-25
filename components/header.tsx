export default function Header() {
  return (
    <header className="bg-white border-b border-border sticky top-0 z-50">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-primary">Search Engine</h1>
            <p className="text-accent text-sm mt-1">Semantic search for HTML content</p>
          </div>
          <div className="text-xs text-accent bg-secondary px-3 py-1 rounded-full">v0.1</div>
        </div>
      </div>
    </header>
  )
}
