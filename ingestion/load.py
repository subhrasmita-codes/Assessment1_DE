import os
import psycopg2


def load_daily(logical_date, rows):
    """
    Idempotently load one logical date into raw.weather_daily.
    Re-running the same date replaces the existing rows for that date.
    """

    conn = psycopg2.connect(
        host=os.environ["WAREHOUSE_HOST"],
        port=os.environ["WAREHOUSE_PORT"],
        dbname=os.environ["WAREHOUSE_DB"],
        user=os.environ["WAREHOUSE_USER"],
        password=os.environ["WAREHOUSE_PASSWORD"],
    )

    try:
        with conn:
            with conn.cursor() as cur:

                # Remove existing rows for this logical date.
                cur.execute(
                    """
                    DELETE FROM raw.weather_daily
                    WHERE date = %s
                    """,
                    (logical_date,),
                )

                # Insert the fresh API rows.
                for row in rows:
                    cur.execute(
                        """
                        INSERT INTO raw.weather_daily (
                            date,
                            city,
                            latitude,
                            longitude,
                            temperature_2m_max,
                            temperature_2m_min,
                            precipitation_sum
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            row["date"],
                            row["city"],
                            row["latitude"],
                            row["longitude"],
                            row["temperature_2m_max"],
                            row["temperature_2m_min"],
                            row["precipitation_sum"],
                        ),
                    )
    finally:
        conn.close()