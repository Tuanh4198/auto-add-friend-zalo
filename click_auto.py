# cmd run: python click_auto.py

print("Script bắt đầu chạy")

import pyautogui
import csv
from pynput import mouse, keyboard
import time
import os
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Đường dẫn đến Tesseract (tự động tìm)
def setup_tesseract_path():
    """Tự động tìm đường dẫn Tesseract"""
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',  # Cài đặt thông thường
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',  # 32-bit
        './tesseract-portable/bin/tesseract.exe',  # Portable version
        './tesseract/bin/tesseract.exe',  # Portable version khác
        os.path.join(os.path.dirname(__file__), 'tesseract-portable', 'bin', 'tesseract.exe'),  # Relative path
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"✅ Tìm thấy Tesseract tại: {path}")
            return path
    
    print("⚠️  Không tìm thấy Tesseract, sử dụng đường dẫn mặc định")
    return r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Thiết lập đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = setup_tesseract_path()

csv_path = "input.csv"
message_path = "message.txt"
click_positions = []
stop_flag = False  # Cờ dừng chương trình
start_flag = False  # Cờ bắt đầu chương trình

# Nếu file CSV chưa tồn tại → tạo mới với header
if not os.path.exists(csv_path):
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Data", "Search", "Result", "AddFriend1", "InputMsg", "SendFriend"])

# Nếu file message.txt chưa tồn tại → tạo mới
if not os.path.exists(message_path):
    with open(message_path, "w", encoding="utf-8") as f:
        f.write("Xin chào! Tôi tìm thấy bạn qua tìm kiếm và muốn kết bạn. Hy vọng chúng ta có thể trò chuyện và tìm hiểu nhau hơn!")

def load_message():
    """Đọc nội dung tin nhắn từ file message.txt"""
    try:
        with open(message_path, "r", encoding="utf-8") as f:
            message = f.read().strip()
            if message:
                print(f"✅ Đã đọc tin nhắn từ {message_path}: {message[:50]}...")
                return message
            else:
                print("⚠️  File message.txt trống, sử dụng tin nhắn mặc định")
                return "hello"
    except Exception as e:
        print(f"⚠️  Lỗi khi đọc file message.txt: {e}")
        print("⚠️  Sử dụng tin nhắn mặc định")
        return "hello"

# === Lấy tọa độ click chuột ===
def on_click(x, y, button, pressed):
    if pressed:
        click_positions.append((x, y))
        print(f"📌 Đã lấy tọa độ {len(click_positions)}/5: {x}, {y}")
        if len(click_positions) >= 5:
            print("✅ Đã đủ 5 tọa độ!")
            return False  # Đủ 5 tọa độ thì dừng listener

# === Lắng nghe phím ===
def on_press(key):
    global stop_flag, start_flag
    try:
        if key == keyboard.Key.esc:
            stop_flag = True
            print("🛑 Đã nhấn ESC → Dừng chương trình.")
            return False  # Dừng listener ngay lập tức
        elif key == keyboard.Key.enter:
            start_flag = True
            print("🚀 Đã nhấn ENTER → Bắt đầu chương trình.")
            return False  # Dừng listener ngay lập tức
    except AttributeError:
        pass

