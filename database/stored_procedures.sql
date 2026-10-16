DROP PROCEDURE IF EXISTS sp_create_onboarding_record;

DELIMITER //

CREATE PROCEDURE sp_create_onboarding_record(
    IN p_email VARCHAR(255),
    IN p_full_name VARCHAR(255),
    IN p_document_number VARCHAR(100)
)
BEGIN
    INSERT INTO onboarding_records (
        email,
        full_name,
        document_number
    )
    VALUES (
        p_email,
        p_full_name,
        p_document_number
    );

    SELECT
        id,
        email,
        full_name,
        document_number,
        created_at
    FROM onboarding_records
    WHERE id = LAST_INSERT_ID();
END //

DELIMITER ;