import { env } from "../config/env";
import type {
  RegistrationFormData,
  RegistrationResponse,
} from "../types/registration";

export async function createRegistration(
  formData: RegistrationFormData
): Promise<RegistrationResponse> {
  if (!formData.file) {
    throw new Error("Please select an identity document image.");
  }

  const body = new FormData();

  body.append("email", formData.email);
  body.append("file", formData.file);

  const response = await fetch(
    `${env.apiUrl}/registrations/with-document`,
    {
      method: "POST",
      body,
    }
  );

  const data: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    const detail =
      typeof data === "object" &&
      data !== null &&
      "detail" in data &&
      typeof data.detail === "string"
        ? data.detail
        : "Registration failed. Please try again.";

    throw new Error(detail);
  }

  return data as RegistrationResponse;
}