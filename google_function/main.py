import base64
from google.cloud import storage
from datetime import datetime
import json

def hello_pubsub(event, context):
     storage_client = storage.Client()
     bucket = storage_client.get_bucket('solar_storage')

     pubsub_message = base64.b64decode(event['data']).decode('utf-8')
     output_dict = {**event['attributes'],**eval(pubsub_message)}
     print(pubsub_message)
     print(event['attributes'])
     date_str = event['attributes']['published_at']
     print(date_str)
     # Check if file exists:
     file_name = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y/%m/%d/data.txt')
     blob = bucket.get_blob(file_name)
     file_exists = storage.Blob(bucket=bucket, name=file_name).exists(storage_client)
     if not file_exists: 
          print('file does not exist')
          new_file = bucket.blob(file_name)
          new_file.upload_from_string(json.dumps(output_dict))
     else:
          blob = bucket.get_blob(file_name)
          target_blob = bucket.blob(file_name)
          local_tmp_path = '/tmp/tmp.txt'
          # append
          with open(local_tmp_path, 'w') as f:
               f.write(blob.download_as_text() + ',' + json.dumps(output_dict))

          with open(local_tmp_path, 'r') as f:
               target_blob.upload_from_file(f)
          print('file exist')
          
     print(datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y/%m/%d/data.txt'))
     print({**event['attributes'],**eval(pubsub_message)})

# Function dependencies, for example:
# package>=version
google-cloud-storage