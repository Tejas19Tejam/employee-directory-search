/** Shown while a search request is in flight. */
export function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center gap-3 py-16 text-slate-500">
      <div
        className="h-8 w-8 animate-spin rounded-full border-2 border-slate-200 border-t-indigo-600"
        role="status"
        aria-label="Loading employees"
      />
      <p className="text-sm">Loading employees...</p>
    </div>
  )
}

/** Shown when a search returns zero results. */
export function EmptyState({ query }) {
  return (
    <div className="flex flex-col items-center justify-center gap-2 rounded-lg border border-dashed border-slate-300 py-16 text-center">
      <p className="text-base font-medium text-slate-700">No employees found</p>
      <p className="max-w-sm text-sm text-slate-500">
        {query
          ? `No results for "${query}". Try a different name or department.`
          : 'No employees to display.'}
      </p>
    </div>
  )
}

/** Shown when the API request fails. Message is always user-friendly text from the API layer. */
export function ErrorState({ message, onRetry }) {
  return (
    <div
      role="alert"
      className="flex flex-col items-center justify-center gap-3 rounded-lg border border-red-200 bg-red-50 py-16 text-center"
    >
      <p className="text-base font-medium text-red-700">Something went wrong</p>
      <p className="max-w-sm text-sm text-red-600">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-300"
        >
          Try again
        </button>
      )}
    </div>
  )
}
