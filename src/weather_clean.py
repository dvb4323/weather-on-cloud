import json
import os

# Thư mục dữ liệu đầu vào và đầu ra
input_dir = "../data"
output_dir = "../data/output"


# Hàm chuyển đổi nhiệt độ từ Kelvin sang Celsius
def kelvin_to_celsius(temp_k):
    return round(temp_k - 273.15, 2)


# Hàm trích xuất các trường cần thiết
def extract_relevant_fields(data):
    return {
        "timestamp": data["dt"],
        "temperature": kelvin_to_celsius(data["main"].get("temp")),
        "pressure": data["main"].get("pressure"),
        "humidity": data["main"].get("humidity"),
        "wind": data["wind"].get("speed"),
        "clouds": data["clouds"].get("all"),
        "weather": data["weather"][0].get("main") if data.get("weather") else None,
    }


# Hàm xử lý một file JSON
def process_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Lấy timestamp đầu tiên
    if "list" in data and len(data["list"]) > 0:
        input_data = data["list"][0]
        cleaned_data = extract_relevant_fields(input_data)

        # Đảm bảo thư mục đích tồn tại
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Ghi dữ liệu làm sạch vào file mới
        with open(output_path, "w", encoding="utf-8") as output_file:
            json.dump(cleaned_data, output_file, indent=4, ensure_ascii=False)
        print(f"Processed: {input_path} -> {output_path}")
    else:
        print(f"Skipped (invalid or empty): {input_path}")


# Lặp qua tất cả các file JSON trong thư mục đầu vào
for root, _, files in os.walk(input_dir):
    for file_name in files:
        if file_name.endswith(".json"):
            input_path = os.path.join(root, file_name)

            # Xác định đường dẫn output tương ứng
            relative_path = os.path.relpath(input_path, input_dir)
            output_path = os.path.join(output_dir, relative_path)

            # Xử lý file
            process_file(input_path, output_path)

print("Hoàn thành xử lý tất cả các file JSON.")
