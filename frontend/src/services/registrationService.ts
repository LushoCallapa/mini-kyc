import { postForm } from "./apiClient";
import type {
  RegistrationFormData,
  RegistrationResponse,
} from "../types/registration";

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