const HAS_TIMEZONE = /(Z|[+-]\d{2}:?\d{2})$/;

export function formatDateTime(value: string): string {
  const normalized = HAS_TIMEZONE.test(value) ? value : `${value}Z`;
  const date = new Date(normalized);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString();
}