from google.cloud import bigquery
from flask import Flask
import os

app = Flask(__name__)

client = bigquery.Client(project="mlops-dev-513820")

table_id = "mlops-dev-513820.test_schema.us_states"

uri = "gs://mlops-dev-513820-data/us-states.csv"


@app.route("/")
def main():
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        schema=[
            bigquery.SchemaField("name", "STRING"),
            bigquery.SchemaField("post_abbr", "STRING"),
        ],
    )

    load_job = client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )
    load_job.result()

    destination_table = client.get_table(table_id)

    return {
        "message": "CSV loaded successfully",
        "table": table_id,
        "rows": destination_table.num_rows,
    }


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
    )
