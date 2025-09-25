SELECT
    user_id,
    first_name,
    last_name,
    email,
    company_id
FROM
    {{ source('deskbird_data', 'users') }}
