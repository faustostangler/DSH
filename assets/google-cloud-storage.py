import pandas as pd
from google.cloud import storage
from io import BytesIO

import helper as b3

def upload_to_gcs(df, file_name):
    # GCS configuration
    destination_blob_name = f'{file_name}.zip'

    # Initialize GCS client
    client = storage.Client.from_service_account_json(b3.json_key_file)
    bucket = client.get_bucket(b3.bucket_name)

    # Save DataFrame to a bytes buffer as a zipped pickle file
    buffer = BytesIO()
    df.to_pickle(buffer, compression='zip')
    buffer.seek(0)

    # Upload the buffer to GCS
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(buffer, content_type='application/zip')

    return df

def download_from_gcs(file_name):
    # GCS configuration
    source_blob_name = f'{file_name}.zip'

    # Initialize GCS client
    client = storage.Client.from_service_account_json(b3.json_key_file)
    bucket = client.get_bucket(b3.bucket_name)

    # Download the zipped DataFrame from GCS to a bytes buffer
    buffer = BytesIO()
    blob = bucket.blob(source_blob_name)
    blob.download_to_file(buffer)
    buffer.seek(0)

    # Load the zipped DataFrame into a Pandas DataFrame
    df = pd.read_pickle(buffer, compression='zip')
    return df

file_name = 'b3_companies'
b3_companies = b3.run.read_or_create_dataframe(file_name, b3.cols_nsd)


b3_companies = upload_to_gcs(b3_companies, file_name)

b3_companies = download_from_gcs(file_name)

print(b3_companies)

print('done')