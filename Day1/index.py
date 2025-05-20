# =============================================================================
# CHƯƠNG TRÌNH QUẢN LÝ CỬA HÀNG SÁCH NHỎ
# =============================================================================
# Tác giả: AI Assistant
# Ngày tạo: Ngày hiện tại
# Mô tả: Chương trình giúp quản lý cửa hàng sách với các chức năng:
#   - Tính tổng tiền hóa đơn dựa trên số lượng sách và giá
#   - Kiểm tra trạng thái sách (còn hàng/hết hàng)
#   - Tạo mã giảm giá đơn giản dựa trên loại khách hàng
#   - In ra danh sách các cuốn sách bán chạy (dựa trên số lượng bán)
# =============================================================================

# =============================================================================
# KHỞI TẠO DỮ LIỆU
# =============================================================================

# Danh sách sách trong cửa hàng
# Mỗi cuốn sách được biểu diễn bằng một dictionary với các thông tin:
# - ten_sach: Tên của cuốn sách
# - gia: Giá bán của cuốn sách (VNĐ)
# - so_luong_ton_kho: Số lượng sách còn trong kho
# - so_luong_da_ban: Số lượng sách đã bán được
danh_sach_sach = [
    {
        "ten_sach": "Đắc Nhân Tâm",
        "gia": 85000.0,
        "so_luong_ton_kho": 10,
        "so_luong_da_ban": 150
    },
    {
        "ten_sach": "Nhà Giả Kim",
        "gia": 65000.0,
        "so_luong_ton_kho": 5,
        "so_luong_da_ban": 120
    },
    {
        "ten_sach": "Tuổi Trẻ Đáng Giá Bao Nhiêu",
        "gia": 70000.0,
        "so_luong_ton_kho": 0,
        "so_luong_da_ban": 200
    },
    {
        "ten_sach": "Tôi Thấy Hoa Vàng Trên Cỏ Xanh",
        "gia": 60000.0,
        "so_luong_ton_kho": 15,
        "so_luong_da_ban": 80
    },
    {
        "ten_sach": "Cà Phê Cùng Tony",
        "gia": 90000.0,
        "so_luong_ton_kho": 8,
        "so_luong_da_ban": 100
    }
]

# Thông tin khách hàng mẫu
# - ten_khach_hang: Tên của khách hàng
# - loai_khach_hang: Loại khách hàng ("thường" hoặc "VIP")
ten_khach_hang = "Nguyễn Duy Mạnh "
loai_khach_hang = "VIP"  # "thường" hoặc "VIP"

# =============================================================================
# CÁC HÀM XỬ LÝ
# =============================================================================

def calculate_bill(ten_sach, so_luong_mua, loai_khach_hang):
    """
    Tính toán hóa đơn dựa trên tên sách, số lượng mua và loại khách hàng
    
    Args:
        ten_sach (str): Tên cuốn sách cần mua
        so_luong_mua (int): Số lượng sách cần mua
        loai_khach_hang (str): Loại khách hàng ("thường" hoặc "VIP")
        
    Returns:
        tuple: (tổng tiền sau giảm giá (float), thông báo (str))
               Nếu sách hết hàng hoặc đầu vào không hợp lệ, trả về (0.0, thông báo lỗi)
    
    Example:
        >>> calculate_bill("Đắc Nhân Tâm", 2, "VIP")
        (153000.0, 'Thành công')
        >>> calculate_bill("Tuổi Trẻ Đáng Giá Bao Nhiêu", 1, "thường")
        (0.0, 'Sách hết hàng')
    """
    # Kiểm tra đầu vào
    if not isinstance(so_luong_mua, int) or so_luong_mua <= 0:
        return 0.0, "Số lượng mua phải là số nguyên dương"
    
    # Tìm sách trong danh sách
    sach_can_mua = None
    for sach in danh_sach_sach:
        if sach["ten_sach"] == ten_sach:
            sach_can_mua = sach
            break
    
    # Kiểm tra xem sách có tồn tại không
    if sach_can_mua is None:
        return 0.0, f"Không tìm thấy sách '{ten_sach}' trong cửa hàng"
    
    # Kiểm tra xem sách có còn hàng không
    if sach_can_mua["so_luong_ton_kho"] == 0:
        return 0.0, "Sách hết hàng"
    
    # Kiểm tra xem có đủ số lượng không
    if sach_can_mua["so_luong_ton_kho"] < so_luong_mua:
        return 0.0, f"Số lượng sách trong kho không đủ. Chỉ còn {sach_can_mua['so_luong_ton_kho']} cuốn"
    
    # Tính tổng tiền
    tong_tien = float(sach_can_mua["gia"]) * so_luong_mua
    
    # Áp dụng giảm giá nếu là khách VIP
    if loai_khach_hang.upper() == "VIP":
        # Giảm 10% cho khách VIP
        tong_tien = tong_tien * 0.9  # hoặc tong_tien -= tong_tien * 0.1
    
    return tong_tien, "Thành công"
 
