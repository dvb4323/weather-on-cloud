import os
import boto3

BUCKET_NAME = 'weather-data-time'

def upload_to_s3(data_directory):
    s3 = boto3.client('s3')

    for city in os.listdir(data_directory):
        city_folder = os.path.join(data_directory, city)
        if os.path.isdir(city_folder):  # Kiểm tra nếu là folder
            for filename in os.listdir(city_folder):
                local_path = os.path.join(city_folder, filename)
                s3_key = f"{city}/{filename}"  # Tạo key theo cấu trúc folder
                s3.upload_file(local_path, BUCKET_NAME, s3_key)
                print(f"Uploaded {s3_key} to S3 bucket {BUCKET_NAME}")

if __name__ == "__main__":
    # # Xác định đường dẫn đến thư mục 'data' bên ngoài thư mục 'src'
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Thư mục cha của 'src'
    # DATA_DIR = os.path.join(BASE_DIR, "data")
    DATA_DIR = "../data/output"
    upload_to_s3(DATA_DIR)
