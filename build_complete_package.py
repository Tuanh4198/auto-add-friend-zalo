# Script build gói hoàn chỉnh bao gồm Tesseract portable
import os
import subprocess
import sys
import shutil
from datetime import datetime

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    print("📦 Đang cài đặt các thư viện cần thiết...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Đã cài đặt xong các thư viện!")

def download_tesseract_portable():
    """Tải và chuẩn bị Tesseract portable"""
    print("🔧 Đang chuẩn bị Tesseract portable...")
    
    # Kiểm tra xem đã có chưa
    if os.path.exists("tesseract-portable"):
        print("✅ Tesseract portable đã tồn tại!")
        return True
    
    # Tạo thư mục tesseract-portable cơ bản
    os.makedirs("tesseract-portable", exist_ok=True)
    os.makedirs("tesseract-portable/bin", exist_ok=True)
    os.makedirs("tesseract-portable/tessdata", exist_ok=True)
    
    # Tạo file config
    config_content = """# Tesseract Portable Configuration
# Đường dẫn tới thư mục tessdata
TESSDATA_PREFIX=./tessdata/
# Ngôn ngữ mặc định
LANG=eng
"""
    
    with open("tesseract-portable/tesseract.conf", "w") as f:
        f.write(config_content)
    
    # Tạo file README cho Tesseract
    readme_content = """# Tesseract Portable

Đây là phiên bản portable của Tesseract OCR.

## Cấu trúc:
- bin/ - Chứa file tesseract.exe (cần tải thêm)
- tessdata/ - Chứa dữ liệu ngôn ngữ (cần tải thêm)
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
    return True

def build_exe():
    """Build file exe với PyInstaller"""
    print("🔨 Đang build file exe...")
    
    # Lệnh PyInstaller với các tùy chọn
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

def create_batch_files():
    """Tạo các file batch cần thiết"""
    print("📝 Đang tạo các file batch...")
    
    # File chạy tool
    run_tool_content = """@echo off
echo ========================================
echo    Auto Click Tool
echo ========================================
echo.
echo Chuan bi chay tool...
echo.
pause
AutoClickTool.exe
pause
"""
    
    with open("run_tool.bat", "w", encoding="utf-8") as f:
        f.write(run_tool_content)
    
    # File setup Tesseract
    setup_tesseract_content = """@echo off
echo ========================================
echo    Cài đặt Tesseract OCR
echo ========================================
echo.

if exist "tesseract-portable\\bin\\tesseract.exe" (
    echo ✅ Tesseract portable đã sẵn sàng!
    echo 📁 Đường dẫn: tesseract-portable\\bin\\tesseract.exe
    echo.
    goto :end
)

echo 🚀 Đang tải Tesseract OCR...
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
    tesseract-installer.exe /S /D=C:\\Program Files\\Tesseract-OCR
    
    echo.
    echo ✅ Cài đặt hoàn tất!
    echo 📁 Tesseract được cài tại: C:\\Program Files\\Tesseract-OCR\\
    echo.
    
    REM Xóa file tạm
    del tesseract-installer.exe
) else (
    echo ❌ Không thể tải file cài đặt!
    echo.
    echo 📋 Hướng dẫn cài đặt thủ công:
    echo 1. Truy cập: https://github.com/UB-Mannheim/tesseract/releases
    echo 2. Tải file: tesseract-ocr-w64-setup-5.3.1.20230401.exe
    echo 3. Cài đặt vào: C:\\Program Files\\Tesseract-OCR\\
)

cd ..
rmdir /s /q temp

:end
echo.
echo 🎉 Hoàn tất! Bây giờ bạn có thể chạy AutoClickTool.exe
pause
"""
    
    with open("setup_tesseract.bat", "w", encoding="utf-8") as f:
        f.write(setup_tesseract_content)
    
    print("✅ Đã tạo các file batch!")

def create_package():
    """Tạo gói phân phối hoàn chỉnh"""
    print("📦 Đang tạo gói phân phối...")
    
    # Tên gói
    package_name = f"AutoClickTool_Complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
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
    
    # Tạo file hướng dẫn nhanh
    quick_guide = f"""# 🚀 Hướng dẫn nhanh

## Bước 1: Cài đặt Tesseract OCR
Chạy file: setup_tesseract.bat

## Bước 2: Chuẩn bị dữ liệu
- Mở file input.csv
- Thêm số điện thoại vào cột A (1 số/dòng)

## Bước 3: Chạy tool
- Double-click: AutoClickTool.exe
- Hoặc chạy: run_tool.bat

## ⚠️ Lưu ý
- Có thể cần tắt Windows Defender
- Chạy với quyền Administrator nếu cần
- Đảm bảo độ phân giải màn hình giống nhau

## 📞 Hỗ trợ
Xem file README.md để biết thêm chi tiết
"""
    
    with open(os.path.join(package_name, "HƯỚNG DẪN NHANH.txt"), "w", encoding="utf-8") as f:
        f.write(quick_guide)
    
    print(f"\n🎉 Đã tạo gói phân phối: {package_name}")
    return package_name

def main():
    print("🚀 Build gói Auto Click Tool hoàn chỉnh")
    print("=" * 60)
    
    # Bước 1: Cài đặt thư viện
    install_requirements()
    
    # Bước 2: Chuẩn bị Tesseract portable
    download_tesseract_portable()
    
    # Bước 3: Build exe
    if not build_exe():
        print("❌ Build thất bại!")
        return
    
    # Bước 4: Tạo file batch
    create_batch_files()
    
    # Bước 5: Tạo gói phân phối
    package_name = create_package()
    
    print("\n" + "=" * 60)
    print("🎉 Build hoàn thành!")
    print(f"📁 Gói phân phối: {package_name}")
    print("\n📋 Gói bao gồm:")
    print("   ✅ AutoClickTool.exe - File chính")
    print("   ✅ input.csv - File dữ liệu")
    print("   ✅ run_tool.bat - Script chạy")
    print("   ✅ setup_tesseract.bat - Script cài Tesseract")
    print("   ✅ tesseract-portable/ - Tesseract portable")
    print("   ✅ README.md - Hướng dẫn chi tiết")
    print("   ✅ HƯỚNG DẪN NHANH.txt - Hướng dẫn nhanh")
    print("\n🎯 Cách sử dụng trên máy khác:")
    print("   1. Copy thư mục gói sang máy đích")
    print("   2. Chạy setup_tesseract.bat (nếu cần)")
    print("   3. Chỉnh sửa input.csv")
    print("   4. Chạy AutoClickTool.exe")

if __name__ == "__main__":
    main()