def kiem_tra_trang_thai_sach(sach):
    """
    Kiểm tra trạng thái của sách (còn hàng/hết hàng)
    
    Args:
        sach (dict): Thông tin cuốn sách cần kiểm tra, bao gồm:
                    - ten_sach: Tên sách
                    - gia: Giá sách
                    - so_luong_ton_kho: Số lượng còn trong kho
                    - so_luong_da_ban: Số lượng đã bán
        
    Returns:
        str: Trạng thái của sách ("Còn hàng" hoặc "Hết hàng")
    
    Example:
        >>> sach = {"ten_sach": "Đắc Nhân Tâm", "gia": 85000.0, "so_luong_ton_kho": 10, "so_luong_da_ban": 150}
        >>> kiem_tra_trang_thai_sach(sach)
        'Còn hàng'
    """
    # Kiểm tra số lượng tồn kho
    if sach["so_luong_ton_kho"] > 0:
        return "Còn hàng"
    else:
        return "Hết hàng"


def tao_ma_giam_gia(loai_khach_hang):
    """
    Tạo mã giảm giá dựa trên loại khách hàng
    
    Args:
        loai_khach_hang (str): Loại khách hàng ("thường" hoặc "VIP")
        
    Returns:
        float: Phần trăm giảm giá (0.15 cho VIP, 0.05 cho khách thường)
    
    Example:
        >>> tao_ma_giam_gia("VIP")
        0.15
        >>> tao_ma_giam_gia("thường")
        0.05
    """
    # Kiểm tra loại khách hàng và trả về phần trăm giảm giá tương ứng
    if loai_khach_hang.upper() == "VIP":
        return 0.15  # Giảm 15% cho khách VIP
    else:
        return 0.05  # Giảm 5% cho khách thường


def tinh_tong_tien_hoa_don(danh_sach_mua, loai_khach_hang):
    """
    Tính tổng tiền hóa đơn dựa trên danh sách sách mua và loại khách hàng
    
    Args:
        danh_sach_mua (list): Danh sách các cuốn sách và số lượng mua
                             Mỗi phần tử là một dict với các key:
                             - ten_sach: Tên sách cần mua
                             - so_luong: Số lượng sách cần mua
        loai_khach_hang (str): Loại khách hàng để áp dụng giảm giá
        
    Returns:
        tuple: (tổng tiền trước giảm giá, tổng tiền sau giảm giá)
               Nếu có lỗi (không đủ số lượng), trả về (0, 0)
    
    Example:
        >>> danh_sach_mua = [{"ten_sach": "Đắc Nhân Tâm", "so_luong": 2}]
        >>> tinh_tong_tien_hoa_don(danh_sach_mua, "VIP")
        (170000.0, 144500.0)
    """
    tong_tien = 0
    
    # Tính tổng tiền trước khi giảm giá
    for item in danh_sach_mua:
        ten_sach = item["ten_sach"]
        so_luong = item["so_luong"]
        
        # Tìm sách trong danh sách
        for sach in danh_sach_sach:
            if sach["ten_sach"] == ten_sach:
                # Kiểm tra xem có đủ số lượng trong kho không
                if sach["so_luong_ton_kho"] >= so_luong:
                    # Tính tiền cho cuốn sách này và cộng vào tổng
                    tong_tien += sach["gia"] * so_luong
                else:
                    # Thông báo lỗi nếu không đủ số lượng
                    print(f"Lỗi: Sách '{ten_sach}' không đủ số lượng. Chỉ còn {sach['so_luong_ton_kho']} cuốn.")
                    return 0, 0
                break
    
    # Áp dụng giảm giá dựa trên loại khách hàng
    phan_tram_giam_gia = tao_ma_giam_gia(loai_khach_hang)
    tien_giam = tong_tien * phan_tram_giam_gia
    tong_tien_sau_giam_gia = tong_tien - tien_giam
    
    return tong_tien, tong_tien_sau_giam_gia


