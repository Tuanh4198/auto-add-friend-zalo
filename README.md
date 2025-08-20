# 🤖 Auto Click Tool

Tool tự động click và xử lý dữ liệu từ file CSV.

## 📋 Yêu cầu hệ thống

- Windows 10/11
- Python 3.8+ (chỉ cần thiết khi build)
- Tesseract OCR (cần thiết để đọc text)

## 🚀 Cách đóng gói tool

### Bước 1: Chuẩn bị môi trường
```bash
# Cài đặt Python (nếu chưa có)
# Tải từ: https://www.python.org/downloads/

# Clone hoặc tải source code
```

### Bước 2: Build gói hoàn chỉnh (Khuyến nghị)
```bash
# Chạy script build hoàn chỉnh (bao gồm Tesseract portable)
python build_complete_package.py
```

### Bước 3: Build cơ bản
```bash
# Chạy script build cơ bản
python build_exe.py
```

Hoặc thủ công:
```bash
# Cài đặt thư viện
pip install -r requirements.txt

# Build exe
pyinstaller --onefile --name=AutoClickTool --add-data=input.csv;. click_auto.py
```

### Bước 3: Kiểm tra kết quả
Sau khi build thành công, bạn sẽ có:
- `dist/AutoClickTool.exe` - File chính
- `run_tool.bat` - File chạy dễ dàng
- `setup_tesseract.bat` - Script cài Tesseract

## 📦 Đóng gói để phân phối

### Gói hoàn chỉnh bao gồm:
```
AutoClickTool_Complete_20241201_143022/
├── AutoClickTool.exe          # File chính
├── input.csv                  # File dữ liệu
├── run_tool.bat              # Script chạy
├── setup_tesseract.bat       # Script cài Tesseract
├── tesseract-portable/       # Tesseract portable
│   ├── bin/                  # Thư mục chứa tesseract.exe
│   ├── tessdata/             # Thư mục chứa dữ liệu ngôn ngữ
│   ├── tesseract.conf        # File cấu hình
│   └── README.txt            # Hướng dẫn Tesseract
├── README.md                 # Hướng dẫn chi tiết
└── HƯỚNG DẪN NHANH.txt       # Hướng dẫn nhanh
```

## 🎯 Cách sử dụng trên máy khác

### Bước 1: Cài đặt Tesseract OCR
```bash
# Chạy script tự động
setup_tesseract.bat
```

Hoặc cài thủ công:
1. Tải từ: https://github.com/UB-Mannheim/tesseract/releases
2. Cài đặt vào: `C:\Program Files\Tesseract-OCR\`

### Bước 2: Chuẩn bị dữ liệu
1. Copy `input.csv` vào thư mục chứa tool
2. Đảm bảo cột A chứa số điện thoại

### Bước 3: Chạy tool
```bash
# Cách 1: Double-click file exe
AutoClickTool.exe

# Cách 2: Chạy script batch
run_tool.bat
```

## 🔧 Cấu trúc file CSV

```
0386876699
0386876700
0386876701
...
[trống],"x1,y1","x2,y2","x3,y3","x4,y4","x5,y5"
```

- **Cột A**: Số điện thoại (1 số/dòng)
- **Dòng cuối**: Tọa độ 5 điểm (tự động tạo)

## ⚠️ Lưu ý quan trọng

### Bảo mật:
- Có thể cần tắt Windows Defender
- Chạy với quyền Administrator nếu cần
- Thêm vào whitelist nếu bị chặn

### Tương thích:
- Chỉ hỗ trợ Windows
- Cần Tesseract OCR để đọc text
- Test trên Windows 10/11

### Troubleshooting:
1. **Lỗi "Tesseract not found"**
   - Chạy `setup_tesseract.bat`
   - Kiểm tra đường dẫn: `C:\Program Files\Tesseract-OCR\`

2. **Lỗi "Permission denied"**
   - Chạy với quyền Administrator
   - Tắt Windows Defender tạm thời

3. **Tool không click đúng vị trí**
   - Đảm bảo độ phân giải màn hình giống nhau
   - Lấy lại tọa độ trên máy đích

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Tesseract OCR đã cài đúng chưa
2. File CSV có đúng định dạng không
3. Quyền truy cập có đủ không
4. Windows Defender có chặn không

## 🔄 Cập nhật

Để cập nhật tool:
1. Thay thế `AutoClickTool.exe` bằng file mới
2. Giữ nguyên `input.csv` và các file khác
3. Chạy lại tool
# auto-add-friend-zalo
