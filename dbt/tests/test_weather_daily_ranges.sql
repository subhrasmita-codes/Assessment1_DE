select *
from {{ ref('stg_weather_daily') }}
where temperature_2m_min > temperature_2m_max
   or precipitation_sum < 0