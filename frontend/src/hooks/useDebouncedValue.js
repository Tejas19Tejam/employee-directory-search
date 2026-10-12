import { useEffect, useState } from 'react'

/**
 * Returns a debounced copy of `value` that only updates after `delayMs` of
 * no further changes. Used to avoid firing an API request on every keystroke
 * - e.g. typing "Rah" quickly results in a single request for "Rah" instead
 * of three requests for "R", "Ra", "Rah".
 */
export function useDebouncedValue(value, delayMs = 400) {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timeoutId = setTimeout(() => setDebouncedValue(value), delayMs)
    return () => clearTimeout(timeoutId)
  }, [value, delayMs])

  return debouncedValue
}
