import { useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

import { createRegistration } from "../services/registrationService";
import type {
  RegistrationFormData,
  RegistrationResponse,
} from "../types/registration";

const MAX_FILE_SIZE = 5 * 1024 * 1024;

const ALLOWED_TYPES = [
  "image/jpeg",
  "image/png",
  "image/webp",
];

const validationSchema = Yup.object({
  email: Yup.string()
    .email("Enter a valid email address.")
    .required("Email is required."),

  file: Yup.mixed<File>()
    .required("Please select an identity document image.")
    .test(
      "file-type",
      "Only JPEG, PNG, and WebP images are supported.",
      (file) => !file || ALLOWED_TYPES.includes(file.type)
    )
    .test(
      "file-size",
      "The image must not exceed 5 MB.",
      (file) => !file || file.size <= MAX_FILE_SIZE
    ),
});

const initialValues: RegistrationFormData = {
  email: "",
  file: null,
};

export default function RegistrationForm() {
  const [result, setResult] = useState<RegistrationResponse | null>(null);
  const [serverError, setServerError] = useState("");

  async function handleSubmit(
    values: RegistrationFormData,
    helpers: {
      setSubmitting: (isSubmitting: boolean) => void;
      resetForm: () => void;
    }
  ) {
    setResult(null);
    setServerError("");

    try {
      const registration = await createRegistration({
        email: values.email,
        file: values.file,
      });

      setResult(registration);
      helpers.resetForm();
    } catch (error) {
      setServerError(
        error instanceof Error
          ? error.message
          : "Could not connect to the server."
      );
    } finally {
      helpers.setSubmitting(false);
    }
  }

  return (
    <section className="card">
      <p className="eyebrow">MINI KYC</p>
      <h1>Identity registration</h1>

      <p className="description">
        Enter your email and upload an image of your identity document.
      </p>

      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={handleSubmit}
      >
        {({ isSubmitting, setFieldValue }) => (
          <Form>
            <label htmlFor="email">Email address</label>

            <Field
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              placeholder="name@example.com"
            />

            <ErrorMessage
              name="email"
              component="p"
              className="field-error"
            />

            <label htmlFor="file">Identity document</label>

            <input
              id="file"
              name="file"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              onChange={(event) => {
                setFieldValue(
                  "file",
                  event.currentTarget.files?.[0] ?? null
                );
              }}
            />

            <ErrorMessage
              name="file"
              component="p"
              className="field-error"
            />

            <p className="hint">
              JPEG, PNG or WebP. Maximum size: 5 MB.
            </p>

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting
                ? "Processing document..."
                : "Register identity"}
            </button>

            {serverError && (
              <div className="message error" role="alert">
                {serverError}
              </div>
            )}

            {result && (
              <div className="message success" role="status">
                <h2>Registration successful</h2>
                <p><strong>ID:</strong> {result.id}</p>
                <p><strong>Name:</strong> {result.full_name}</p>
                <p><strong>Document:</strong> {result.document_number}</p>
                <p><strong>Email:</strong> {result.email}</p>
              </div>
            )}
          </Form>
        )}
      </Formik>
    </section>
  );
}
