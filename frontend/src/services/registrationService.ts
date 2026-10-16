import { getJson, postForm } from "./apiClient";
import type {
  RegistrationFormData,
  RegistrationRecord,
  RegistrationResponse,
} from "../types/registration";

const REGISTRATIONS_PATH = "/registrations";
const REGISTRATION_WITH_DOCUMENT_PATH = "/registrations/with-document";

export async function createRegistration(
  formData: RegistrationFormData
): Promise<RegistrationResponse> {
  if (!formData.file) {
    throw new Error("Please select an identity document image.");
  }

  const body = new FormData();
  body.append("email", formData.email);
  body.append("file", formData.file);

  return postForm<RegistrationResponse>(
    REGISTRATION_WITH_DOCUMENT_PATH,
    body
  );
}

export function listRegistrations(): Promise<RegistrationRecord[]> {
  return getJson<RegistrationRecord[]>(REGISTRATIONS_PATH);
}