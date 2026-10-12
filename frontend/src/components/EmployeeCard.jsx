function formatDate(isoDate) {
  try {
    return new Date(isoDate).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  } catch {
    return isoDate
  }
}

function initials(name) {
  return name
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('')
}

/**
 * Displays a single employee. Pure presentational component driven entirely
 * by props - no data fetching here.
 */
export function EmployeeCard({ employee }) {
  const { name, email, department, designation, date_of_joining } = employee

  return (
    <div className="flex items-start gap-4 rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-md">
      <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-sm font-semibold text-indigo-700">
        {initials(name)}
      </div>
      <div className="min-w-0 flex-1">
        <div className="flex flex-wrap items-baseline justify-between gap-2">
          <h3 className="truncate text-base font-semibold text-slate-900">{name}</h3>
          <span className="shrink-0 rounded-full bg-indigo-50 px-2.5 py-0.5 text-xs font-medium text-indigo-700">
            {department}
          </span>
        </div>
        <p className="truncate text-sm text-slate-500">{designation}</p>
        <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-slate-500">
          <span className="truncate">{email}</span>
          <span>Joined {formatDate(date_of_joining)}</span>
        </div>
      </div>
    </div>
  )
}
