import { useEffect, useRef, useState } from 'react'
import { ApiError, fetchEmployees } from '../api/employeeApi'
import { useDebouncedValue } from './useDebouncedValue'

/**
 * Encapsulates all state and side-effects for the employee search feature:
 * debouncing the raw input, calling the API, and tracking the request
 * lifecycle (idle/loading/success/error) plus the resulting data.
 *
 * Keeping this logic in a hook (rather than inside a component) means
 * SearchBar/EmployeeList/EmployeeCard stay purely presentational and can be
 * reused or tested independently of how data is fetched.
 */
export function useEmployeeSearch({ debounceMs = 400 } = {}) {
  const [rawQuery, setRawQuery] = useState('')
  const debouncedQuery = useDebouncedValue(rawQuery, debounceMs)

  const [status, setStatus] = useState('loading') // 'loading' | 'success' | 'error'
  const [employees, setEmployees] = useState([])
  const [total, setTotal] = useState(0)
  const [errorMessage, setErrorMessage] = useState(null)
  // Bumping this forces the effect below to re-run even when debouncedQuery
  // hasn't changed, which is what powers the "Try again" retry button.
  const [retryToken, setRetryToken] = useState(0)

  // Tracks the most recent request so a slow earlier response can't
  // overwrite a newer one ("race condition" guard) and lets us cancel
  // in-flight requests when the query changes again or the component unmounts.
  const abortControllerRef = useRef(null)

  useEffect(() => {
    abortControllerRef.current?.abort()
    const controller = new AbortController()
    abortControllerRef.current = controller

    const trimmed = debouncedQuery.trim()

    async function run() {
      setStatus('loading')
      setErrorMessage(null)

      try {
        const data = await fetchEmployees({
          search: trimmed || undefined,
          limit: 50,
          signal: controller.signal,
        })
        setEmployees(data.items)
        setTotal(data.total)
        setStatus('success')
      } catch (err) {
        if (err.name === 'AbortError') return // superseded by a newer request
        const message = err instanceof ApiError ? err.message : 'An unexpected error occurred.'
        setErrorMessage(message)
        setStatus('error')
      }
    }

    run()

    return () => controller.abort()
  }, [debouncedQuery, retryToken])

  return {
    query: rawQuery,
    setQuery: setRawQuery,
    status,
    employees,
    total,
    errorMessage,
    isDebouncing: rawQuery !== debouncedQuery,
    retry: () => setRetryToken((t) => t + 1),
  }
}
