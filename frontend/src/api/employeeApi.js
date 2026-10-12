import { API_BASE_URL } from '../config'

/**
 * Thrown when the backend responds with a non-2xx status. Carries the
 * server-provided message (if any) and HTTP status so UI code can present
 * user-friendly errors without parsing responses itself.
 */
export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

/**
 * Fetch employees from the backend, optionally filtered by a search term.
 *
 * This function contains ALL API/network logic for employees - UI components
 * never call `fetch` directly. That keeps components simple and makes this
 * logic reusable/testable in isolation.
 *
 * @param {Object} params
 * @param {string} [params.search] - Term matched against name or department.
 * @param {number} [params.limit] - Page size.
 * @param {number} [params.offset] - Number of records to skip.
 * @param {AbortSignal} [params.signal] - Allows the caller to cancel an in-flight request.
 */
export async function fetchEmployees({ search, limit = 20, offset = 0, signal } = {}) {
  const params = new URLSearchParams()
  if (search) params.set('search', search)
  params.set('limit', String(limit))
  params.set('offset', String(offset))

  let response
  try {
    response = await fetch(`${API_BASE_URL}/employees?${params.toString()}`, { signal })
  } catch (err) {
    if (err.name === 'AbortError') throw err
    // Network-level failure: backend unreachable, DNS failure, CORS block, etc.
    throw new ApiError('Could not reach the server. Please check your connection and try again.', 0)
  }

  if (!response.ok) {
    let detail = 'Something went wrong while fetching employees.'
    try {
      const body = await response.json()
      if (body?.detail) detail = body.detail
    } catch {
      // response body wasn't JSON - fall back to the generic message
    }
    throw new ApiError(detail, response.status)
  }

  return response.json()
}
