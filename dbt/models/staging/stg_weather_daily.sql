select
    date,
    city,
    latitude,
    longitude,
    temperature_2m_max,
    temperature_2m_min,
    precipitation_sum
from {{ source('raw', 'weather_daily') }}