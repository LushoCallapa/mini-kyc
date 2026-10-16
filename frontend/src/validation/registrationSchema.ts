import * as Yup from "yup";
import { ALLOWED_TYPES, MAX_FILE_SIZE } from "../config/upload";

export const registrationSchema = Yup.object({
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