from book_management import Book

class User:
    def __init__(self, ma_nguoi_dung, ten):
        self.__ma_nguoi_dung = ma_nguoi_dung
        self.ten = ten
        self.danh_sach_muon = []
    
    def borrow_book(self, ma_sach, thu_vien):
        # Kiểm tra mã sách hợp lệ và tồn tại trong thư viện
        if isinstance(ma_sach, str) and ma_sach not in self.danh_sach_muon:
            if any(sach._Book__ma_sach == ma_sach for sach in thu_vien.ds_sach):
                self.danh_sach_muon.append(ma_sach)
    
    def return_book(self, ma_sach):
        if ma_sach in self.danh_sach_muon:
            self.danh_sach_muon.remove(ma_sach)
    
    def get_borrowed_books(self):
        return self.danh_sach_muon.copy()

class Library:
    def __init__(self, ds_sach):
        self.ds_sach = ds_sach
    
    def __iter__(self):
        self.index = 0
        self.sorted_books = sorted(self.ds_sach, key=lambda x: x.tieu_de)
        return self
    
    def __next__(self):
        if self.index < len(self.sorted_books):
            result = self.sorted_books[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

def display_books(ds_sach):
    for sach in ds_sach:
        print(sach.get_info())