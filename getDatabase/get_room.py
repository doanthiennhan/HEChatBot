import os
import requests
import json
from dotenv import load_dotenv

# Load biến môi trường từ tệp .env
load_dotenv()

def get_room_type():
    # Lấy URL từ biến môi trường
    api_url = os.getenv("API_URL") + "/room_type"
    
    # In ra URL để kiểm tra
    print(f"URL API: {api_url}")
    
    if not api_url:
        return {"error": "Không tìm thấy URL của API."}

    # Gửi yêu cầu GET đến API
    response = requests.get(api_url)
    
    # In ra mã trạng thái của response
    print(f"Response status code: {response.status_code}")
    
    if response.status_code == 200:
        # Nếu API trả về dữ liệu thành công, trả về kết quả JSON
        return response.json()["result"]
    else:
        # In ra nội dung response nếu có lỗi
        print(f"Response content: {response.content}")
        return {"error": "Không thể lấy thông tin giá vé từ API."}

def get_room():
    # Lấy URL từ biến môi trường
    api_url = os.getenv("API_URL") + "/room"
    
    # In ra URL để kiểm tra
    print(f"URL API: {api_url}")
    
    if not api_url:
        return {"error": "Không tìm thấy URL của API."}

    # Gửi yêu cầu GET đến API
    response = requests.get(api_url)
    
    # In ra mã trạng thái của response
    print(f"Response status code: {response.status_code}")
    
    if response.status_code == 200:
        # Nếu API trả về dữ liệu thành công, trả về kết quả JSON
        return response.json()["result"]
    else:
        # In ra nội dung response nếu có lỗi
        print(f"Response content: {response.content}")
        return {"error": "Không thể lấy thông tin giá vé từ API."}


def get_empty_room():
    api_url = os.getenv("API_URL") + "/room/findByRoomType/entity"
    
     # In ra URL để kiểm tra
    print(f"URL API: {api_url}")
    
    if not api_url:
        return {"error": "Không tìm thấy URL của API."}

    # Gửi yêu cầu GET đến API
    response = requests.get(api_url)
    
    # In ra mã trạng thái của response
    print(f"Response status code: {response.status_code}")
    
    if response.status_code == 200:
        # Nếu API trả về dữ liệu thành công, trả về kết quả JSON
        return response.json()["result"]
    else:
        # In ra nội dung response nếu có lỗi
        print(f"Response content: {response.content}")
        return {"error": "Không thể lấy thông tin giá vé từ API."}


if __name__ == "__main__":
   data = get_room_type()
   for room in data:
       print(room["name"])