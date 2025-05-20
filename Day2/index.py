import numpy as np


events = [
    {"id": "EV001", "name": "Hội chợ sách", "ticket_price": 50000.0, "tickets_left": 200},
    {"id": "EV002", "name": "Triển lãm nghệ thuật", "ticket_price": 75000.0, "tickets_left": 150},
    {"id": "EV003", "name": "Workshop nấu ăn", "ticket_price": 100000.0, "tickets_left": 50},
    {"id": "EV004", "name": "Hội chợ ẩm thực", "ticket_price": 60000.0, "tickets_left": 180},
    {"id": "EV005", "name": "Biểu diễn âm nhạc", "ticket_price": 120000.0, "tickets_left": 100}
]

sponsors = {
    "SP001": ("Công ty A", 5000000.0),
    "SP002": ("Công ty B", 3000000.0),
    "SP003": ("Công ty C", 4000000.0)
}


events_with_sales = set()

ticket_history = []

def manage_events():
    """Function to manage events with CRUD operations"""
    global events
    
    while True:
        print("\n=== QUẢN LÝ SỰ KIỆN ===")
        print("1. Thêm sự kiện")
        print("2. Xóa sự kiện")
        print("3. Cập nhật số lượng vé")
        print("4. Xem thông tin sự kiện")
        print("5. Xem tất cả sự kiện")
        print("6. Tính giá vé trung bình")
        print("7. Quay lại")
        
        choice = input("Chọn chức năng: ")
        
        if choice == "1":
            # Add new event
            event_id = input("Nhập mã sự kiện: ")
            if any(e['id'] == event_id for e in events):
                print("Mã sự kiện đã tồn tại!")
                continue
                
            name = input("Nhập tên sự kiện: ")
            try:
                price = float(input("Nhập giá vé: "))
                tickets = int(input("Nhập số lượng vé: "))
                if price <= 0 or tickets < 0:
                    raise ValueError
            except ValueError:
                print("Giá vé và số lượng vé phải là số dương!")
                continue
                
            events.append({
                "id": event_id,
                "name": name,
                "ticket_price": price,
                "tickets_left": tickets
            })
            print("Thêm sự kiện thành công!")
            
        elif choice == "2":
            # Delete event
            event_id = input("Nhập mã sự kiện cần xóa: ")
            for i, e in enumerate(events):
                if e['id'] == event_id:
                    del events[i]
                    print("Xóa sự kiện thành công!")
                    break
            else:
                print("Không tìm thấy sự kiện!")
                
        elif choice == "3":
            # Update tickets
            event_id = input("Nhập mã sự kiện cần cập nhật: ")
            for e in events:
                if e['id'] == event_id:
                    try:
                        new_tickets = int(input("Nhập số lượng vé mới: "))
                        if new_tickets < 0:
                            raise ValueError
                        e['tickets_left'] = new_tickets
                        print("Cập nhật thành công!")
                    except ValueError:
                        print("Số lượng vé phải là số nguyên dương!")
                    break
            else:
                print("Không tìm thấy sự kiện!")
                
        elif choice == "4":
            # View event info
            event_id = input("Nhập mã sự kiện cần xem: ")
            for e in events:
                if e['id'] == event_id:
                    print(f"\nThông tin sự kiện {event_id}:")
                    print(f"Tên: {e['name']}")
                    print(f"Giá vé: {e['ticket_price']:,.0f} VNĐ")
                    print(f"Số lượng vé còn lại: {e['tickets_left']}")
                    break
            else:
                print("Không tìm thấy sự kiện!")
                
        elif choice == "5":
            # List all events
            print("\n=== DANH SÁCH SỰ KIỆN ===")
            for e in events:
                print(f"{e['id']}: {e['name']} - Giá vé: {e['ticket_price']:,.0f} VNĐ - Còn lại: {e['tickets_left']} vé")
                
        elif choice == "6":
         
            prices = np.array([e['ticket_price'] for e in events])
            avg_price = np.mean(prices)
            print(f"Giá vé trung bình: {avg_price:,.0f} VNĐ")
            
        elif choice == "7":
            break
        else:
            print("Lựa chọn không hợp lệ!")

