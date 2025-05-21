class Book:
    def __init__(self, ma_sach, tieu_de, tac_gia, so_luong_ton):
        self.__ma_sach = ma_sach
        self.tieu_de = tieu_de
        self.tac_gia = tac_gia
        self.so_luong_ton = so_luong_ton if so_luong_ton >= 0 else 0
    
    def get_info(self):
        return f"Mã sách: {self.__ma_sach}, Tiêu đề: {self.tieu_de}, Tác giả: {self.tac_gia}, Tồn kho: {self.so_luong_ton}"
    
    def update_stock(self, so_luong_moi):
        if so_luong_moi >= 0:
            self.so_luong_ton = so_luong_moi
        else:
            print("Số lượng tồn kho không thể âm")

class PhysicalBook(Book):
    def __init__(self, ma_sach, tieu_de, tac_gia, so_luong_ton, trang_thai):
        super().__init__(ma_sach, tieu_de, tac_gia, so_luong_ton)
        self.trang_thai = trang_thai
    
    def get_info(self):
        return f"{super().get_info()}, Trạng thái: {self.trang_thai}"

class EBook(Book):
    def __init__(self, ma_sach, tieu_de, tac_gia, so_luong_ton, dinh_dang):
        super().__init__(ma_sach, tieu_de, tac_gia, so_luong_ton)
        self.dinh_dang = dinh_dang
    
    def get_info(self):
        return f"{super().get_info()}, Định dạng: {self.dinh_dang}"