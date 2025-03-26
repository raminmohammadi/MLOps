from flask import Flask
from google.cloud import storage, bigquery
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello from the intermediate lab!"

@app.route('/upload')
def upload_file():
    # Initialize Cloud Storage client
    storage_client = storage.Client()
    bucket_name = os.environ.get('BUCKET_NAME')
    if not bucket_name:
        return 'BUCKET_NAME environment variable is not set.', 500
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('hello.txt')
    blob.upload_from_string('Hello, Cloud Storage!')
    return f'File uploaded to {bucket_name}.'

@app.route('/query')
def query_bigquery():
    # Initialize BigQuery client
    client = bigquery.Client()
    query = """
        SELECT name, SUM(number) as total
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE state = 'TX'
        GROUP BY name
        ORDER BY total DESC
        LIMIT 10
    """
    query_job = client.query(query)
    results = query_job.result()
    names = [row.name for row in results]
    return f'Top names in Texas: {", ".join(names)}'

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)  # Flask
    # uvicorn app:app --host 0.0.0.0 --port $PORT  # FastAPI