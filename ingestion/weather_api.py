import requests
import yaml
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"
CITIES_FILE = "/opt/airflow/config/cities.yml"


def load_cities():
    with open(CITIES_FILE, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config["cities"]


def fetch_daily(logical_date):
    session = requests.Session()

    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )

    session.mount("https://", HTTPAdapter(max_retries=retry))

    rows = []

    for city in load_cities():
        params = {
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "start_date": logical_date,
            "end_date": logical_date,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "UTC",
        }

        response = session.get(
            BASE_URL,
            params=params,
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        daily = data["daily"]

        rows.append(
            {
                "date": daily["time"][0],
                "city": city["name"],
                "latitude": city["latitude"],
                "longitude": city["longitude"],
                "temperature_2m_max": daily["temperature_2m_max"][0],
                "temperature_2m_min": daily["temperature_2m_min"][0],
                "precipitation_sum": daily["precipitation_sum"][0],
            }
        )

    return rows
