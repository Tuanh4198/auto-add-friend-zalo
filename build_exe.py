# Script để build file exe
import os
import subprocess
import sys

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    print("📦 Đang cài đặt các thư viện cần thiết...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✅ Đã cài đặt xong các thư viện!")

def build_exe():
    """Build file exe với PyInstaller"""
    print("🔨 Đang build file exe...")
    
    # Lệnh PyInstaller với các tùy chọn
    cmd = [
        "pyinstaller",
        "--onefile",  # Tạo 1 file exe duy nhất
        "--windowed",  # Không hiển thị console (tùy chọn)
        "--name=AutoClickTool",  # Tên file exe
        "--icon=icon.ico",  # Icon cho file exe (nếu có)
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
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi build: {e}")
        return False
    
    return True

def create_batch_file():
    """Tạo file batch để chạy dễ dàng"""
    batch_content = """@echo off
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
        f.write(batch_content)
    
    print("✅ Đã tạo file run_tool.bat")

def main():
    print("🚀 Bắt đầu quá trình đóng gói tool...")
    print("=" * 50)
    
    # Bước 1: Cài đặt thư viện
    install_requirements()
    
    # Bước 2: Build exe
    if build_exe():
        # Bước 3: Tạo file batch
        create_batch_file()
        
        print("\n" + "=" * 50)
        print("🎉 Đóng gói thành công!")
        print("📁 Các file đã tạo:")
        print("   - dist/AutoClickTool.exe (File chính)")
        print("   - run_tool.bat (File chạy)")
        print("   - input.csv (File dữ liệu)")
        print("\n📋 Hướng dẫn sử dụng:")
        print("   1. Copy thư mục dist/ sang máy khác")
        print("   2. Copy file input.csv vào cùng thư mục")
        print("   3. Chạy AutoClickTool.exe hoặc run_tool.bat")
        print("\n⚠️  Lưu ý:")
        print("   - Máy đích cần cài Tesseract OCR")
        print("   - Có thể cần tắt Windows Defender")
        print("   - Chạy với quyền Administrator nếu cần")
    else:
        print("❌ Đóng gói thất bại!")

if __name__ == "__main__":
    main()