def manage_sponsors():
    """Function to manage sponsors with CRUD operations"""
    global sponsors
    
    while True:
        print("\n=== QUẢN LÝ NHÀ TÀI TRỢ ===")
        print("1. Thêm nhà tài trợ")
        print("2. Xóa nhà tài trợ")
        print("3. Cập nhật số tiền tài trợ")
        print("4. Xem thông tin nhà tài trợ")
        print("5. Xem tất cả nhà tài trợ")
        print("6. Quay lại")
        
        choice = input("Chọn chức năng: ")
        
        if choice == "1":
            # Add new sponsor
            sponsor_id = input("Nhập mã nhà tài trợ: ")
            if sponsor_id in sponsors:
                print("Mã nhà tài trợ đã tồn tại!")
                continue
                
            name = input("Nhập tên nhà tài trợ: ")
            try:
                amount = float(input("Nhập số tiền tài trợ: "))
                if amount <= 0:
                    raise ValueError
            except ValueError:
                print("Số tiền tài trợ phải là số dương!")
                continue
                
            sponsors[sponsor_id] = (name, amount)
            print("Thêm nhà tài trợ thành công!")
            
        elif choice == "2":
            # Delete sponsor
            sponsor_id = input("Nhập mã nhà tài trợ cần xóa: ")
            if sponsor_id in sponsors:
                del sponsors[sponsor_id]
                print("Xóa nhà tài trợ thành công!")
            else:
                print("Không tìm thấy nhà tài trợ!")
                
        elif choice == "3":
            # Update sponsor amount
            sponsor_id = input("Nhập mã nhà tài trợ cần cập nhật: ")
            if sponsor_id in sponsors:
                try:
                    new_amount = float(input("Nhập số tiền tài trợ mới: "))
                    if new_amount <= 0:
                        raise ValueError
                    name = sponsors[sponsor_id][0]
                    sponsors[sponsor_id] = (name, new_amount)
                    print("Cập nhật thành công!")
                except ValueError:
                    print("Số tiền tài trợ phải là số dương!")
            else:
                print("Không tìm thấy nhà tài trợ!")
                
        elif choice == "4":
            # View sponsor info
            sponsor_id = input("Nhập mã nhà tài trợ cần xem: ")
            if sponsor_id in sponsors:
                name, amount = sponsors[sponsor_id]
                print(f"\nThông tin nhà tài trợ {sponsor_id}:")
                print(f"Tên: {name}")
                print(f"Số tiền tài trợ: {amount:,.0f} VNĐ")
            else:
                print("Không tìm thấy nhà tài trợ!")
                
        elif choice == "5":
            # List all sponsors
            print("\n=== DANH SÁCH NHÀ TÀI TRỢ ===")
            for sponsor_id, (name, amount) in sponsors.items():
                print(f"{sponsor_id}: {name} - Tài trợ: {amount:,.0f} VNĐ")
                
        elif choice == "6":
            break
        else:
            print("Lựa chọn không hợp lệ!")

