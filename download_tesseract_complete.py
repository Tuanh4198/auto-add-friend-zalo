# Script tải Tesseract portable hoàn chỉnh
import os
import urllib.request
import zipfile
import shutil
from pathlib import Path

def download_tesseract_portable():
    """Tải Tesseract portable hoàn chỉnh"""
    print("🔧 Đang tải Tesseract portable hoàn chỉnh...")
    
    # Tạo thư mục
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
    
    with open("tesseract-portable/tesseract.conf", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    # Tải Tesseract portable từ GitHub releases
    print("📥 Đang tải Tesseract portable...")
    
    # URL cho Tesseract portable
    tesseract_urls = [
        "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.1.20230401/tesseract-ocr-w64-setup-5.3.1.20230401.exe",
        "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe"
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
        print("📋 Hướng dẫn cài đặt thủ công:")
        print("1. Truy cập: https://github.com/UB-Mannheim/tesseract/releases")
        print("2. Tải file: tesseract-ocr-w64-setup-5.3.1.20230401.exe")
        print("3. Cài đặt vào: C:\\Program Files\\Tesseract-OCR\\")
        return False
    
    # Tải tessdata
    print("📥 Đang tải tessdata...")
    tessdata_url = "https://github.com/tesseract-ocr/tessdata/archive/refs/heads/main.zip"
    tessdata_zip = "tessdata.zip"
    
    try:
        urllib.request.urlretrieve(tessdata_url, tessdata_zip)
        print("✅ Tải tessdata thành công!")
        
        # Giải nén tessdata
        with zipfile.ZipFile(tessdata_zip, 'r') as zip_ref:
            zip_ref.extractall("temp_tessdata")
        
        # Copy file eng.traineddata
        eng_data_path = "temp_tessdata/tessdata-main/eng.traineddata"
        if os.path.exists(eng_data_path):
            shutil.copy2(eng_data_path, "tesseract-portable/tessdata/eng.traineddata")
            print("✅ Đã copy eng.traineddata")
        else:
            print("⚠️ Không tìm thấy eng.traineddata")
        
        # Copy file osd.traineddata
        osd_data_path = "temp_tessdata/tessdata-main/osd.traineddata"
        if os.path.exists(osd_data_path):
            shutil.copy2(osd_data_path, "tesseract-portable/tessdata/osd.traineddata")
            print("✅ Đã copy osd.traineddata")
        
        # Xóa file tạm
        shutil.rmtree("temp_tessdata")
        os.remove(tessdata_zip)
        
    except Exception as e:
        print(f"❌ Lỗi khi tải tessdata: {e}")
        print("📋 Hướng dẫn tải tessdata thủ công:")
        print("1. Truy cập: https://github.com/tesseract-ocr/tessdata")
        print("2. Tải file eng.traineddata")
        print("3. Copy vào thư mục: tesseract-portable/tessdata/")
    
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
    
    # Xóa file installer
    if os.path.exists(installer_path):
        os.remove(installer_path)
    
    return True

def create_setup_script():
    """Tạo script setup tự động"""
    setup_content = """@echo off
chcp 65001 >nul
echo ========================================
echo    Cài đặt Tesseract OCR Portable
echo ========================================
echo.

if exist "tesseract-portable\\bin\\tesseract.exe" (
    echo ✅ Tesseract portable đã sẵn sàng!
    echo 📁 Đường dẫn: tesseract-portable\\bin\\tesseract.exe
    echo.
    goto :end
)

echo 🚀 Đang cài đặt Tesseract OCR...
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
    
    REM Copy file tesseract.exe vào portable
    if exist "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" (
        copy "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" "..\\tesseract-portable\\bin\\"
        echo ✅ Đã copy tesseract.exe vào portable
    )
    
    REM Copy tessdata vào portable
    if exist "C:\\Program Files\\Tesseract-OCR\\tessdata" (
        xcopy "C:\\Program Files\\Tesseract-OCR\\tessdata\\*" "..\\tesseract-portable\\tessdata\\" /E /I /Y
        echo ✅ Đã copy tessdata vào portable
    )
    
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
)

cd ..
rmdir /s /q temp

:end
echo.
echo 🎉 Hoàn tất! Bây giờ bạn có thể chạy AutoClickTool.exe
pause
"""
    
    with open("setup_tesseract_complete.bat", "w", encoding="utf-8") as f:
        f.write(setup_content)
    
    print("✅ Đã tạo script setup hoàn chỉnh!")

def main():
    print("🚀 Tải Tesseract Portable hoàn chỉnh")
    print("=" * 50)
    
    # Tải Tesseract portable
    if download_tesseract_portable():
        print("✅ Tải Tesseract portable thành công!")
    else:
        print("❌ Tải Tesseract portable thất bại!")
    
    # Tạo script setup
    create_setup_script()
    
    print("\n" + "=" * 50)
    print("🎉 Hoàn thành!")
    print("📁 Cấu trúc thư mục:")
    print("   tesseract-portable/")
    print("   ├── bin/ (cần copy tesseract.exe vào)")
    print("   ├── tessdata/ (đã có eng.traineddata)")
    print("   ├── tesseract.conf")
    print("   └── README.txt")
    print("\n📋 Bước tiếp theo:")
    print("   1. Chạy setup_tesseract_complete.bat")
    print("   2. Hoặc tải thủ công tesseract.exe")
    print("   3. Copy vào thư mục bin/")

if __name__ == "__main__":
    main()
