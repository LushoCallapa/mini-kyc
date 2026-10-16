import { useRef, useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";

import { registrationSchema } from "../validation/registrationSchema";
import { useRegistration } from "../hooks/useRegistration";
import { useFilePreview } from "../hooks/useFilePreview";
import { useScrollIntoViewOnMobile } from "../hooks/useScrollIntoViewOnMobile";
import type { RegistrationFormData } from "../types/registration";
import FileUploadField from "./FileUploadField";
import RecognitionResult from "./RecognitionResult";

const initialValues: RegistrationFormData = {
  email: "",
  file: null,
};

export default function RegistrationForm() {
  const { result, serverError, submit, reset } = useRegistration();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const previewUrl = useFilePreview(selectedFile);

  const resultRef = useRef<HTMLDivElement | null>(null);
  useScrollIntoViewOnMobile(resultRef, result !== null);

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
    reset();
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
          validationSchema={registrationSchema}
          onSubmit={(values) => submit(values)}
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

              <FileUploadField
                fileName={values.file?.name ?? null}
                onFileChange={(file) =>
                  handleFileChange(file, setFieldValue)
                }
              />

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