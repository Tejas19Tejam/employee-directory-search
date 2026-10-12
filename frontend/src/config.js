/**
 * Centralized runtime configuration.
 *
 * The API base URL is read from Vite's environment variables (prefixed with
 * VITE_) rather than hardcoded, so the same build can point at different
 * backends across local/dev/staging/prod just by changing the .env file.
 */
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'
