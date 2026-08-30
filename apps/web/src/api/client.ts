const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "";

export async function apiDelay<T>(value: T, delay = 240): Promise<T> {
  await new Promise((resolve) => window.setTimeout(resolve, delay));
  return value;
}

export function getApiUrl(path: string) {
  return `${API_BASE_URL}${path}`;
}
