import { ErrorMessage } from "formik";

import { ALLOWED_TYPES } from "../config/upload";
import UploadIcon from "./icons/UploadIcon";

interface FileUploadFieldProps {
  fileName: string | null;
  onFileChange: (file: File | null) => void;
}

export default function FileUploadField({
  fileName,
  onFileChange,
}: FileUploadFieldProps) {
  return (
    <div className="form-field">
      <label htmlFor="file">Identity document</label>

      <div className="upload-area">
        <input
          id="file"
          name="file"
          type="file"
          accept={ALLOWED_TYPES.join(",")}
          className="file-input"
          aria-describedby="file-hint"
          onChange={(event) =>
            onFileChange(event.currentTarget.files?.[0] ?? null)
          }
        />

        <label htmlFor="file" className="upload-label">
          <span className="upload-icon" aria-hidden="true">
            <UploadIcon />
          </span>

          <strong>
            {fileName ? "Choose another image" : "Upload your document"}
          </strong>

          <span>{fileName ?? "Click or tap to select an image"}</span>
        </label>
      </div>

      <ErrorMessage name="file" component="p" className="field-error" />

      <p id="file-hint" className="hint">
        JPEG, PNG or WebP. Maximum size: 5 MB.
      </p>
    </div>
  );
}