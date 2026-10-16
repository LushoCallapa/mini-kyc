import type { RegistrationResponse } from "../types/registration";

interface RecognitionResultProps {
  result: RegistrationResponse | null;
  previewUrl: string | null;
  fileName: string | null;
}

export default function RecognitionResult({
  result,
  previewUrl,
  fileName,
}: RecognitionResultProps) {
  return (
    <section className="result-card" aria-labelledby="result-title">
      <div className="section-heading">
        <div>
          <p className="eyebrow">STEP 02</p>
          <h2 id="result-title">Recognition results</h2>
        </div>

        <span className={`result-badge ${result ? "is-success" : ""}`}>
          {result ? "Completed" : "Awaiting document"}
        </span>
      </div>

      <div className="document-preview">
        {previewUrl ? (
          <img
            className="document-image"
            src={previewUrl}
            alt="Preview of the selected identity document"
          />
        ) : (
          <div className="preview-placeholder">
            <div className="document-icon" aria-hidden="true">
              <svg
                viewBox="0 0 48 48"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <rect
                  x="10"
                  y="5"
                  width="28"
                  height="38"
                  rx="4"
                  stroke="currentColor"
                  strokeWidth="1.8"
                />
                <circle
                  cx="20"
                  cy="19"
                  r="4"
                  stroke="currentColor"
                  strokeWidth="1.8"
                />
                <path
                  d="M14 30C14 26.7 16.7 24 20 24C23.3 24 26 26.7 26 30M29 17H33M29 23H33M15 36H33"
                  stroke="currentColor"
                  strokeWidth="1.8"
                  strokeLinecap="round"
                />
              </svg>
            </div>

            <h3>Your document preview</h3>
            <p>Choose an image to see it here.</p>
          </div>
        )}
      </div>

      {fileName && (
        <p className="file-name" title={fileName}>
          <span aria-hidden="true">↗</span> {fileName}
        </p>
      )}

      <div className="recognized-data">
        <h3>Extracted information</h3>

        <div className="data-field">
          <span>Full name</span>
          <p>{result?.full_name ?? "Not available yet"}</p>
        </div>

        <div className="data-field">
          <span>Document number</span>
          <p>{result?.document_number ?? "Not available yet"}</p>
        </div>

        <div className="data-field">
          <span>Email address</span>
          <p>{result?.email ?? "Not available yet"}</p>
        </div>

        {result ? (
          <div className="success-notice" role="status">
            <span className="success-icon" aria-hidden="true">
              ✓
            </span>

            <div>
              <strong>Registration completed</strong>
              <p>Registration ID: {result.id}</p>
            </div>
          </div>
        ) : (
          <p className="result-hint">
            Your extracted information will appear here after processing.
          </p>
        )}
      </div>
    </section>
  );
}