def cap_nhat_so_luong_sach(danh_sach_mua):
    """
    Cập nhật số lượng sách trong kho và số lượng đã bán sau khi mua
    
    Args:
        danh_sach_mua (list): Danh sách các cuốn sách và số lượng mua
                             Mỗi phần tử là một dict với các key:
                             - ten_sach: Tên sách cần mua
                             - so_luong: Số lượng sách cần mua
    
    Returns:
        None: Hàm này không trả về giá trị mà chỉ cập nhật danh_sach_sach
    """
    # Duyệt qua từng cuốn sách trong danh sách mua
    for item in danh_sach_mua:
        ten_sach = item["ten_sach"]
        so_luong = item["so_luong"]
        
        # Tìm sách trong danh sách cửa hàng
        for sach in danh_sach_sach:
            if sach["ten_sach"] == ten_sach:
                # Kiểm tra và cập nhật số lượng
                if sach["so_luong_ton_kho"] >= so_luong:
                    # Giảm số lượng tồn kho
                    sach["so_luong_ton_kho"] -= so_luong
                    # Tăng số lượng đã bán
                    sach["so_luong_da_ban"] += so_luong
                break


def in_danh_sach_sach_ban_chay(so_luong=3):
    """
    In danh sách các cuốn sách bán chạy nhất
    
    Args:
        so_luong (int, optional): Số lượng sách bán chạy cần hiển thị. Mặc định là 3.
    
    Returns:
        None: Hàm này không trả về giá trị mà chỉ in kết quả ra màn hình
    """
    # Sắp xếp danh sách sách theo số lượng đã bán (giảm dần)
    # Sử dụng lambda function để chỉ định key sắp xếp
    sach_ban_chay = sorted(danh_sach_sach, key=lambda x: x["so_luong_da_ban"], reverse=True)
    
    # In tiêu đề
    print("\n=== DANH SÁCH SÁCH BÁN CHẠY ===")
    
    # In thông tin sách bán chạy
    for i in range(min(so_luong, len(sach_ban_chay))):
        sach = sach_ban_chay[i]
        print(f"{i+1}. {sach['ten_sach']} - Đã bán: {sach['so_luong_da_ban']} cuốn")


def hien_thi_danh_sach_sach():
    """
    Hiển thị thông tin của tất cả các cuốn sách trong cửa hàng
    
    Returns:
        None: Hàm này không trả về giá trị mà chỉ in kết quả ra màn hình
    """
    # In tiêu đề
    print("\n=== DANH SÁCH SÁCH TRONG CỬA HÀNG ===")
    
    # In header của bảng
    print(f"{'Tên sách':<30} {'Giá':<15} {'Tồn kho':<15} {'Đã bán':<15} {'Trạng thái':<15}")
    print("-" * 90)  # Đường kẻ ngang
    
    # In thông tin từng cuốn sách
    for sach in danh_sach_sach:
        # Lấy trạng thái của sách
        trang_thai = kiem_tra_trang_thai_sach(sach)
        
        # In thông tin sách với định dạng bảng
        # :<30 nghĩa là căn trái và chiếm 30 ký tự
        # :,.0f định dạng số với dấu phẩy ngăn cách hàng nghìn
        print(f"{sach['ten_sach']:<30} {sach['gia']:<15,.0f} {sach['so_luong_ton_kho']:<15} {sach['so_luong_da_ban']:<15} {trang_thai:<15}")