def process_tickets():
    """Function to process ticket sales"""
    global events, events_with_sales, ticket_history
    
    while True:
        print("\n=== QUẢN LÝ VÉ ĐÃ BÁN ===")
        print("1. Thêm giao dịch bán vé")
        print("2. Kiểm tra sự kiện có vé bán")
        print("3. Xem lịch sử bán vé")
        print("4. Xóa giao dịch không hợp lệ")
        print("5. Quay lại")
        
        choice = input("Chọn chức năng: ")
        
        if choice == "1":
            # Add ticket transaction
            event_id = input("Nhập mã sự kiện: ")
            
            # Find the event
            event = None
            for e in events:
                if e['id'] == event_id:
                    event = e
                    break
            
            if not event:
                print("Không tìm thấy sự kiện!")
                continue
                
            ticket_id = f"TICKET_{len(ticket_history)+1:03d}"
            
            try:
                quantity = int(input("Nhập số lượng vé bán: "))
                if quantity <= 0:
                    print("Số lượng vé phải lớn hơn 0!")
                    continue
                
                if quantity > event['tickets_left']:
                    print(f"Chỉ còn {event['tickets_left']} vé cho sự kiện này!")
                    continue
                
                # Update tickets left
                event['tickets_left'] -= quantity
                
                # Add to sales set
                events_with_sales.add(event_id)
                
                # Add to history
                ticket_history.append({
                    "event_id": event_id,
                    "ticket_id": ticket_id,
                    "quantity": quantity
                })
                
                print(f"Thêm giao dịch {ticket_id} thành công!")
                
            except ValueError:
                print("Số lượng vé phải là số nguyên dương!")
                
        elif choice == "2":
            # Check if event has sales
            event_id = input("Nhập mã sự kiện cần kiểm tra: ")
            if event_id in events_with_sales:
                print("Sự kiện này đã có vé bán trong ngày!")
            else:
                print("Sự kiện này chưa có vé bán trong ngày.")
                
        elif choice == "3":
            # View ticket sales history
            print("\n=== LỊCH SỬ BÁN VÉ ===")
            for transaction in ticket_history:
                print(f"Mã vé: {transaction['ticket_id']} - Sự kiện: {transaction['event_id']} - Số lượng: {transaction['quantity']}")
                
        elif choice == "4":
            
            removed = 0
            for i in range(len(ticket_history)-1, -1, -1):
                if ticket_history[i]['quantity'] == 0:
                    del ticket_history[i]
                    removed += 1
            
            print(f"Đã xóa {removed} giao dịch không hợp lệ!")
            
        elif choice == "5":
            break
        else:
            print("Lựa chọn không hợp lệ!")

def generate_report():
    """Function to generate statistics report"""
    global events, ticket_history
    
    print("\n=== BÁO CÁO THỐNG KÊ ===")
    
    # Events with low tickets
    low_ticket_events = [e for e in events if e['tickets_left'] < 20]
    if low_ticket_events:
        print("\nSự kiện sắp hết vé:")
        for e in low_ticket_events:
            print(f"- {e['name']} (còn {e['tickets_left']} vé)")
    else:
        print("\nKhông có sự kiện nào sắp hết vé.")
    
    # Total remaining ticket value
    ticket_values = np.array([e['ticket_price'] * e['tickets_left'] for e in events])
    total_value = np.sum(ticket_values)
    print(f"\nTổng giá trị vé còn lại: {total_value:,.0f} VNĐ")
    
    # Events with sales
    unique_events_with_sales = {t['event_id'] for t in ticket_history}
    if unique_events_with_sales:
        print("\nSự kiện đã bán vé:")
        for event_id in unique_events_with_sales:
            print(f"- {event_id}")
    else:
        print("\nChưa có sự kiện nào bán vé.")

def main():
    """Main function to run the program"""
    while True:
        print("\n=== CHƯƠNG TRÌNH QUẢN LÝ SỰ KIỆN VĂN HÓA ===")
        print("1. Quản lý sự kiện")
        print("2. Quản lý nhà tài trợ")
        print("3. Quản lý vé đã bán")
        print("4. Báo cáo thống kê")
        print("5. Thoát")
        
        choice = input("Chọn chức năng: ")
        
        if choice == "1":
            manage_events()
        elif choice == "2":
            manage_sponsors()
        elif choice == "3":
            process_tickets()
        elif choice == "4":
            generate_report()
        elif choice == "5":
            print("Cảm ơn đã sử dụng chương trình!")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()