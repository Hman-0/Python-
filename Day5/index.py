from datetime import datetime
import re
import json
import os

# Thêm thư viện để kết nối với Google Drive
try:
    from google.colab import drive
    IN_COLAB = True
    
    # Cài đặt thư viện bên ngoài khi chạy trong Colab
    print("Đang cài đặt thư viện cần thiết...")

except ImportError:
    IN_COLAB = False

# Import thư viện bên ngoài
try:
    import pendulum
    import tabulate
    LIBRARIES_AVAILABLE = True
except ImportError:
    LIBRARIES_AVAILABLE = False
    print("Cảnh báo: Thư viện pendulum hoặc tabulate chưa được cài đặt.")
    print("Nếu bạn đang chạy trên máy tính cá nhân, hãy cài đặt bằng lệnh:")
    print("pip install pendulum tabulate")

def validate_input(loai_input, gia_tri):
    """
    Hàm kiểm tra tính hợp lệ của dữ liệu đầu vào
    """
    if loai_input == "ho_ten":
        # Kiểm tra họ tên chỉ chứa chữ cái và khoảng trắng
        pattern = r'^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ\s]+$'
        if not re.match(pattern, gia_tri):
            raise ValueError("Họ tên chỉ được chứa chữ cái và khoảng trắng")
        return gia_tri
        
    elif loai_input == "email":
        # Kiểm tra email đúng định dạng
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, gia_tri):
            raise ValueError("Email không đúng định dạng")
        return gia_tri
        
    elif loai_input == "so_bai_tap":
        # Kiểm tra số bài tập là số nguyên không âm
        so_bai_tap = int(gia_tri)
        if so_bai_tap < 0:
            raise ValueError("Số bài tập phải là số nguyên không âm")
        return so_bai_tap
        
    elif loai_input == "diem_tb":
        # Kiểm tra điểm trung bình nằm trong khoảng 0-10
        diem_tb = float(gia_tri)
        if diem_tb < 0 or diem_tb > 10:
            raise ValueError("Điểm trung bình phải nằm trong khoảng 0 đến 10")
        return diem_tb
    
    elif loai_input == "so_luong_hoc_vien":
        # Kiểm tra số lượng học viên là số nguyên dương
        so_luong = int(gia_tri)
        if so_luong <= 2:
            raise ValueError("Số lượng học viên phải là số nguyên dương và ít nhất phải là 3 ")
        return so_luong
    
    return gia_tri

def calculate_stats(hoc_vien, so_bai_tap_toi_da=5):
    """
    Hàm tính toán thống kê từ danh sách học viên
    """
    # Tính điểm trung bình của tất cả học viên
    tong_diem = sum(hv['Điểm TB'] for hv in hoc_vien)
    diem_tb = tong_diem / len(hoc_vien) if hoc_vien else 0
    diem_tb = round(diem_tb, 2)
    
    # Tìm học viên có điểm cao nhất và thấp nhất
    if hoc_vien:
        hv_diem_cao_nhat = max(hoc_vien, key=lambda hv: hv['Điểm TB'])
        hv_diem_thap_nhat = min(hoc_vien, key=lambda hv: hv['Điểm TB'])
    else:
        hv_diem_cao_nhat = hv_diem_thap_nhat = None
    
    # Tính tỷ lệ hoàn thành bài tập
    tong_bai_tap = sum(hv['Số bài tập'] for hv in hoc_vien)
    tong_bai_tap_toi_da = len(hoc_vien) * so_bai_tap_toi_da
    ty_le_hoan_thanh = (tong_bai_tap / tong_bai_tap_toi_da * 100) if tong_bai_tap_toi_da > 0 else 0
    ty_le_hoan_thanh = round(ty_le_hoan_thanh, 2)
    
    return {
        'diem_tb': diem_tb,
        'hv_diem_cao_nhat': hv_diem_cao_nhat,
        'hv_diem_thap_nhat': hv_diem_thap_nhat,
        'ty_le_hoan_thanh': ty_le_hoan_thanh
    }

