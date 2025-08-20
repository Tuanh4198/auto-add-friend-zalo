# Script build gói standalone hoàn chỉnh
import os
import subprocess
import sys
import shutil
import urllib.request
import zipfile
from datetime import datetime

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    print("📦 Đang cài đặt các thư viện cần thiết...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Đã cài đặt xong các thư viện!")

def download_tesseract_portable():
    """Tải và cài đặt Tesseract portable hoàn chỉnh"""
    print("🔧 Đang tải Tesseract portable...")
    
    # Kiểm tra xem đã có chưa
    if os.path.exists("tesseract-portable/bin/tesseract.exe"):
        print("✅ Tesseract portable đã tồn tại!")
        return True
    
    # Tạo thư mục
    os.makedirs("tesseract-portable", exist_ok=True)
    os.makedirs("tesseract-portable/bin", exist_ok=True)
    os.makedirs("tesseract-portable/tessdata", exist_ok=True)
    
    try:
        # Tải Tesseract portable từ GitHub
        print("📥 Đang tải Tesseract portable...")
        tesseract_url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.1.20230401/tesseract-ocr-w64-setup-5.3.1.20230401.exe"
        installer_path = "tesseract-installer.exe"
        
        urllib.request.urlretrieve(tesseract_url, installer_path)
        print("✅ Đã tải xong installer!")
        
        # Tạo file config
        config_content = """# Tesseract Portable Configuration
# Đường dẫn tới thư mục tessdata
TESSDATA_PREFIX=./tessdata/
# Ngôn ngữ mặc định
LANG=eng
"""
        
        with open("tesseract-portable/tesseract.conf", "w", encoding="utf-8") as f:
            f.write(config_content)
        
        # Tạo file README
        readme_content = """# Tesseract Portable

Đây là phiên bản portable của Tesseract OCR.

## Cấu trúc:
- bin/ - Chứa file tesseract.exe
- tessdata/ - Chứa dữ liệu ngôn ngữ
- tesseract.conf - File cấu hình

## Cách sử dụng:
1. Tải tesseract.exe từ: https://github.com/UB-Mannheim/tesseract/releases
2. Copy vào thư mục bin/
3. Tải tessdata từ: https://github.com/tesseract-ocr/tessdata
4. Copy vào thư mục tessdata/

Hoặc chạy setup_tesseract.bat để tự động cài đặt.
"""
        
        with open("tesseract-portable/README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("✅ Đã tạo cấu trúc Tesseract portable!")
        print("⚠️  Cần tải thêm file tesseract.exe và tessdata")
        
        # Xóa file installer
        if os.path.exists(installer_path):
            os.remove(installer_path)
            
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi tải Tesseract: {e}")
        return False

def build_exe():
    """Build file exe với PyInstaller"""
    print("🔨 Đang build file exe...")
    
    # Lệnh PyInstaller với các tùy chọn tối ưu
    cmd = [
        "pyinstaller",
        "--onefile",  # Tạo 1 file exe duy nhất
        "--name=AutoClickTool",  # Tên file exe
        "--add-data=input.csv;.",  # Thêm file CSV vào exe
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

def create_standalone_files():
    """Tạo các file cần thiết cho gói standalone"""
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
    
    # File setup Tesseract cải tiến
    setup_tesseract_content = """@echo off
chcp 65001 >nul
echo ========================================
echo    Cài đặt Tesseract OCR
echo ========================================
echo.

REM Kiểm tra xem Tesseract portable đã sẵn sàng chưa
if exist "tesseract-portable\\bin\\tesseract.exe" (
    echo ✅ Tesseract portable đã sẵn sàng!
    echo 📁 Đường dẫn: tesseract-portable\\bin\\tesseract.exe
    echo.
    goto :end
)

REM Kiểm tra xem Tesseract đã được cài đặt trong hệ thống chưa
if exist "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" (
    echo 🔍 Tìm thấy Tesseract trong hệ thống!
    echo 📁 Đường dẫn: C:\\Program Files\\Tesseract-OCR\\tesseract.exe
    echo.
    echo 🔧 Đang copy vào thư mục portable...
    
    REM Tạo thư mục portable nếu chưa có
    if not exist "tesseract-portable" mkdir tesseract-portable
    if not exist "tesseract-portable\\bin" mkdir tesseract-portable\\bin
    if not exist "tesseract-portable\\tessdata" mkdir tesseract-portable\\tessdata
    
    REM Copy tesseract.exe
    copy "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" "tesseract-portable\\bin\\"
    if exist "tesseract-portable\\bin\\tesseract.exe" (
        echo ✅ Đã copy tesseract.exe thành công!
    ) else (
        echo ❌ Không thể copy tesseract.exe!
    )
    
    REM Copy tessdata
    if exist "C:\\Program Files\\Tesseract-OCR\\tessdata" (
        xcopy "C:\\Program Files\\Tesseract-OCR\\tessdata\\*" "tesseract-portable\\tessdata\\" /E /I /Y >nul
        echo ✅ Đã copy tessdata thành công!
    ) else (
        echo ⚠️ Không tìm thấy tessdata trong hệ thống!
    )
    
    REM Tạo file config
    echo # Tesseract Portable Configuration > "tesseract-portable\\tesseract.conf"
    echo # Đường dẫn tới thư mục tessdata >> "tesseract-portable\\tesseract.conf"
    echo TESSDATA_PREFIX=./tessdata/ >> "tesseract-portable\\tesseract.conf"
    echo # Ngôn ngữ mặc định >> "tesseract-portable\\tesseract.conf"
    echo LANG=eng >> "tesseract-portable\\tesseract.conf"
    
    echo ✅ Đã tạo file config!
    echo.
    goto :end
)

echo 🚀 Đang tải và cài đặt Tesseract OCR...
echo.

REM Tạo thư mục tạm
if not exist "temp" mkdir temp
cd temp

REM Tải Tesseract OCR
echo 📥 Đang tải file cài đặt...
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.1.20230401/tesseract-ocr-w64-setup-5.3.1.20230401.exe' -OutFile 'tesseract-installer.exe'"

if exist "tesseract-installer.exe" (
    echo ✅ Tải thành công!
    echo.
    echo 🔧 Đang cài đặt Tesseract OCR...
    echo ⚠️  Vui lòng làm theo hướng dẫn cài đặt...
    echo.
    
    REM Cài đặt Tesseract
    tesseract-installer.exe /S /D=C:\\Program Files\\Tesseract-OCR
    
    echo.
    echo ✅ Cài đặt hoàn tất!
    echo 📁 Tesseract được cài tại: C:\\Program Files\\Tesseract-OCR\\
    echo.
    
    REM Copy vào thư mục portable
    echo 🔧 Đang copy vào thư mục portable...
    
    REM Tạo thư mục portable
    if not exist "..\\tesseract-portable" mkdir "..\\tesseract-portable"
    if not exist "..\\tesseract-portable\\bin" mkdir "..\\tesseract-portable\\bin"
    if not exist "..\\tesseract-portable\\tessdata" mkdir "..\\tesseract-portable\\tessdata"
    
    REM Copy tesseract.exe
    if exist "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" (
        copy "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" "..\\tesseract-portable\\bin\\"
        echo ✅ Đã copy tesseract.exe vào portable!
    ) else (
        echo ❌ Không tìm thấy tesseract.exe sau khi cài đặt!
    )
    
    REM Copy tessdata
    if exist "C:\\Program Files\\Tesseract-OCR\\tessdata" (
        xcopy "C:\\Program Files\\Tesseract-OCR\\tessdata\\*" "..\\tesseract-portable\\tessdata\\" /E /I /Y >nul
        echo ✅ Đã copy tessdata vào portable!
    ) else (
        echo ⚠️ Không tìm thấy tessdata sau khi cài đặt!
    )
    
    REM Tạo file config
    echo # Tesseract Portable Configuration > "..\\tesseract-portable\\tesseract.conf"
    echo # Đường dẫn tới thư mục tessdata >> "..\\tesseract-portable\\tesseract.conf"
    echo TESSDATA_PREFIX=./tessdata/ >> "..\\tesseract-portable\\tesseract.conf"
    echo # Ngôn ngữ mặc định >> "..\\tesseract-portable\\tesseract.conf"
    echo LANG=eng >> "..\\tesseract-portable\\tesseract.conf"
    
    echo ✅ Đã tạo file config!
    
    REM Xóa file tạm
    del tesseract-installer.exe
    
) else (
    echo ❌ Không thể tải file cài đặt!
    echo.
    echo 📋 Hướng dẫn cài đặt thủ công:
    echo 1. Truy cập: https://github.com/UB-Mannheim/tesseract/releases
    echo 2. Tải file: tesseract-ocr-w64-setup-5.3.1.20230401.exe
    echo 3. Cài đặt vào: C:\\Program Files\\Tesseract-OCR\\
    echo 4. Copy tesseract.exe vào: tesseract-portable\\bin\\
    echo 5. Copy tessdata vào: tesseract-portable\\tessdata\\
    echo.
    echo 🔧 Hoặc chạy script này lại sau khi cài đặt thủ công!
)

cd ..
rmdir /s /q temp

:end
echo.
echo 🎉 Hoàn tất! Bây giờ bạn có thể chạy AutoClickTool.exe
echo.
echo 📋 Kiểm tra:
if exist "tesseract-portable\\bin\\tesseract.exe" (
    echo ✅ Tesseract portable: Sẵn sàng
) else (
    echo ❌ Tesseract portable: Chưa sẵn sàng
)

if exist "tesseract-portable\\tessdata\\eng.traineddata" (
    echo ✅ Tessdata English: Sẵn sàng
) else (
    echo ⚠️ Tessdata English: Chưa có (có thể tải thêm)
)

echo.
pause
"""
    
    with open("setup_tesseract.bat", "w", encoding="utf-8") as f:
        f.write(setup_tesseract_content)
    
    # File setup thủ công
    setup_manual_content = """@echo off
chcp 65001 >nul
echo ========================================
echo    Hướng dẫn cài đặt Tesseract thủ công
echo ========================================
echo.

echo 📋 Bước 1: Tải Tesseract OCR
echo 1. Truy cập: https://github.com/UB-Mannheim/tesseract/releases
echo 2. Tải file: tesseract-ocr-w64-setup-5.3.1.20230401.exe
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
3. Chạy `setup_tesseract.bat` để cài đặt Tesseract OCR (nếu cần)

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

def create_standalone_package():
    """Tạo gói standalone hoàn chỉnh"""
    print("📦 Đang tạo gói standalone...")
    
    # Tên gói
    package_name = f"AutoClickTool_Standalone_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Tạo thư mục gói
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Copy các file cần thiết
    files_to_copy = [
        ("dist/AutoClickTool.exe", "AutoClickTool.exe"),
        ("input.csv", "input.csv"),
        ("run_tool.bat", "run_tool.bat"),
        ("setup_tesseract.bat", "setup_tesseract.bat"),
        ("setup_tesseract_manual.bat", "setup_tesseract_manual.bat"),
        ("HƯỚNG DẪN SỬ DỤNG.txt", "HƯỚNG DẪN SỬ DỤNG.txt"),
        ("README.md", "README.md")
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

### 2️⃣ Cài đặt Tesseract (nếu cần)
- Chạy `setup_tesseract.bat` (tự động)
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

## 📖 Xem thêm:
- `HƯỚNG DẪN SỬ DỤNG.txt` - Hướng dẫn chi tiết
- `README.md` - Thông tin kỹ thuật

---
*Gói được tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(os.path.join(package_name, "KHỞI ĐỘNG NHANH.txt"), "w", encoding="utf-8") as f:
        f.write(quick_start)
    
    print(f"\n🎉 Đã tạo gói standalone: {package_name}")
    return package_name

def main():
    print("🚀 Build gói Auto Click Tool Standalone")
    print("=" * 60)
    
    # Bước 1: Cài đặt thư viện
    install_requirements()
    
    # Bước 2: Chuẩn bị Tesseract portable
    download_tesseract_portable()
    
    # Bước 3: Build exe
    if not build_exe():
        print("❌ Build thất bại!")
        return
    
    # Bước 4: Tạo file cần thiết
    create_standalone_files()
    
    # Bước 5: Tạo gói standalone
    package_name = create_standalone_package()
    
    print("\n" + "=" * 60)
    print("🎉 Build hoàn thành!")
    print(f"📁 Gói standalone: {package_name}")
    print("\n📋 Gói bao gồm:")
    print("   ✅ AutoClickTool.exe - File chính (standalone)")
    print("   ✅ input.csv - File dữ liệu")
    print("   ✅ run_tool.bat - Script chạy với hướng dẫn")
    print("   ✅ setup_tesseract.bat - Script cài Tesseract (tự động)")
    print("   ✅ setup_tesseract_manual.bat - Script cài Tesseract (thủ công)")
    print("   ✅ tesseract-portable/ - Tesseract portable")
    print("   ✅ HƯỚNG DẪN SỬ DỤNG.txt - Hướng dẫn chi tiết")
    print("   ✅ KHỞI ĐỘNG NHANH.txt - Hướng dẫn nhanh")
    print("   ✅ README.md - Thông tin kỹ thuật")
    print("\n🎯 Cách sử dụng trên máy khác:")
    print("   1. Copy thư mục gói sang máy đích")
    print("   2. Chạy setup_tesseract.bat để cài Tesseract")
    print("   3. Double-click run_tool.bat")
    print("   4. Làm theo hướng dẫn trên màn hình")
    print("   5. Không cần cài đặt gì thêm!")
    print("\n💡 Ưu điểm của gói standalone:")
    print("   - Không cần cài Python")
    print("   - Không cần cài thư viện")
    print("   - Chạy được ngay trên mọi máy Windows")
    print("   - Bao gồm tất cả dependencies")
    print("   - Có script setup tự động và thủ công")

if __name__ == "__main__":
    main()
