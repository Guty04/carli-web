import {
  UnauthorizedError,
  ForbiddenError,
  NotFoundError,
  ValidationError,
  ServerError,
  ApiError,
} from "./errors";

export async function handleResponse<T>(response: Response): Promise<T> {
  if (response.ok) {
    if (response.status === 204) return undefined as T;
    return response.json() as Promise<T>;
  }

  if (response.status === 401) {
    const body = await response.json().catch(() => null);
    const message = typeof body?.detail === "string" ? body.detail : "Unauthorized";

    if (typeof window !== "undefined") {
      const { getToken, clearToken } = await import("@/shared/token-storage");
      const hadToken = !!getToken();
      clearToken();
      if (hadToken) {
        window.location.href = "/login?expired=true";
      }
    }
    throw new UnauthorizedError(message);
  }

  if (response.status === 403) {
    throw new ForbiddenError();
  }

  if (response.status === 404) {
    throw new NotFoundError();
  }

  if (response.status === 422) {
    const data = await response.json().catch(() => null);
    throw new ValidationError("Validation error", data);
  }

  if (response.status >= 500) {
    throw new ServerError();
  }

  throw new ApiError(response.status, `Unexpected error: ${response.status}`);
}
