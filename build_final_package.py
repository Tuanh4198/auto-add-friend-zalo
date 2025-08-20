# Script build gói final với Tesseract installer đi kèm
import os
import subprocess
import sys
import shutil
from datetime import datetime

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    print("📦 Đang cài đặt các thư viện cần thiết...")
    
    # Tạo file requirements.txt nếu chưa có
    requirements_content = """pyautogui==0.9.54
pynput==1.7.6
pytesseract==0.3.10
Pillow==10.0.1
opencv-python==4.8.1.78
numpy==1.24.3
pyinstaller==6.1.0
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Đã cài đặt xong các thư viện!")

def build_exe():
    """Build file exe với PyInstaller"""
    print("🔨 Đang build file exe...")
    
    # Lệnh PyInstaller với các tùy chọn tối ưu
    cmd = [
        "pyinstaller",
        "--onefile",  # Tạo 1 file exe duy nhất
        "--name=AutoClickTool",  # Tên file exe
        "--add-data=input.csv;.",  # Thêm file CSV vào exe
        "--add-data=message.txt;.",  # Thêm file message vào exe
        "--hidden-import=pynput.keyboard._win32",  # Import ẩn cho Windows
        "--hidden-import=pynput.mouse._win32",
        "--hidden-import=cv2",
        "--hidden-import=PIL",
        "--hidden-import=pytesseract",
        "--hidden-import=numpy",
        "--hidden-import=pyautogui",
        "--hidden-import=pynput",
        "--collect-all=pytesseract",  # Thu thập tất cả pytesseract
        "--collect-all=PIL",  # Thu thập tất cả PIL
        "--collect-all=cv2",  # Thu thập tất cả cv2
        "--collect-all=numpy",  # Thu thập tất cả numpy
        "--collect-all=pyautogui",  # Thu thập tất cả pyautogui
        "--collect-all=pynput",  # Thu thập tất cả pynput
        "--exclude-module=matplotlib",  # Loại trừ matplotlib để giảm kích thước
        "--exclude-module=scipy",
        "--exclude-module=pandas",
        "--exclude-module=tkinter",
        "--exclude-module=PyQt5",
        "--exclude-module=PySide2",
        "click_auto.py"
    ]
    
    # Thêm Tesseract portable nếu có
    if os.path.exists("tesseract-portable"):
        cmd.extend(["--add-data=tesseract-portable;tesseract-portable"])
        print("✅ Đã thêm Tesseract portable vào exe")
    
    try:
        subprocess.check_call(cmd)
        print("✅ Build thành công! File exe nằm trong thư mục dist/")
        print("📁 Đường dẫn: dist/AutoClickTool.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi build: {e}")
        return False

def create_final_files():
    """Tạo các file cần thiết cho gói final"""
    print("📝 Đang tạo các file cần thiết...")
    
    # File chạy tool với hướng dẫn
    run_tool_content = """@echo off
chcp 65001 >nul
echo ========================================
echo    Auto Click Tool - Zalo Add Friend
echo ========================================
echo.
echo 🚀 Chương trình sẽ bắt đầu trong 5 giây...
echo ⚠️  Lưu ý:
echo    - Đảm bảo Zalo đã mở và đăng nhập
echo    - Không di chuyển chuột trong quá trình chạy
echo    - Nhấn ESC để dừng chương trình
echo    - Có thể chỉnh sửa tin nhắn trong file message.txt
echo.
timeout /t 5 /nobreak >nul
echo.
echo 🎯 Bắt đầu chạy AutoClickTool...
echo.
AutoClickTool.exe
echo.
echo ✅ Chương trình đã kết thúc!
pause
"""
    
    with open("run_tool.bat", "w", encoding="utf-8") as f:
        f.write(run_tool_content)
    
    # File setup thủ công
    setup_manual_content = """@echo off
chcp 65001 >nul
echo ========================================
echo    Hướng dẫn cài đặt Tesseract thủ công
echo ========================================
echo.

echo 📋 Bước 1: Tải Tesseract OCR
echo 1. Truy cập: https://github.com/UB-Mannheim/tesseract/releases
echo 2. Tải file: tesseract-ocr-w64-setup-5.4.0.20240606.exe
echo 3. Cài đặt vào: C:\\Program Files\\Tesseract-OCR\\
echo.

echo 📋 Bước 2: Copy vào thư mục portable
echo 1. Copy file: C:\\Program Files\\Tesseract-OCR\\tesseract.exe
echo 2. Paste vào: tesseract-portable\\bin\\
echo 3. Copy thư mục: C:\\Program Files\\Tesseract-OCR\\tessdata
echo 4. Paste vào: tesseract-portable\\tessdata\\
echo.

