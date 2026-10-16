import { useEffect, useRef, useState } from "react";
import {
  Formik,
  Form,
  Field,
  ErrorMessage,
  type FormikHelpers,
} from "formik";
import * as Yup from "yup";

import { createRegistration } from "../services/registrationService";
import type {
  RegistrationFormData,
  RegistrationResponse,
} from "../types/registration";
import RecognitionResult from "./RecognitionResult";

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
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  const resultRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl(null);
      return;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);

    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [selectedFile]);

  useEffect(() => {
    if (!result) return;

    if (window.matchMedia("(max-width: 900px)").matches) {
      resultRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, [result]);

  async function handleSubmit(
    values: RegistrationFormData,
    helpers: FormikHelpers<RegistrationFormData>
  ) {
    setResult(null);
    setServerError("");

    try {
      const registration = await createRegistration({
        email: values.email,
        file: values.file,
      });

      setResult(registration);
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

  function handleFileChange(
    file: File | null,
    setFieldValue: (
      field: string,
      value: unknown,
      shouldValidate?: boolean
    ) => void
  ) {
    setSelectedFile(file);
    setFieldValue("file", file);
    setResult(null);
    setServerError("");
  }

  return (
    <div className="workspace">
      <section className="form-card" aria-labelledby="registration-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">STEP 01</p>
            <h2 id="registration-title">Verify your identity</h2>
          </div>

          <span className="step-number">01 / 02</span>
        </div>

        <p className="section-description">
          Enter your email and upload a clear image of your identity
          document. Our system will extract the information automatically.
        </p>

        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting, setFieldValue, values }) => (
            <Form noValidate>
              <div className="form-field">
                <label htmlFor="email">Email address</label>

                <Field
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  placeholder="name@example.com"
                  className="text-input"
                />

                <ErrorMessage
                  name="email"
                  component="p"
                  className="field-error"
                />
              </div>

              <div className="form-field">
                <label htmlFor="file">Identity document</label>

                <div className="upload-area">
                  <input
                    id="file"
                    name="file"
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    className="file-input"
                    aria-describedby="file-hint"
                    onChange={(event) => {
                      const file =
                        event.currentTarget.files?.[0] ?? null;

                      handleFileChange(file, setFieldValue);
                    }}
                  />

                  <label htmlFor="file" className="upload-label">
                    <span className="upload-icon" aria-hidden="true">
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M12 16V4M7.5 8.5L12 4L16.5 8.5M4 15.5V19C4 19.55 4.45 20 5 20H19C19.55 20 20 19.55 20 19V15.5"
                          stroke="currentColor"
                          strokeWidth="1.7"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </span>

                    <strong>
                      {values.file
                        ? "Choose another image"
                        : "Upload your document"}
                    </strong>

                    <span>
                      {values.file
                        ? values.file.name
                        : "Click or tap to select an image"}
                    </span>
                  </label>
                </div>

                <ErrorMessage
                  name="file"
                  component="p"
                  className="field-error"
                />

                <p id="file-hint" className="hint">
                  JPEG, PNG or WebP. Maximum size: 5 MB.
                </p>
              </div>

              {serverError && (
                <div className="message error" role="alert">
                  <strong>Unable to complete registration</strong>
                  <p>{serverError}</p>
                </div>
              )}

              <button
                className="submit-button"
                type="submit"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <span
                      className="loading-spinner"
                      aria-hidden="true"
                    />
                    Processing document...
                  </>
                ) : (
                  "Process and register"
                )}
              </button>

              <p className="privacy-note">
                Your document is sent to the configured API for processing.
              </p>
            </Form>
          )}
        </Formik>
      </section>

      <div
        ref={resultRef}
        className="recognition-result-anchor"
        aria-live="polite"
      >
        <RecognitionResult
          result={result}
          previewUrl={previewUrl}
          fileName={selectedFile?.name ?? null}
        />
      </div>
    </div>
  );
}
