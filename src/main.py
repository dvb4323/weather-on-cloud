from fetch_weather import fetch_weather_data
from upload_s3 import upload_files_to_s3
import os

if __name__ == "__main__":
    # Fetch and save weather data
    weather_data = fetch_weather_data()

    if weather_data:
        print("Weather data fetched and saved successfully.")

        # Determine the data directory path
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of this script
        project_root = os.path.dirname(script_dir)  # Parent directory of 'src'
        data_directory = os.path.join(project_root, 'data')  # Path to 'data' directory

        # Upload saved data files to S3
        print("Starting upload to S3...")
        upload_files_to_s3(data_directory)
    else:
        print("Failed to fetch weather data. No upload performed.")