# === Lấy tọa độ và lưu vào CSV ===
def get_positions():
    global click_positions
    click_positions = []  # Reset positions
    
    print("👉 Hãy click 5 lần theo thứ tự:")
    print("1. Ô Search")
    print("2. Giá trị Search (kết quả lọc)")
    print("3. Nút Add Friend")
    print("4. Click Input Msg")
    print("5. Nút Request Add Friend")
    
    # Sử dụng listener với timeout để tránh treo
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    
    # Chờ cho đến khi đủ 5 tọa độ hoặc timeout
    timeout = 60  # 60 giây timeout
    start_time = time.time()
    
    while len(click_positions) < 5:
        if time.time() - start_time > timeout:
            print("⚠ Hết thời gian chờ! Vui lòng thử lại.")
            listener.stop()
            return False
        time.sleep(0.1)
    
    listener.stop()

    if len(click_positions) != 5:
        print("⚠ Không đủ 5 tọa độ!")
        return False

    try:
        # Đọc CSV hiện tại để giữ lại số điện thoại
        existing_rows = []
        if os.path.exists(csv_path):
            with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
                existing_rows = list(csv.reader(f))
        
        # Tạo dòng mới với tọa độ
        coordinates_row = [""]  # Cột A để trống
        coordinates_row.append(f"{click_positions[0][0]},{click_positions[0][1]}")  # Search
        coordinates_row.append(f"{click_positions[1][0]},{click_positions[1][1]}")  # Result
        coordinates_row.append(f"{click_positions[2][0]},{click_positions[2][1]}")  # AddFriend1
        coordinates_row.append(f"{click_positions[3][0]},{click_positions[3][1]}")  # InputMsg
        coordinates_row.append(f"{click_positions[4][0]},{click_positions[4][1]}")  # SendFriend
        
        # Ghi lại CSV với tọa độ ở dòng cuối
        with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Ghi lại tất cả dòng số điện thoại
            for row in existing_rows:
                if row and row[0].strip():  # Chỉ ghi dòng có số điện thoại
                    writer.writerow(row)
            
            # Ghi dòng tọa độ ở cuối
            writer.writerow(coordinates_row)
            
    except Exception as e:
        print(f"⚠ Lỗi khi lưu tọa độ vào CSV: {e}")
        return False

    print("✅ Đã lưu tọa độ vào CSV.")
    print("👉 Nhấn ENTER để bắt đầu chương trình, hoặc ESC để thoát.")
    return True

