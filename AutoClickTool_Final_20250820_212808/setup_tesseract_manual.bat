@echo off
chcp 65001 >nul
echo ========================================
echo    Hướng dẫn cài đặt Tesseract thủ công
echo ========================================
echo.

echo 📋 Bước 1: Tải Tesseract OCR
echo 1. Truy cập: https://github.com/UB-Mannheim/tesseract/releases
echo 2. Tải file: tesseract-ocr-w64-setup-5.4.0.20240606.exe
echo 3. Cài đặt vào: C:\Program Files\Tesseract-OCR\
echo.

echo 📋 Bước 2: Copy vào thư mục portable
echo 1. Copy file: C:\Program Files\Tesseract-OCR\tesseract.exe
echo 2. Paste vào: tesseract-portable\bin\
echo 3. Copy thư mục: C:\Program Files\Tesseract-OCR\tessdata
echo 4. Paste vào: tesseract-portable\tessdata\
echo.

echo 📋 Bước 3: Kiểm tra
echo 1. Kiểm tra file: tesseract-portable\bin\tesseract.exe
echo 2. Kiểm tra file: tesseract-portable\tessdata\eng.traineddata
echo.

echo 🎉 Hoàn tất! Bây giờ bạn có thể chạy AutoClickTool.exe
pause
