select
    date,
    city
from {{ ref('stg_weather_daily') }}
group by date, city
having count(*) > 1