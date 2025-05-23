# Cài đặt: pip install email-validator
from email_validator import validate_email, EmailNotValidError
import json
from datetime import datetime
import re

# Thêm danh sách khóa học
danh_sach_khoa_hoc = {
    "KH001": 1500000,
    "KH002": 2000000,
    "KH003": 1800000,
    "KH004": 2500000
}

def calculate_cost(ma_khoa_hoc, so_luong, ma_uu_dai=None):
    gia_goc = danh_sach_khoa_hoc.get(ma_khoa_hoc, 0)
    tong_tien = gia_goc * so_luong
    
    # Áp dụng giảm giá
    if ma_uu_dai == "SUMMER25":
        tong_tien *= 0.75
    elif ma_uu_dai == "EARLYBIRD":
        tong_tien *= 0.85
    
    return round(tong_tien, 2)

def validate_email_format(email):
    try:
        validate_email(email)
        return True, ""
    except EmailNotValidError as e:
        return False, str(e)

def validate_ma_khoa_hoc(ma_khoa_hoc):
    if not re.match(r'^KH\d{3}$', ma_khoa_hoc):
        return False, "Mã khóa học phải có định dạng KH + 3 số"
    if ma_khoa_hoc not in danh_sach_khoa_hoc:
        return False, f"Mã khóa học {ma_khoa_hoc} không tồn tại trong hệ thống"
    return True, ""

def validate_ho_ten(ho_ten):
    if len(ho_ten.strip()) < 2:
        return False, "Tên phải có ít nhất 2 ký tự"
    return True, ""

def save_registration(registration_data):
    try:
        # Đọc dữ liệu cũ nếu có
        try:
            with open("registrations.json", "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []
        
        # Thêm dữ liệu mới
        existing_data.append(registration_data)
        
        # Ghi toàn bộ dữ liệu
        with open("registrations.json", "w", encoding="utf-8") as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu: {str(e)}")

def load_registrations():
    try:
        with open("registrations.json", "r", encoding="utf-8") as f:
            registrations = json.load(f)
            for reg in registrations:
                print(
                    f"\nĐăng ký của {reg['ho_ten']}: "
                    f"Khóa học {reg['ma_khoa_hoc']}, "
                    f"Ngày {reg['ngay_dang_ky']}, "
                    f"Chi phí {reg['chi_phi']:,.2f} VNĐ"
                )
        return True
    except FileNotFoundError:
        print("Không tìm thấy file đăng ký!")
        return False
    except json.JSONDecodeError:
        print("Lỗi định dạng file JSON!")
        return False

def main():
    """Hàm chính điều khiển luồng đăng ký khóa học"""
    try:
        print("=== CHƯƠNG TRÌNH ĐĂNG KÝ KHÓA HỌC ===")
        
        # Nhập và validate họ tên
        while True:
            ho_ten = input("Nhập họ tên học viên: ")
            valid, error_msg = validate_ho_ten(ho_ten)
            if valid:
                break
            print(f"[!] Lỗi: {error_msg}")
        
        # Nhập và validate email
        while True:
            email = input("Nhập email: ")
            valid, error_msg = validate_email_format(email)
            if valid:
                break
            print(f"[!] Lỗi: {error_msg}")
        
        # Nhập và validate mã khóa học
        while True:
            ma_khoa_hoc = input("Nhập mã khóa học (VD: KH001): ")
            valid, error_msg = validate_ma_khoa_hoc(ma_khoa_hoc)
            if valid:
                break
            print(f"[!] Lỗi: {error_msg}")
        
        # Nhập và validate số lượng
        while True:
            try:
                so_luong = int(input("Nhập số lượng khóa học: "))
                if so_luong < 1:
                    print("[!] Lỗi: Số lượng phải lớn hơn 0")
                    continue
                break
            except ValueError:
                print("[!] Lỗi: Số lượng phải là số nguyên dương")
        
        # Nhập mã ưu đãi
        ma_uu_dai = input("Nhập mã ưu đãi (nếu có): ") or None
        
        # Tính toán chi phí
        ngay_dang_ky = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        tong_chi_phi = calculate_cost(ma_khoa_hoc, so_luong, ma_uu_dai)
        
        # Tạo bản ghi và lưu file
        registration_data = {
            "ho_ten": ho_ten,
            "email": email,
            "ma_khoa_hoc": ma_khoa_hoc,
            "so_luong": so_luong,
            "ngay_dang_ky": ngay_dang_ky,
            "chi_phi": tong_chi_phi
        }
        save_registration(registration_data)
        
        # Hiển thị kết quả với String Formatting
        print(f"\n{'='*50}")
        print(f"ĐĂNG KÝ THÀNH CÔNG!")
        print(f"{'='*50}")
        
        # Thông báo xác nhận đăng ký theo yêu cầu
        thong_bao_xac_nhan = "Chúc mừng {ten} đã đăng ký khóa học {ma_khoa_hoc} vào ngày {ngay_dang_ky}!".format(
            ten=ho_ten,
            ma_khoa_hoc=ma_khoa_hoc,
            ngay_dang_ky=ngay_dang_ky
        )
        print(thong_bao_xac_nhan)
        
        # Thông tin chi tiết
        print(f"\nThông tin chi tiết:")
        print(f"Học viên: {ho_ten}")
        print(f"Email: {email}")
        print(f"Mã khóa học: {ma_khoa_hoc} x {so_luong}")
        print(f"Tổng chi phí: {tong_chi_phi:,.2f} VNĐ")
        print(f"{'='*50}\n")
        
        # Hiển thị lịch sử đăng ký
        print("\n=== LỊCH SỬ ĐĂNG KÝ ===")
        load_registrations()
        
    except Exception as e:
        print(f"\n[!] LỖI HỆ THỐNG: {str(e)}")
    finally:
        print("\nCảm ơn đã sử dụng dịch vụ!")

# Chạy chương trình
if __name__ == "__main__":
    main()