echo 📋 Bước 3: Kiểm tra
echo 1. Kiểm tra file: tesseract-portable\\bin\\tesseract.exe
echo 2. Kiểm tra file: tesseract-portable\\tessdata\\eng.traineddata
echo.

echo 🎉 Hoàn tất! Bây giờ bạn có thể chạy AutoClickTool.exe
pause
"""
    
    with open("setup_tesseract_manual.bat", "w", encoding="utf-8") as f:
        f.write(setup_manual_content)
    
    # File hướng dẫn sử dụng
    guide_content = """# 🚀 Auto Click Tool - Zalo Add Friend

## 📋 Mô tả
Tool tự động thêm bạn bè trên Zalo bằng cách:
1. Tìm kiếm số điện thoại
2. Click vào kết quả tìm kiếm
3. Click nút "Add friend"
4. Nhập tin nhắn và gửi lời mời

## 🎯 Cách sử dụng

### Bước 1: Chuẩn bị
1. Mở Zalo và đăng nhập
2. Mở file `input.csv` và thêm số điện thoại vào cột A (1 số/dòng)
3. Chỉnh sửa file `message.txt` để tùy chỉnh nội dung tin nhắn
4. Chạy `setup_tesseract.bat` để cài đặt Tesseract OCR (nếu cần)

### Bước 2: Chạy tool
1. Double-click `run_tool.bat` hoặc `AutoClickTool.exe`
2. Làm theo hướng dẫn trên màn hình:
   - Click 5 vị trí theo thứ tự: Search → Result → Add Friend → Input Msg → Send
   - Nhấn ENTER để bắt đầu
   - Nhấn ESC để dừng

### Bước 3: Theo dõi
- Tool sẽ tự động xử lý từng số điện thoại
- Có thể dừng bất cứ lúc nào bằng ESC
- Kết quả được lưu trong file CSV

## 📝 Tùy chỉnh tin nhắn

Chỉnh sửa file `message.txt` để thay đổi nội dung tin nhắn gửi đi:
- Mở file `message.txt` bằng Notepad
- Thay đổi nội dung tin nhắn
- Lưu file và chạy lại tool

## ⚠️ Lưu ý quan trọng

### Yêu cầu hệ thống:
- Windows 10/11
- Độ phân giải màn hình 1920x1080 (khuyến nghị)
- Zalo đã cài đặt và đăng nhập

### Bảo mật:
- Tắt Windows Defender tạm thời nếu bị chặn
- Chạy với quyền Administrator nếu cần
- Không chia sẻ file exe với người khác

### Hiệu suất:
- Không di chuyển chuột trong quá trình chạy
- Đảm bảo Zalo không bị che khuất
- Tắt các ứng dụng không cần thiết

## 🛠️ Xử lý lỗi

### Lỗi thường gặp:
1. **"Không tìm thấy Tesseract"**: 
   - Chạy `setup_tesseract.bat` (tự động)
   - Hoặc chạy `setup_tesseract_manual.bat` (hướng dẫn thủ công)
2. **"File CSV không tồn tại"**: Tạo file `input.csv` với số điện thoại
3. **"Tool không click đúng vị trí"**: Lấy lại tọa độ với cùng độ phân giải màn hình
4. **"Windows Defender chặn"**: Thêm exception hoặc tắt tạm thời

### Hỗ trợ:
- Kiểm tra file `README.md` để biết thêm chi tiết
- Đảm bảo tất cả file trong cùng thư mục
- Chạy với quyền Administrator nếu cần

## 📞 Liên hệ
Nếu gặp vấn đề, vui lòng kiểm tra:
1. File log (nếu có)
2. Cấu hình hệ thống
3. Phiên bản Zalo

---
*Tool được tạo tự động - Sử dụng cẩn thận*
"""
    
    with open("HƯỚNG DẪN SỬ DỤNG.txt", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("✅ Đã tạo các file cần thiết!")

def create_final_package():
    """Tạo gói final hoàn chỉnh"""
    print("📦 Đang tạo gói final...")
    
    # Tên gói
    package_name = f"AutoClickTool_Final_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Tạo thư mục gói
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Copy các file cần thiết
    files_to_copy = [
        ("dist/AutoClickTool.exe", "AutoClickTool.exe"),
        ("input.csv", "input.csv"),
        ("message.txt", "message.txt"),
        ("run_tool.bat", "run_tool.bat"),
        ("setup_tesseract.bat", "setup_tesseract.bat"),
        ("setup_tesseract_manual.bat", "setup_tesseract_manual.bat"),
        ("HƯỚNG DẪN SỬ DỤNG.txt", "HƯỚNG DẪN SỬ DỤNG.txt"),
        ("tesseract-ocr-w64-setup-5.4.0.20240606.exe", "tesseract-ocr-w64-setup-5.4.0.20240606.exe")
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(package_name, dst))
            print(f"✅ Đã copy: {src} -> {dst}")
        else:
            print(f"⚠️  File không tồn tại: {src}")
    
    # Copy thư mục Tesseract portable nếu có
    if os.path.exists("tesseract-portable"):
        print("📁 Copy thư mục tesseract-portable...")
        shutil.copytree("tesseract-portable", os.path.join(package_name, "tesseract-portable"))
        print("✅ Đã copy Tesseract portable")
    
    # Tạo file README nhanh
    quick_start = f"""# 🚀 Auto Click Tool - Khởi động nhanh

