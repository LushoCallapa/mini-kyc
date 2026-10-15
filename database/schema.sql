USE mini_kyc;

CREATE TABLE IF NOT EXISTS onboarding_records (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    document_number VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_onboarding_email UNIQUE (email),
    CONSTRAINT uq_onboarding_document_number UNIQUE (document_number)
);