def save_summary(tuan, ngay_tk, hoc_vien, thu_muc="data"):
    """
    Hàm lưu thông tin tuần vào tệp JSON
    """
    # Kiểm tra và kết nối Google Drive nếu đang chạy trong Colab
    if IN_COLAB:
        try:
            drive.mount('/content/drive')
            thu_muc = "/content/drive/MyDrive/data"
        except Exception as e:
            print(f"Lỗi kết nối Google Drive: {e}")
            return False
    
    # Tạo thư mục nếu chưa tồn tại
    try:
        if not os.path.exists(thu_muc):
            os.makedirs(thu_muc)
    except Exception as e:
        print(f"Lỗi tạo thư mục: {e}")
        return False
    
    # Tạo đường dẫn tệp JSON
    ten_tep = f"week_{tuan}.json"
    duong_dan = os.path.join(thu_muc, ten_tep)
    
    # Chuẩn bị dữ liệu để lưu
    du_lieu = {
        'tuần': tuan,
        'ngày tổng kết': ngay_tk,
        'học viên': hoc_vien
    }
    
    # Lưu dữ liệu vào tệp JSON
    try:
        with open(duong_dan, 'w', encoding='utf-8') as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=4)
        print(f"Đã lưu thông tin tuần {tuan} vào tệp {ten_tep}")
        return True
    except Exception as e:
        print(f"Lỗi lưu tệp JSON: {e}")
        return False

