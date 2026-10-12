import { EmployeeList } from './components/EmployeeList'
import { SearchBar } from './components/SearchBar'
import { useEmployeeSearch } from './hooks/useEmployeeSearch'

function App() {
  const { query, setQuery, status, employees, total, errorMessage, retry } = useEmployeeSearch()

  return (
    <div className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-3xl px-4 py-10">
        <header className="mb-6">
          <h1 className="text-2xl font-semibold text-slate-900">Employee Directory</h1>
          <p className="mt-1 text-sm text-slate-500">Search employees by name or department.</p>
        </header>

        <div className="mb-6">
          <SearchBar value={query} onChange={setQuery} />
        </div>

        <EmployeeList
          status={status}
          employees={employees}
          total={total}
          query={query}
          errorMessage={errorMessage}
          onRetry={retry}
        />
      </div>
    </div>
  )
}

export default App
