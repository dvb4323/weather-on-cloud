import os
import requests
import json
from datetime import datetime, timedelta

# API Configuration
API_KEY = "6d41a14862d158fcf2383bfd4af59179"

# Xác định đường dẫn đến thư mục 'data' bên ngoài thư mục 'src'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Thư mục cha của 'src'
DATA_DIR = os.path.join(BASE_DIR, "data")

# Tạo thư mục 'data' nếu chưa tồn tại
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def read_cities_from_file(file_path):
    """Đọc danh sách thành phố từ file."""
    with open(file_path, "r") as file:
        cities = [line.strip() for line in file.readlines()]
    return cities


def get_dates_last_year():
    """Tạo danh sách các ngày trong vòng 1 năm qua."""
    today = datetime.now()
    dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(365)]
    return dates


def fetch_historical_weather(city, start, end):
    """Gửi yêu cầu tới API để lấy dữ liệu thời tiết lịch sử."""
    url = f"http://history.openweathermap.org/data/2.5/history/city?q={city}&type=hour&start={start}&end={end}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {city} from {start} to {end}: {response.status_code}")
        return None


def save_to_file(city, date, data):
    """Lưu dữ liệu vào file JSON."""
    city_name = city.replace(" ", "_")
    city_folder = os.path.join(DATA_DIR, city_name)

    # Tạo folder riêng cho từng thành phố
    if not os.path.exists(city_folder):
        os.makedirs(city_folder)

    filename = f"weather_{city_name}_{date}.json"
    file_path = os.path.join(city_folder, filename)

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    print(f"Data saved: {file_path}")


if __name__ == "__main__":
    # Đọc danh sách thành phố từ file
    cities_file = os.path.join(BASE_DIR, "cities_En.txt")
    cities = read_cities_from_file(cities_file)

    # Lấy danh sách các ngày trong vòng 1 năm
    dates = get_dates_last_year()

    for city in cities:
        for date in dates:
            # Tạo timestamps cho ngày
            start = int(datetime.strptime(date, "%Y-%m-%d").timestamp())
            end = start + 86400  # Cộng 1 ngày (86400 giây)

            # Lấy dữ liệu từ API
            data = fetch_historical_weather(city, start, end)
            if data:
                save_to_file(city, date, data)