def check_stock(ten_sach, so_luong_mua):
    """
    Kiểm tra trạng thái sách và phân loại sách theo giá
    
    Args:
        ten_sach (str): Tên cuốn sách cần kiểm tra
        so_luong_mua (int): Số lượng sách muốn mua
        
    Returns:
        tuple: (bool, str, str)
               - bool: True nếu còn đủ hàng, False nếu không đủ
               - str: Thông báo trạng thái ("Còn hàng" hoặc "Hết hàng hoặc không đủ")
               - str: Phân loại sách theo giá ("Sách giá rẻ", "Sách trung bình", "Sách cao cấp")
    
    Example:
        >>> check_stock("Đắc Nhân Tâm", 2)
        (True, 'Còn hàng', 'Sách trung bình')
        >>> check_stock("Tuổi Trẻ Đáng Giá Bao Nhiêu", 1)
        (False, 'Hết hàng hoặc không đủ', 'Sách trung bình')
    """
    # Tìm sách trong danh sách
    sach_can_kiem_tra = None
    for sach in danh_sach_sach:
        if sach["ten_sach"] == ten_sach:
            sach_can_kiem_tra = sach
            break
    
    # Nếu không tìm thấy sách
    if sach_can_kiem_tra is None:
        return False, f"Không tìm thấy sách '{ten_sach}' trong cửa hàng", "Không xác định"
    
    # Kiểm tra số lượng tồn kho
    if sach_can_kiem_tra["so_luong_ton_kho"] >= so_luong_mua:
        trang_thai = True
        thong_bao = "Còn hàng"
    else:
        trang_thai = False
        thong_bao = "Hết hàng hoặc không đủ"
    
    # Phân loại sách theo giá sử dụng match-case (Python 3.10+)
    gia = sach_can_kiem_tra["gia"]
    
    # Sử dụng match-case để phân loại sách theo giá
    match True:
        case _ if gia < 50000:
            phan_loai = "Sách giá rẻ"
        case _ if 50000 <= gia <= 100000:
            phan_loai = "Sách trung bình"
        case _:
            phan_loai = "Sách cao cấp"
    
    return trang_thai, thong_bao, phan_loai


# =============================================================================
# TẠO MÃ GIẢM GIÁ VÀ THỐNG KÊ SÁCH BÁN CHẠY
# =============================================================================

# Lambda function để tạo mã giảm giá dựa trên loại khách hàng
tao_ma_giam_gia_lambda = lambda ten, loai: ten.upper() + "_VIP" if loai.upper() == "VIP" else ten.upper() + "_REG"

def thong_ke_sach_ban_chay():
    """
    Thống kê và hiển thị các cuốn sách bán chạy (số lượng bán > 10)
    
    Returns:
        None: Hàm này không trả về giá trị mà chỉ in kết quả ra màn hình
    """
    print("\n=== DANH SÁCH SÁCH BÁN CHẠY (SỐ LƯỢNG BÁN > 10) ===")
    
    # Sử dụng for loop để duyệt danh sách sách
    for sach in danh_sach_sach:
        if sach["so_luong_da_ban"] > 10:
            print(f"- {sach['ten_sach']}: Đã bán {sach['so_luong_da_ban']} cuốn")

def tim_sach_ban_chay_nhat():
    """
    Tìm và hiển thị thông tin cuốn sách bán chạy nhất
    
    Returns:
        dict: Thông tin cuốn sách bán chạy nhất
    """
    if not danh_sach_sach:
        print("Không có sách trong cửa hàng!")
        return None
    
    # Sử dụng while loop để tìm sách bán chạy nhất
    i = 0
    sach_ban_chay_nhat = danh_sach_sach[0]
    
    while i < len(danh_sach_sach):
        if danh_sach_sach[i]["so_luong_da_ban"] > sach_ban_chay_nhat["so_luong_da_ban"]:
            sach_ban_chay_nhat = danh_sach_sach[i]
        i += 1
    
    # In thông tin sách bán chạy nhất
    print("\n=== SÁCH BÁN CHẠY NHẤT ===")
    print(f"Tên sách: {sach_ban_chay_nhat['ten_sach']}")
    print(f"Số lượng đã bán: {sach_ban_chay_nhat['so_luong_da_ban']} cuốn")
    print(f"Giá: {sach_ban_chay_nhat['gia']:,.0f} VNĐ")
    
    return sach_ban_chay_nhat


