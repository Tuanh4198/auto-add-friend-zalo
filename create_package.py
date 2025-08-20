# Script tạo gói phân phối hoàn chỉnh
import os
import shutil
import zipfile
from datetime import datetime

def create_package():
    """Tạo gói phân phối hoàn chỉnh"""
    print("📦 Đang tạo gói phân phối...")
    
    # Tên gói
    package_name = f"AutoClickTool_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
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
    
    # Copy thư mục Tesseract portable nếu có
    if os.path.exists("tesseract-portable"):
        print("📁 Copy thư mục tesseract-portable...")
        shutil.copytree("tesseract-portable", os.path.join(package_name, "tesseract-portable"))
        print("✅ Đã copy Tesseract portable")
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(package_name, dst))
            print(f"✅ Đã copy: {src} -> {dst}")
        else:
            print(f"⚠️  File không tồn tại: {src}")
    
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
    
    # Tạo file ZIP
    zip_name = f"{package_name}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 Đã tạo gói phân phối: {zip_name}")
    print(f"📁 Thư mục: {package_name}")
    
    return package_name, zip_name

def main():
    print("🚀 Tạo gói phân phối Auto Click Tool")
    print("=" * 50)
    
    # Kiểm tra file exe đã build chưa
    if not os.path.exists("dist/AutoClickTool.exe"):
        print("❌ File exe chưa được build!")
        print("💡 Hãy chạy: python build_exe.py trước")
        return
    
    # Tạo gói
    package_name, zip_name = create_package()
    
    print("\n" + "=" * 50)
    print("📋 Gói phân phối bao gồm:")
    print("   ✅ AutoClickTool.exe - File chính")
    print("   ✅ input.csv - File dữ liệu")
    print("   ✅ run_tool.bat - Script chạy")
    print("   ✅ setup_tesseract.bat - Script cài Tesseract")
    print("   ✅ README.md - Hướng dẫn chi tiết")
    print("   ✅ HƯỚNG DẪN NHANH.txt - Hướng dẫn nhanh")
    print("\n📦 Có thể phân phối:")
    print(f"   📁 Thư mục: {package_name}")
    print(f"   📦 File ZIP: {zip_name}")
    print("\n🎯 Cách sử dụng trên máy khác:")
    print("   1. Giải nén file ZIP")
    print("   2. Chạy setup_tesseract.bat")
    print("   3. Chỉnh sửa input.csv")
    print("   4. Chạy AutoClickTool.exe")

if __name__ == "__main__":
    main()
