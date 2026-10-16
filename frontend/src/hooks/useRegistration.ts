import { useState } from "react";

import { createRegistration } from "../services/registrationService";
import type {
  RegistrationFormData,
  RegistrationResponse,
} from "../types/registration";

export function useRegistration() {
  const [result, setResult] = useState<RegistrationResponse | null>(null);
  const [serverError, setServerError] = useState("");

  async function submit(values: RegistrationFormData) {
    setResult(null);
    setServerError("");

    try {
      const registration = await createRegistration(values);
      setResult(registration);
    } catch (error) {
      setServerError(
        error instanceof Error
          ? error.message
          : "Could not connect to the server."
      );
    }
  }

  function reset() {
    setResult(null);
    setServerError("");
  }

  return { result, serverError, submit, reset };
}