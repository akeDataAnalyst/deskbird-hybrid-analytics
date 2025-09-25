SELECT
    session_id,
    user_id,
    page_visited,
    timestamp,
    is_conversion_event,
    conversion_type,
    lead_id
FROM
    {{ source('deskbird_data', 'website_visits') }}