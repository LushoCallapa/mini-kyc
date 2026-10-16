import { env } from "../config/env";

const DEFAULT_ERROR_MESSAGE = "Request failed. Please try again.";
const NETWORK_ERROR_MESSAGE = "Could not connect to the server.";

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

function extractErrorMessage(data: unknown): string {
  if (typeof data !== "object" || data === null || !("detail" in data)) {
    return DEFAULT_ERROR_MESSAGE;
  }

  const { detail } = data;

  if (typeof detail === "string") {
    return detail;
  }

  // FastAPI validation errors (422) return detail as an array.
  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) =>
        typeof item === "object" &&
        item !== null &&
        "msg" in item &&
        typeof item.msg === "string"
          ? item.msg
          : null
      )
      .filter((message): message is string => message !== null);

    if (messages.length > 0) {
      return messages.join(" ");
    }
  }

  return DEFAULT_ERROR_MESSAGE;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${env.apiUrl}${path}`, init);
  } catch {
    throw new ApiError(NETWORK_ERROR_MESSAGE, 0);
  }

  const data: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    throw new ApiError(extractErrorMessage(data), response.status);
  }

  return data as T;
}

export function getJson<T>(path: string): Promise<T> {
  return request<T>(path);
}

export function postForm<T>(path: string, body: FormData): Promise<T> {
  return request<T>(path, { method: "POST", body });
}