# =============================================================================
# CHƯƠNG TRÌNH CHÍNH (CẬP NHẬT)
# =============================================================================
def main():
    """
    Hàm chính của chương trình, điều phối các chức năng
    """
    # Hiển thị thông tin chào mừng
    print("=== CHƯƠNG TRÌNH QUẢN LÝ CỬA HÀNG SÁCH ===")
    print(f"Xin chào, {ten_khach_hang}!")
    print(f"Loại khách hàng: {loai_khach_hang}")
    
    # Hiển thị danh sách sách ban đầu
    hien_thi_danh_sach_sach()
    
    # 1. Tạo mã giảm giá bằng lambda function
    ma_giam_gia = tao_ma_giam_gia_lambda(ten_khach_hang, loai_khach_hang)
    print(f"\nMã giảm giá của bạn: {ma_giam_gia}")
    
    # 2. Gọi hàm calculate_bill với ví dụ
    ten_sach_mua = "Đắc Nhân Tâm"
    so_luong_mua = 2
    print(f"\n=== TÍNH HÓA ĐƠN CHO {ten_sach_mua} (SỐ LƯỢNG: {so_luong_mua}) ===")
    tien_sach, thong_bao = calculate_bill(ten_sach_mua, so_luong_mua, loai_khach_hang)
    
    if thong_bao == "Thành công":
        print(f"Tổng tiền: {tien_sach:,.0f} VNĐ")
    else:
        print(f"Lỗi: {thong_bao}")
    
    # 3. Gọi hàm check_stock với ví dụ
    ten_sach_kiem_tra = "Nhà Giả Kim"
    so_luong_kiem_tra = 3
    print(f"\n=== KIỂM TRA TRẠNG THÁI SÁCH {ten_sach_kiem_tra} (SỐ LƯỢNG: {so_luong_kiem_tra}) ===")
    trang_thai, thong_bao, phan_loai = check_stock(ten_sach_kiem_tra, so_luong_kiem_tra)
    
    print(f"Trạng thái: {thong_bao}")
    print(f"Phân loại: {phan_loai}")
    
    # 4. Thống kê sách bán chạy
    thong_ke_sach_ban_chay()
    
    # 5. Tìm sách bán chạy nhất
    tim_sach_ban_chay_nhat()
    
    # Giả lập danh sách mua hàng
    print("\n=== THỰC HIỆN MUA HÀNG ===")
    danh_sach_mua = [
        {"ten_sach": "Đắc Nhân Tâm", "so_luong": 2},
        {"ten_sach": "Nhà Giả Kim", "so_luong": 1}
    ]
    
    # Hiển thị thông tin hóa đơn
    print("\n=== HÓA ĐƠN MUA HÀNG ===")
    print(f"Khách hàng: {ten_khach_hang} (Loại: {loai_khach_hang})")
    print(f"Mã giảm giá: {ma_giam_gia}")
    print("Danh sách sách mua:")
    
    # Tính tổng tiền hóa đơn
    tong_tien_hoa_don = 0
    for item in danh_sach_mua:
        ten_sach = item["ten_sach"]
        so_luong = item["so_luong"]
        
        # Tính hóa đơn cho cuốn sách này
        tien_sach, thong_bao = calculate_bill(ten_sach, so_luong, loai_khach_hang)
        
        if thong_bao == "Thành công":
            # Tìm thông tin sách để hiển thị
            for sach in danh_sach_sach:
                if sach["ten_sach"] == ten_sach:
                    gia_goc = sach["gia"] * so_luong
                    print(f"- {ten_sach} x {so_luong} = {gia_goc:,.0f} VNĐ", end="")
                    
                    # Hiển thị thông tin giảm giá nếu là khách VIP
                    if loai_khach_hang.upper() == "VIP":
                        print(f" (Sau giảm giá 10%: {tien_sach:,.0f} VNĐ)")
                    else:
                        print()
                    
                    # Cộng vào tổng tiền hóa đơn
                    tong_tien_hoa_don += tien_sach
                    break
        else:
            # Hiển thị thông báo lỗi
            print(f"- {ten_sach} x {so_luong}: {thong_bao}")
    
    # Hiển thị tổng tiền hóa đơn
    print(f"\nTổng tiền hóa đơn: {tong_tien_hoa_don:,.0f} VNĐ")
    
    # Cập nhật số lượng sách sau khi mua
    cap_nhat_so_luong_sach(danh_sach_mua)
    
    print("\nCảm ơn bạn đã mua hàng!")
    
    # Hiển thị danh sách sách sau khi cập nhật
    hien_thi_danh_sach_sach()


# Điểm bắt đầu của chương trình
# Chỉ chạy hàm main() khi file được chạy trực tiếp (không phải import)
if __name__ == "__main__":
    main()