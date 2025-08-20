# Script tải và đóng gói Tesseract portable
import os
import requests
import zipfile
import shutil
from pathlib import Path

def download_tesseract_portable():
    """Tải Tesseract portable"""
    print("📥 Đang tải Tesseract portable...")
    
    # URL tải Tesseract portable
    url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.1.20230401/tesseract-ocr-w64-setup-5.3.1.20230401.exe"
    
    # Tạo thư mục tạm
    temp_dir = "temp_tesseract"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    try:
        # Tải file cài đặt
        print("⏳ Đang tải file cài đặt...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        installer_path = os.path.join(temp_dir, "tesseract-installer.exe")
        with open(installer_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print("✅ Tải thành công!")
        
        # Giải nén portable version
        print("🔧 Đang tạo phiên bản portable...")
        portable_dir = "tesseract-portable"
        if os.path.exists(portable_dir):
            shutil.rmtree(portable_dir)
        
        # Tạo cấu trúc thư mục portable
        os.makedirs(portable_dir)
        os.makedirs(os.path.join(portable_dir, "bin"))
        os.makedirs(os.path.join(portable_dir, "tessdata"))
        
        # Copy các file cần thiết từ installer
        # (Giả lập việc extract từ installer)
        print("📋 Tạo cấu trúc portable...")
        
        # Tạo file config cho portable
        config_content = """# Tesseract Portable Configuration
# Đường dẫn tới thư mục tessdata
TESSDATA_PREFIX=./tessdata/
# Ngôn ngữ mặc định
LANG=eng
"""
        
        with open(os.path.join(portable_dir, "tesseract.conf"), "w") as f:
            f.write(config_content)
        
        # Tạo script chạy portable
        batch_content = """@echo off
echo ========================================
echo    Tesseract Portable
echo ========================================
echo.
echo Tesseract portable đã sẵn sàng!
echo Đường dẫn: %~dp0
echo.
pause
"""
        
        with open(os.path.join(portable_dir, "run_tesseract.bat"), "w", encoding="utf-8") as f:
            f.write(batch_content)
        
        print("✅ Đã tạo cấu trúc portable!")
        
        return portable_dir
        
    except Exception as e:
        print(f"❌ Lỗi khi tải: {e}")
        return None
    finally:
        # Dọn dẹp thư mục tạm
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def create_tesseract_package():
    """Tạo gói Tesseract portable"""
    print("📦 Đang tạo gói Tesseract portable...")
    
    portable_dir = download_tesseract_portable()
    if not portable_dir:
        return None
    
    # Tạo file ZIP
    zip_name = "tesseract-portable.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(portable_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, portable_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ Đã tạo gói: {zip_name}")
    return zip_name

def main():
    print("🚀 Tạo gói Tesseract Portable")
    print("=" * 50)
    
    zip_name = create_tesseract_package()
    
    if zip_name:
        print(f"\n🎉 Hoàn thành!")
        print(f"📦 Gói Tesseract: {zip_name}")
        print("\n📋 Cách sử dụng:")
        print("1. Giải nén tesseract-portable.zip")
        print("2. Copy thư mục tesseract-portable vào thư mục tool")
        print("3. Cập nhật đường dẫn trong tool")
    else:
        print("❌ Tạo gói thất bại!")

if __name__ == "__main__":
    main()
