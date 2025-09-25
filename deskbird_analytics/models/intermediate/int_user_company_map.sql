SELECT
    u.user_id,
    u.first_name,
    u.last_name,
    u.email,
    u.company_id,
    c.company_name,
    c.company_size,
    c.country
FROM
    {{ ref('stg_users') }} AS u
LEFT JOIN
    {{ ref('stg_companies') }} AS c
ON
    u.company_id = c.company_id