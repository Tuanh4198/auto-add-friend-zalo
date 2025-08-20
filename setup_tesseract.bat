@echo off
chcp 65001 >nul
echo ========================================
echo    Cài đặt Tesseract OCR
echo ========================================
echo.

REM Kiểm tra xem Tesseract portable đã sẵn sàng chưa
if exist "tesseract-portable\bin\tesseract.exe" (
    echo ✅ Tesseract portable đã sẵn sàng!
    echo 📁 Đường dẫn: tesseract-portable\bin\tesseract.exe
    echo.
    goto :end
)

REM Kiểm tra xem Tesseract đã được cài đặt trong hệ thống chưa
if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
    echo 🔍 Tìm thấy Tesseract trong hệ thống!
    echo 📁 Đường dẫn: C:\Program Files\Tesseract-OCR\tesseract.exe
    echo.
    echo 🔧 Đang copy vào thư mục portable...
    
    REM Tạo thư mục portable nếu chưa có
    if not exist "tesseract-portable" mkdir tesseract-portable
    if not exist "tesseract-portable\bin" mkdir tesseract-portable\bin
    if not exist "tesseract-portable\tessdata" mkdir tesseract-portable\tessdata
    
    REM Copy tesseract.exe
    copy "C:\Program Files\Tesseract-OCR\tesseract.exe" "tesseract-portable\bin\"
    if exist "tesseract-portable\bin\tesseract.exe" (
        echo ✅ Đã copy tesseract.exe thành công!
    ) else (
        echo ❌ Không thể copy tesseract.exe!
    )
    
    REM Copy tessdata
    if exist "C:\Program Files\Tesseract-OCR\tessdata" (
        xcopy "C:\Program Files\Tesseract-OCR\tessdata\*" "tesseract-portable\tessdata\" /E /I /Y >nul
        echo ✅ Đã copy tessdata thành công!
    ) else (
        echo ⚠️ Không tìm thấy tessdata trong hệ thống!
    )
    
    REM Tạo file config
    echo # Tesseract Portable Configuration > "tesseract-portable\tesseract.conf"
    echo # Đường dẫn tới thư mục tessdata >> "tesseract-portable\tesseract.conf"
    echo TESSDATA_PREFIX=./tessdata/ >> "tesseract-portable\tesseract.conf"
    echo # Ngôn ngữ mặc định >> "tesseract-portable\tesseract.conf"
    echo LANG=eng >> "tesseract-portable\tesseract.conf"
    
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
    tesseract-installer.exe /S /D=C:\Program Files\Tesseract-OCR
    
    echo.
    echo ✅ Cài đặt hoàn tất!
    echo 📁 Tesseract được cài tại: C:\Program Files\Tesseract-OCR\
    echo.
    
    REM Copy vào thư mục portable
    echo 🔧 Đang copy vào thư mục portable...
    
    REM Tạo thư mục portable
    if not exist "..\tesseract-portable" mkdir "..\tesseract-portable"
    if not exist "..\tesseract-portable\bin" mkdir "..\tesseract-portable\bin"
    if not exist "..\tesseract-portable\tessdata" mkdir "..\tesseract-portable\tessdata"
    
    REM Copy tesseract.exe
    if exist "C:\Program Files\Tesseract-OCR\tesseract.exe" (
        copy "C:\Program Files\Tesseract-OCR\tesseract.exe" "..\tesseract-portable\bin\"
        echo ✅ Đã copy tesseract.exe vào portable!
    ) else (
        echo ❌ Không tìm thấy tesseract.exe sau khi cài đặt!
    )
    
    REM Copy tessdata
    if exist "C:\Program Files\Tesseract-OCR\tessdata" (
        xcopy "C:\Program Files\Tesseract-OCR\tessdata\*" "..\tesseract-portable\tessdata\" /E /I /Y >nul
        echo ✅ Đã copy tessdata vào portable!
    ) else (
        echo ⚠️ Không tìm thấy tessdata sau khi cài đặt!
    )
    
    REM Tạo file config
    echo # Tesseract Portable Configuration > "..\tesseract-portable\tesseract.conf"
    echo # Đường dẫn tới thư mục tessdata >> "..\tesseract-portable\tesseract.conf"
    echo TESSDATA_PREFIX=./tessdata/ >> "..\tesseract-portable\tesseract.conf"
    echo # Ngôn ngữ mặc định >> "..\tesseract-portable\tesseract.conf"
    echo LANG=eng >> "..\tesseract-portable\tesseract.conf"
    
    echo ✅ Đã tạo file config!
    
    REM Xóa file tạm
    del tesseract-installer.exe
    
) else (
    echo ❌ Không thể tải file cài đặt!
    echo.
    echo 📋 Hướng dẫn cài đặt thủ công:
    echo 1. Truy cập: https://github.com/UB-Mannheim/tesseract/releases
    echo 2. Tải file: tesseract-ocr-w64-setup-5.3.1.20230401.exe
    echo 3. Cài đặt vào: C:\Program Files\Tesseract-OCR\
    echo 4. Copy tesseract.exe vào: tesseract-portable\bin\
    echo 5. Copy tessdata vào: tesseract-portable\tessdata\
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
if exist "tesseract-portable\bin\tesseract.exe" (
    echo ✅ Tesseract portable: Sẵn sàng
) else (
    echo ❌ Tesseract portable: Chưa sẵn sàng
)

if exist "tesseract-portable\tessdata\eng.traineddata" (
    echo ✅ Tessdata English: Sẵn sàng
) else (
    echo ⚠️ Tessdata English: Chưa có (có thể tải thêm)
)

echo.
pause
