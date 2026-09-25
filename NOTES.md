# Notes

## Time spent

Approximately 5–6 hours including environment setup, ingestion development, dbt modeling and testing, Airflow orchestration, notebook walkthrough, debugging, and reproducibility testing.

## AI tools used

AI assistance was used for lookup, troubleshooting, debugging, and reviewing implementation details during development. It was also used to help understand Docker, Airflow, dbt, Python ingestion, notebook execution, and data-quality testing.

The final implementation was tested locally using Docker Compose, PostgreSQL, Airflow, dbt, and Jupyter. The pipeline and notebook were executed successfully in the local environment.

## Known gaps

- The current pipeline is designed for a small number of configured cities and a single daily weather record per city.
- Production deployment would require secure secret management, stronger monitoring and alerting, and more extensive data-quality and freshness checks.
- The current loading strategy is designed for this assessment; a production implementation could use incremental/upsert loading and warehouse-specific partitioning or clustering.