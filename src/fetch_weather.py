import os
import requests
import json
from datetime import datetime

# API Configurations
API_KEY = '13df5659e9e4ff7ecadd465d4615d99c'
CITY = 'Hanoi'
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"

# Xác định đường dẫn đến thư mục 'data' bên ngoài thư mục 'src'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Thư mục cha của 'src'
DATA_DIR = os.path.join(BASE_DIR, "data")

# Tạo thư mục 'data' nếu chưa tồn tại
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def save_to_file(data):
    # Đặt tên file theo timestamp
    filename = f"weather_{data['timestamp'].replace(':', '-')}.json"
    file_path = os.path.join(DATA_DIR, filename)  # Đường dẫn đầy đủ

    # Ghi dữ liệu vào file JSON
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Data saved to {file_path}")


def fetch_weather_data():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"] - 273.15,  # Convert Kelvin to Celsius
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H-%M-%S")  # Use "-" for filename compatibility
        }
        save_to_file(weather)
        return weather
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None


if __name__ == "__main__":
    fetch_weather_data()
