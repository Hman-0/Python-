from book_management import Book, PhysicalBook, EBook
from library_management import User, Library, display_books

def main():
    # Khởi tạo danh sách sách
    sach1 = PhysicalBook("P001", "Lập trình OOP", "Trần Thị B", 20, "Mới")
    sach2 = PhysicalBook("P002", "Cấu trúc dữ liệu", "Nguyễn Văn C", -5, "Cũ")  # Test số lượng âm
    sach3 = PhysicalBook("P003", "Giải thuật", "Lê Thị D", 15, "Trung bình")
    sach4 = EBook("E001", "Python Cơ bản", "Võ Văn E", 0, "PDF")
    sach5 = EBook("E002", "Machine Learning", "Phạm Thị F", 50, "EPUB")
    
    # Tạo thư viện và thêm sách
    thu_vien = Library([sach1, sach2, sach3, sach4, sach5])
    
    # Duyệt sách bằng Iterator
    print("\n=== DANH SÁCH SÁCH TRONG THƯ VIỆN (SẮP XẾP THEO TÊN) ===")
    for sach in thu_vien:
        print(sach.get_info())
    
    # Hiển thị sách bằng hàm display_books
    print("\n=== HIỂN THỊ ĐA HÌNH ===")
    display_books(thu_vien.ds_sach)
    
    # Tạo người dùng và thao tác mượn/trả sách
    user1 = User("U001", "Nguyễn Văn A")
    user2 = User("U002", "Trần Thị B")
    
    # User1 mượn sách
    user1.borrow_book("P001", thu_vien)
    user1.borrow_book("E002", thu_vien)
    
    # Hiển thị trước khi trả
    print("\n=== TRẠNG THÁI MƯỢN SÁCH TRƯỚC KHI TRẢ ===")
    print(f"{user1.ten}: {user1.get_borrowed_books()}")

    
    # User1 trả sách
    user1.return_book("P001")
    
    # Hiển thị sau khi trả
    print("\n=== TRẠNG THÁI MƯỢN SÁCH SAU KHI TRẢ ===")
    print(f"{user1.ten}: {user1.get_borrowed_books()}")
    user1.borrow_book("INVALID_ID", thu_vien)  # Sẽ không được thêm vào
    
    # User2 mượn sách
    user2.borrow_book("P003", thu_vien)
    user2.borrow_book("E001", thu_vien)
    
    # User1 trả sách
    user1.return_book("P001")
    
    # In thông tin mượn sách
    print("\n=== THÔNG TIN MƯỢN SÁCH ===")
    print(f"{user1.ten}: {user1.get_borrowed_books()}")
    print(f"{user2.ten}: {user2.get_borrowed_books()}")

if __name__ == "__main__":
    main()