def load_summary(tuan, thu_muc="data"):
    """
    Hàm đọc thông tin tuần từ tệp JSON
    """
    # Kiểm tra và kết nối Google Drive nếu đang chạy trong Colab
    if IN_COLAB:
        try:
            drive.mount('/content/drive')
            thu_muc = "/content/drive/MyDrive/data"
        except Exception as e:
            print(f"Lỗi kết nối Google Drive: {e}")
            return None
    
    # Tạo đường dẫn tệp JSON
    ten_tep = f"week_{tuan}.json"
    duong_dan = os.path.join(thu_muc, ten_tep)
    
    # Đọc dữ liệu từ tệp JSON
    try:
        with open(duong_dan, 'r', encoding='utf-8') as f:
            du_lieu = json.load(f)
        
        print(f"\n===== THÔNG TIN TUẦN {tuan} =====")
        print(f"Ngày tổng kết: {du_lieu['ngày tổng kết']}")
        print(f"Số học viên: {len(du_lieu['học viên'])}")
        
        # Sử dụng tabulate để hiển thị dữ liệu dạng bảng nếu thư viện có sẵn
        if LIBRARIES_AVAILABLE:
            headers = ["STT", "Họ tên", "Email", "Số bài tập", "Điểm TB"]
            table_data = []
            for idx, hv in enumerate(du_lieu['học viên'], 1):
                table_data.append([
                    idx, 
                    hv['Họ tên'], 
                    hv['Email'], 
                    hv['Số bài tập'], 
                    hv['Điểm TB']
                ])
            print("\nDanh sách học viên:")
            print(tabulate.tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            # Hiển thị theo cách thông thường nếu không có thư viện
            print("\nDanh sách học viên:")
            for idx, hv in enumerate(du_lieu['học viên'], 1):
                print(f"{idx}. {hv['Họ tên']} - Email: {hv['Email']}")
                print(f"   Bài tập hoàn thành: {hv['Số bài tập']} - Điểm TB: {hv['Điểm TB']}")
        
        return du_lieu
    except FileNotFoundError:
        print(f"Không tìm thấy tệp {ten_tep}")
        return None
    except json.JSONDecodeError:
        print(f"Tệp {ten_tep} không đúng định dạng JSON")
        return None
    except Exception as e:
        print(f"Lỗi đọc tệp JSON: {e}")
        return None

def get_formatted_date():
    """
    Hàm lấy ngày hiện tại với định dạng đẹp sử dụng pendulum
    """
    if LIBRARIES_AVAILABLE:
        # Sử dụng pendulum để định dạng ngày tháng
        now = pendulum.now()
        # Định dạng: Thứ Hai, 20/04/2025
        weekday_names = {
            1: "Thứ Hai", 2: "Thứ Ba", 3: "Thứ Tư", 4: "Thứ Năm",
            5: "Thứ Sáu", 6: "Thứ Bảy", 0: "Chủ Nhật"
        }
        weekday = weekday_names[now.day_of_week]
        return f"{weekday}, {now.format('DD/MM/YYYY')}"
    else:
        # Sử dụng datetime nếu pendulum không có sẵn
        return datetime.now().strftime("%d/%m/%Y")

# Hàm chính
def main():
    # Nhập số tuần học
    while True:
        try:
            tuan = int(input("Nhập số tuần học: "))
            if tuan <= 0:
                print("Số tuần học phải là số nguyên dương")
                continue
            break
        except ValueError:
            print("Vui lòng nhập một số nguyên dương")
    
    # Nhập số lượng học viên
    while True:
        try:
            so_luong_hoc_vien = validate_input("so_luong_hoc_vien", input("Nhập số lượng học viên(ít nhất 3 ng ): "))
            break
        except ValueError as e:
            print(f"Lỗi: {e}")

    # Khởi tạo danh sách học viên
    hoc_vien = []

    # Nhập thông tin cho số lượng học viên đã chọn
    for i in range(so_luong_hoc_vien):
        print(f"\nNhập thông tin học viên thứ {i+1}:")
        
        # Nhập và kiểm tra họ tên
        while True:
            try:
                ho_ten = validate_input("ho_ten", input("Họ tên: "))
                break
            except ValueError as e:
                print(f"Lỗi: {e}")
        
        # Nhập và kiểm tra email
        while True:
            try:
                email = validate_input("email", input("Email: "))
                break
            except ValueError as e:
                print(f"Lỗi: {e}")
        
        # Nhập và kiểm tra số bài tập
        while True:
            try:
                so_bai_tap = validate_input("so_bai_tap", input("Số bài tập hoàn thành: "))
                break
            except ValueError as e:
                print(f"Lỗi: {e}")
        
        # Nhập và kiểm tra điểm trung bình
        while True:
            try:
                diem_tb = validate_input("diem_tb", input("Điểm trung bình tuần (0-10): "))
                break
            except ValueError as e:
                print(f"Lỗi: {e}")
        
        hoc_vien.append({
            'Họ tên': ho_ten,
            'Email': email,
            'Số bài tập': so_bai_tap,
            'Điểm TB': diem_tb
        })

    # Lấy ngày hiện tại với định dạng đẹp
    ngay_tk = get_formatted_date()

    # In kết quả tổng hợp
    print(f"\nTổng kết tuần {tuan} cho {len(hoc_vien)} học viên, ngày {ngay_tk}")
    
    # Hiển thị danh sách học viên dạng bảng nếu có thư viện tabulate
    if LIBRARIES_AVAILABLE:
        headers = ["STT", "Họ tên", "Email", "Số bài tập", "Điểm TB"]
        table_data = []
        for idx, hv in enumerate(hoc_vien, 1):
            table_data.append([
                idx, 
                hv['Họ tên'], 
                hv['Email'], 
                hv['Số bài tập'], 
                hv['Điểm TB']
            ])
        print("\nDanh sách học viên:")
        print(tabulate.tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        # Hiển thị theo cách thông thường nếu không có thư viện
        print("Chi tiết học viên:")
        for idx, hv in enumerate(hoc_vien, 1):
            print(f"{idx}. {hv['Họ tên']} - Email: {hv['Email']}")
            print(f"   Bài tập hoàn thành: {hv['Số bài tập']} - Điểm TB: {hv['Điểm TB']}")

    # Tính toán và hiển thị thống kê
    stats = calculate_stats(hoc_vien)
    print("\n===== THỐNG KÊ =====")
    print(f"Điểm trung bình tuần: {stats['diem_tb']}")

    if stats['hv_diem_cao_nhat']:
        print(f"Học viên xuất sắc: {stats['hv_diem_cao_nhat']['Họ tên']} ({stats['hv_diem_cao_nhat']['Điểm TB']})")
        print(f"Học viên cần cố gắng: {stats['hv_diem_thap_nhat']['Họ tên']} ({stats['hv_diem_thap_nhat']['Điểm TB']})")

    print(f"Tỷ lệ hoàn thành: {stats['ty_le_hoan_thanh']}%")
    
    # Lưu thông tin vào tệp JSON
    save_summary(tuan, ngay_tk, hoc_vien)
    
    # Menu chức năng
    while True:
        print("\n===== MENU =====")
        print("1. Xem thông tin tuần")
        print("2. Thoát")
        
        lua_chon = input("Chọn chức năng (1-2): ")
        
        if lua_chon == "1":
            tuan_xem = int(input("Nhập số tuần muốn xem: "))
            load_summary(tuan_xem)
        elif lua_chon == "2":
            print("Kết thúc chương trình")
            break
        else:
            print("Lựa chọn không hợp lệ")

# Chạy chương trình khi thực thi trực tiếp
if __name__ == "__main__":
    main()