# === Hàm đọc văn bản từ vùng màn hình ===
def read_text_from_screen(x, y, width=150, height=60):
    try:
        # Chụp ảnh vùng màn hình, căn giữa quanh (x, y)
        screenshot = pyautogui.screenshot(region=(x - width // 2, y - height // 2, width, height))
        # Chuyển đổi sang định dạng OpenCV
        image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        # Chuyển sang grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Tăng độ tương phản
        alpha = 1.5  # Độ tương phản
        beta = 10    # Độ sáng
        adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
        # Áp dụng ngưỡng để cải thiện OCR
        thresh = cv2.threshold(adjusted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        # Trích xuất văn bản
        text = pytesseract.image_to_string(thresh, config='--psm 6').strip()
        return text
    except Exception as e:
        print(f"⚠ Lỗi khi đọc văn bản: {e}")
        return ""

# === Auto nhập dữ liệu ===
def auto_input():
    global stop_flag

    # Đọc toàn bộ file CSV
    with open(csv_path, mode="r", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    if len(rows) < 2:
        print("⚠ CSV không có dữ liệu để chạy.")
        return

    # Lấy tọa độ từ dòng cuối cùng (dòng chứa tọa độ)
    coordinates_row = None
    for row in reversed(rows):
        if row and len(row) >= 5 and row[0] == "":  # Dòng có cột A trống và có đủ 5 cột tọa độ
            coordinates_row = row
            break
    
    if coordinates_row:
        try:
            search_x, search_y = map(int, coordinates_row[1].split(","))
            result_x, result_y = map(int, coordinates_row[2].split(","))
            addfriend1_x, addfriend1_y = map(int, coordinates_row[3].split(","))
            inputmsg_x, inputmsg_y = map(int, coordinates_row[4].split(","))
            sendfriend_x, sendfriend_y = map(int, coordinates_row[5].split(","))
        except (ValueError, IndexError):
            print("⚠ Không thể đọc tọa độ từ CSV. Vui lòng lấy lại tọa độ.")
            return
    else:
        print("⚠ CSV không có tọa độ. Vui lòng lấy lại tọa độ.")
        return

    # Lấy danh sách số điện thoại từ cột A (bỏ qua dòng header nếu có)
    phone_numbers = []
    for i, row in enumerate(rows):
        if i == 0:  # Bỏ qua dòng header nếu có
            continue
        if row and row[0].strip():  # Kiểm tra cột A có dữ liệu
            phone = row[0].strip()
            if phone.isdigit() and len(phone) >= 10:  # Kiểm tra là số điện thoại hợp lệ
                phone_numbers.append(phone)

    if not phone_numbers:
        print("⚠ Không tìm thấy số điện thoại nào trong cột A của CSV.")
        return

    # Đọc nội dung tin nhắn từ file
    message_content = load_message()

    print(f"📱 Tìm thấy {len(phone_numbers)} số điện thoại trong CSV")
    print(f"💬 Tin nhắn sẽ gửi: {message_content}")
    print("🚀 Bắt đầu nhập dữ liệu... (Nhấn ESC để dừng)")
    
    # Bắt đầu listener cho ESC trong quá trình auto_input
    esc_listener = keyboard.Listener(on_press=on_press)
    esc_listener.start()
    
    current_index = 0
    
    while not stop_flag:
        try:
            # Kiểm tra ESC trước mỗi vòng lặp
            if stop_flag:
                print("🛑 Đã nhấn ESC → Dừng chương trình.")
                break
                
            phone = phone_numbers[current_index % len(phone_numbers)]
            print(f"\n📱 Đang xử lý số điện thoại: {phone}")
            
            # Step 1: Click ô search
            print("Step 1: Click ô search")
            pyautogui.click(search_x, search_y)
            time.sleep(1)
            
            # Step 2: Nhập số điện thoại và chờ 3 giây
            print("Step 2: Nhập số điện thoại")
            pyautogui.write(phone)
            time.sleep(3)
            
            # Kiểm tra ESC sau step 2
            if stop_flag:
                print("🛑 Đã nhấn ESC → Dừng chương trình.")
                break
            
            # Step 3: Click vào giá trị lọc ra
            print("Step 3: Click vào giá trị lọc ra")
            pyautogui.click(result_x, result_y)
            time.sleep(1)
            
            # Step 4: Kiểm tra text trước khi click nút add friend
            print("Step 4: Kiểm tra text 'Add friend'")
            button_text = read_text_from_screen(addfriend1_x, addfriend1_y)
            print(f"Text đọc được: '{button_text}'")
            
            if "Add friend" in button_text or "add friend" in button_text.lower():
                print("✅ Text đúng, tiếp tục...")
                pyautogui.click(addfriend1_x, addfriend1_y)
                time.sleep(1)
                
                # Kiểm tra ESC sau step 4
                if stop_flag:
                    print("🛑 Đã nhấn ESC → Dừng chương trình.")
                    break
                
                # Step 5: Click vào input message và xóa hết
                print("Step 5: Click input message và xóa")
                pyautogui.click(inputmsg_x, inputmsg_y)
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'a')  # Select all
                time.sleep(0.5)
                pyautogui.press('backspace')  # Delete
                time.sleep(0.5)
                
                # Step 6: Nhập text từ file message.txt
                print(f"Step 6: Nhập tin nhắn: {message_content}")
                pyautogui.write(message_content)
                time.sleep(0.5)
                
                # Step 7: Click add friend và chờ 3 giây
                print("Step 7: Click add friend")
                pyautogui.click(sendfriend_x, sendfriend_y)
                time.sleep(3)
                
                print("✅ Hoàn thành vòng lặp!")
            else:
                print("❌ Text không đúng 'Add friend', bỏ qua và sang vòng tiếp theo")
            
            # Step 8: Bắt đầu vòng lặp mới
            current_index += 1
            print(f"🔄 Bắt đầu vòng lặp tiếp theo ({current_index})...")
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠ Lỗi trong quá trình xử lý: {e}")
            time.sleep(2)
            continue
    
    # Dừng listener khi kết thúc
    esc_listener.stop()

# === Main function ===
def main():
    global stop_flag, start_flag
    
    print("🤖 Chương trình Auto Click")
    print("=" * 50)
    
    # Lấy tọa độ
    if not get_positions():
        print("❌ Không thể lấy tọa độ. Thoát chương trình.")
        return
    
    # Lắng nghe phím để bắt đầu hoặc dừng
    print("⌨️  Đang chờ nhấn phím...")
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()
    
    # Chờ cho đến khi nhấn phím hoặc timeout
    timeout = 300  # 5 phút timeout
    start_time = time.time()
    
    while not start_flag and not stop_flag:
        if time.time() - start_time > timeout:
            print("⚠ Hết thời gian chờ! Thoát chương trình.")
            keyboard_listener.stop()
            return
        time.sleep(0.1)
    
    keyboard_listener.stop()
    
    if stop_flag:
        print("👋 Thoát chương trình.")
        return
    
    # Bắt đầu auto input
    auto_input()
    
    print("👋 Chương trình kết thúc.")

if __name__ == "__main__":
    main()
