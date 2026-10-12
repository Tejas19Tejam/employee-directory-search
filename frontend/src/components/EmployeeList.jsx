import { EmployeeCard } from './EmployeeCard'
import { EmptyState, ErrorState, LoadingState } from './StatusStates'

/**
 * Renders the employee list for the current search state. Receives all data
 * and status flags as props - contains no fetching logic itself, only
 * decides which visual state to render.
 */
export function EmployeeList({ status, employees, total, query, errorMessage, onRetry }) {
  if (status === 'loading') {
    return <LoadingState />
  }

  if (status === 'error') {
    return <ErrorState message={errorMessage} onRetry={onRetry} />
  }

  if (employees.length === 0) {
    return <EmptyState query={query} />
  }

  return (
    <div>
      <p className="mb-3 text-sm text-slate-500">
        {total} {total === 1 ? 'employee' : 'employees'} found
      </p>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        {employees.map((employee) => (
          <EmployeeCard key={employee.id} employee={employee} />
        ))}
      </div>
    </div>
  )
}
