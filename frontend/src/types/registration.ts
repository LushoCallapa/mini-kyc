export interface RegistrationResponse {
  id: number;
  email: string;
  full_name: string;
  document_number: string;
  message: string;
}

export interface RegistrationFormData {
  email: string;
  file: File | null;
}