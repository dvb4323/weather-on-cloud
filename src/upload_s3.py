import boto3
import json
import os

BUCKET_NAME = 'weather-data-storage-bi'


def upload_files_to_s3(data_directory):
    s3 = boto3.client('s3')

    for filename in os.listdir(data_directory):
        if filename.endswith(('.json', '.csv', '.txt')):  # Adjust file extensions as needed
            local_file_path = os.path.join(data_directory, filename)
            s3.upload_file(local_file_path, BUCKET_NAME, filename)
            print(f"Uploaded {filename} to S3 bucket {BUCKET_NAME}")


if __name__ == "__main__":
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Get the parent directory of the script's directory
    project_root = os.path.dirname(script_dir)

    # Construct the path to the data directory
    data_directory = os.path.join(project_root, 'data')

    upload_files_to_s3(data_directory)
