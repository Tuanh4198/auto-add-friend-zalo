# Script tải Tesseract portable trực tiếp
import os
import urllib.request
import zipfile
import shutil
import subprocess
import sys

def download_tesseract_portable():
    """Tải Tesseract portable trực tiếp"""
    print("🔧 Đang tải Tesseract portable trực tiếp...")
    
    # Tạo thư mục
    os.makedirs("tesseract-portable", exist_ok=True)
    os.makedirs("tesseract-portable/bin", exist_ok=True)
    os.makedirs("tesseract-portable/tessdata", exist_ok=True)
    
    # URL cho Tesseract portable
    tesseract_urls = [
        "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.1.20230401/tesseract-ocr-w64-setup-5.3.1.20230401.exe",
        "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe",
        "https://github.com/UB-Mannheim/tesseract/releases/download/v5.2.0.20221222/tesseract-ocr-w64-setup-5.2.0.20221222.exe"
    ]
    
    installer_path = "tesseract-installer.exe"
    success = False
    
    for url in tesseract_urls:
        try:
            print(f"🔄 Thử tải từ: {url}")
            urllib.request.urlretrieve(url, installer_path)
            print("✅ Tải thành công!")
            success = True
            break
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            continue
    
    if not success:
        print("❌ Không thể tải Tesseract installer!")
        return False
    
    # Tải tessdata
    print("📥 Đang tải tessdata...")
    tessdata_urls = [
        "https://github.com/tesseract-ocr/tessdata/archive/refs/heads/main.zip",
        "https://github.com/tesseract-ocr/tessdata_fast/archive/refs/heads/main.zip"
    ]
    
    tessdata_success = False
    for url in tessdata_urls:
        try:
            print(f"🔄 Thử tải tessdata từ: {url}")
            tessdata_zip = "tessdata.zip"
            urllib.request.urlretrieve(url, tessdata_zip)
            print("✅ Tải tessdata thành công!")
            
            # Giải nén tessdata
            with zipfile.ZipFile(tessdata_zip, 'r') as zip_ref:
                zip_ref.extractall("temp_tessdata")
            
            # Copy file eng.traineddata
            eng_data_path = "temp_tessdata/tessdata-main/eng.traineddata"
            if os.path.exists(eng_data_path):
                shutil.copy2(eng_data_path, "tesseract-portable/tessdata/eng.traineddata")
                print("✅ Đã copy eng.traineddata")
            
            # Copy file osd.traineddata
            osd_data_path = "temp_tessdata/tessdata-main/osd.traineddata"
            if os.path.exists(osd_data_path):
                shutil.copy2(osd_data_path, "tesseract-portable/tessdata/osd.traineddata")
                print("✅ Đã copy osd.traineddata")
            
            tessdata_success = True
            break
            
        except Exception as e:
            print(f"❌ Lỗi khi tải tessdata: {e}")
            continue
    
    if not tessdata_success:
        print("⚠️ Không thể tải tessdata, sẽ tải thủ công sau")
    
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

## Ngôn ngữ hỗ trợ:
- eng (English) - Đã có sẵn
- osd (Orientation and script detection) - Đã có sẵn
- Thêm ngôn ngữ khác: Tải từ https://github.com/tesseract-ocr/tessdata
"""
    
    with open("tesseract-portable/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ Đã tạo cấu trúc Tesseract portable!")
    print("⚠️  Cần tải thêm file tesseract.exe từ installer")
    
    # Xóa file tạm
    if os.path.exists(installer_path):
        os.remove(installer_path)
    
    if tessdata_success:
        shutil.rmtree("temp_tessdata")
        os.remove("tessdata.zip")
    
    return True

def create_manual_setup_script():
    """Tạo script setup thủ công"""
    setup_content = """@echo off
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
        f.write(setup_content)
    
    print("✅ Đã tạo script setup thủ công!")

def main():
    print("🚀 Tải Tesseract Portable trực tiếp")
    print("=" * 50)
    
    # Tải Tesseract portable
    if download_tesseract_portable():
        print("✅ Tải Tesseract portable thành công!")
    else:
        print("❌ Tải Tesseract portable thất bại!")
    
    # Tạo script setup thủ công
    create_manual_setup_script()
    
    print("\n" + "=" * 50)
    print("🎉 Hoàn thành!")
    print("📁 Cấu trúc thư mục:")
    print("   tesseract-portable/")
    print("   ├── bin/ (cần copy tesseract.exe vào)")
    print("   ├── tessdata/ (đã có eng.traineddata)")
    print("   ├── tesseract.conf")
    print("   └── README.txt")
    print("\n📋 Bước tiếp theo:")
    print("   1. Chạy setup_tesseract.bat")
    print("   2. Hoặc chạy setup_tesseract_manual.bat")
    print("   3. Hoặc tải thủ công tesseract.exe")

if __name__ == "__main__":
    main()
