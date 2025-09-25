SELECT
    DATE(cpu.event_timestamp) AS event_date,
    DAYOFWEEK(cpu.event_timestamp) AS day_of_week,
    cpu.company_id,
    cpu.company_size, -- New dimension for segmentation
    SUM(CASE WHEN cpu.event_name = 'desk_booking_event' THEN 1 ELSE 0 END) AS total_desk_bookings,
    SUM(CASE WHEN cpu.event_name = 'meeting_room_booking_event' THEN 1 ELSE 0 END) AS total_room_bookings,
    COUNT(DISTINCT cpu.user_id) AS active_users
FROM
    {{ ref('int_customer_product_usage') }} AS cpu
GROUP BY 1, 2, 3, 4
ORDER BY 1, 2