## 🎯 Cách sử dụng nhanh:

### 1️⃣ Chuẩn bị
- Mở Zalo và đăng nhập
- Mở file `input.csv` → thêm số điện thoại vào cột A
- Chỉnh sửa file `message.txt` → thay đổi nội dung tin nhắn

### 2️⃣ Cài đặt Tesseract (nếu cần)
- Chạy `setup_tesseract.bat` (tự động - sử dụng file đi kèm)
- Hoặc chạy `setup_tesseract_manual.bat` (hướng dẫn thủ công)

### 3️⃣ Chạy tool
- Double-click: `run_tool.bat`
- Hoặc double-click: `AutoClickTool.exe`

### 4️⃣ Làm theo hướng dẫn
- Click 5 vị trí theo thứ tự
- Nhấn ENTER để bắt đầu
- Nhấn ESC để dừng

## ⚠️ Lưu ý:
- Tắt Windows Defender nếu bị chặn
- Chạy với quyền Administrator nếu cần
- Không di chuyển chuột khi tool đang chạy

## 📝 Tính năng mới:
- ✅ Đã bao gồm file Tesseract installer
- ✅ Tùy chỉnh tin nhắn qua file message.txt
- ✅ Setup tự động thông minh

## 📖 Xem thêm:
- `HƯỚNG DẪN SỬ DỤNG.txt` - Hướng dẫn chi tiết

---
*Gói được tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(os.path.join(package_name, "KHỞI ĐỘNG NHANH.txt"), "w", encoding="utf-8") as f:
        f.write(quick_start)
    
    print(f"\n🎉 Đã tạo gói final: {package_name}")
    return package_name

def main():
    print("🚀 Build gói Auto Click Tool Final")
    print("=" * 60)
    
    # Kiểm tra file cần thiết
    required_files = [
        "click_auto.py",
        "input.csv", 
        "message.txt",
        "setup_tesseract.bat",
        "tesseract-ocr-w64-setup-5.4.0.20240606.exe"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Thiếu các file sau:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nVui lòng đảm bảo tất cả file cần thiết đã có!")
        return
    
    # Bước 1: Cài đặt thư viện
    install_requirements()
    
    # Bước 2: Build exe
    if not build_exe():
        print("❌ Build thất bại!")
        return
    
    # Bước 3: Tạo file cần thiết
    create_final_files()
    
    # Bước 4: Tạo gói final
    package_name = create_final_package()
    
    print("\n" + "=" * 60)
    print("🎉 Build hoàn thành!")
    print(f"📁 Gói final: {package_name}")
    print("\n📋 Gói bao gồm:")
    print("   ✅ AutoClickTool.exe - File chính (standalone)")
    print("   ✅ input.csv - File dữ liệu số điện thoại")
    print("   ✅ message.txt - File nội dung tin nhắn (có thể chỉnh sửa)")
    print("   ✅ run_tool.bat - Script chạy với hướng dẫn")
    print("   ✅ setup_tesseract.bat - Script cài Tesseract (tự động)")
    print("   ✅ setup_tesseract_manual.bat - Script cài Tesseract (thủ công)")
    print("   ✅ tesseract-ocr-w64-setup-5.4.0.20240606.exe - Tesseract installer")
    print("   ✅ tesseract-portable/ - Tesseract portable")
    print("   ✅ HƯỚNG DẪN SỬ DỤNG.txt - Hướng dẫn chi tiết")
    print("   ✅ KHỞI ĐỘNG NHANH.txt - Hướng dẫn nhanh")
    print("\n🎯 Cách sử dụng trên máy khác:")
    print("   1. Copy thư mục gói sang máy đích")
    print("   2. Chạy setup_tesseract.bat để cài Tesseract")
    print("   3. Chỉnh sửa message.txt để tùy chỉnh tin nhắn")
    print("   4. Double-click run_tool.bat")
    print("   5. Làm theo hướng dẫn trên màn hình")
    print("\n💡 Ưu điểm của gói final:")
    print("   - Không cần cài Python")
    print("   - Không cần cài thư viện")
    print("   - Bao gồm Tesseract installer")
    print("   - Tùy chỉnh tin nhắn dễ dàng")
    print("   - Setup tự động thông minh")
    print("   - Chạy được ngay trên mọi máy Windows")

if __name__ == "__main__":
    main()
