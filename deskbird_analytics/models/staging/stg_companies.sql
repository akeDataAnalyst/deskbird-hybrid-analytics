SELECT
    company_id,
    company_name,
    company_size,
    -- Add the missing column here:
    country
FROM
    {{ source('deskbird_data', 'companies') }}