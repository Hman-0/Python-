import os
import glob

# Constants
FILE_PREFIX = "tuần"
FILE_SUFFIX = ".txt"

# --- Input and Validation Helper Functions ---

def get_int_input(prompt: str, error_message: str = "Lỗi: Vui lòng nhập một số nguyên.", min_value: int = None) -> int:
    """Lấy đầu vào là số nguyên từ người dùng với validation."""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                raise ValueError(f"Giá trị phải lớn hơn hoặc bằng {min_value}.")
            return value
        except ValueError as e:
            print(f"{error_message} ({e})")

def get_float_input(prompt: str, error_message: str = "Lỗi: Vui lòng nhập một số thực.", min_value: float = None) -> float:
    """Lấy đầu vào là số thực từ người dùng với validation."""
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                raise ValueError(f"Giá trị phải lớn hơn hoặc bằng {min_value}.")
            return value
        except ValueError as e:
            print(f"{error_message} ({e})")

def get_string_input(prompt: str, error_message: str = "Lỗi: Nội dung không được để trống.") -> str:
    """Lấy đầu vào là chuỗi không rỗng từ người dùng."""
    while True:
        value = input(prompt)
        if value.strip():
            return value
        print(error_message)

def get_week_number_input(prompt: str) -> int:
    """Lấy số tuần hợp lệ từ người dùng."""
    return get_int_input(prompt, min_value=1, error_message="Lỗi: Số tuần phải là số nguyên dương.")

# --- Core Logic Functions ---

def create_weekly_log():
    """Tạo nhật ký tuần mới và lưu vào file văn bản."""
    print("\n--- Tạo Nhật Ký Tuần Mới ---")
    week = get_week_number_input("Nhập số tuần: ")
    hours = get_float_input("Nhập số giờ làm việc: ", min_value=0)
    tasks = get_int_input("Nhập số nhiệm vụ hoàn thành: ", min_value=0)
    notes = get_string_input("Nhập ghi chú: ")

    filename = f"{FILE_PREFIX}{week}{FILE_SUFFIX}"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Tuần: {week}\n")
            f.write(f"Số giờ làm việc: {hours}\n")
            f.write(f"Nhiệm vụ hoàn thành: {tasks}\n")
            f.write(f"Ghi chú: {notes}\n")
        print(f"\033[92mĐã tạo thành công nhật ký tuần {week} ({filename})\033[0m") # Green color for success
    except IOError as e:
        print(f"\033[91mLỗi khi ghi file: {e}\033[0m") # Red color for error

def read_weekly_log():
    """Đọc nội dung một nhật ký tuần."""
    print("\n--- Đọc Nhật Ký Tuần ---")
    week = get_week_number_input("Nhập số tuần cần đọc: ")
    filename = f"{FILE_PREFIX}{week}{FILE_SUFFIX}"

    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                print(f"\n=== NHẬT KÝ TUẦN {week} ===")
                print(f.read().strip())
                print("=======================")
        else:
            print(f"\033[93mNhật ký tuần {week} không tồn tại.\033[0m") # Yellow color for warning
    except IOError as e:
        print(f"\033[91mLỗi khi đọc file: {e}\033[0m")

def update_weekly_log():
    """Cập nhật nội dung nhật ký tuần (ghi đè toàn bộ)."""
    print("\n--- Cập Nhật Nhật Ký Tuần ---")
    week = get_week_number_input("Nhập số tuần cần cập nhật: ")
    filename = f"{FILE_PREFIX}{week}{FILE_SUFFIX}"

    if not os.path.exists(filename):
        print(f"\033[93mNhật ký tuần {week} không tồn tại để cập nhật.\033[0m")
        create_new = get_string_input(f"Bạn có muốn tạo mới nhật ký cho tuần {week} không? (y/n): ").lower()
        if create_new == 'y':
            create_weekly_log() # Gọi lại hàm tạo nếu người dùng muốn
        return

    print(f"\n🔄 Nhập thông tin mới cho tuần {week} (để trống nếu không muốn thay đổi một mục cụ thể):")
    # Đọc nội dung cũ để hiển thị hoặc giữ lại nếu người dùng không nhập mới
    try:
        with open(filename, 'r', encoding='utf-8') as f_read:
            lines = f_read.readlines()
            current_hours_str = lines[1].split(": ")[1].strip()
            current_tasks_str = lines[2].split(": ")[1].strip()
            current_notes = lines[3].split(": ")[1].strip() if len(lines) > 3 else ""
    except (IOError, IndexError) as e:
        print(f"\033[91mLỗi khi đọc file hiện tại để cập nhật: {e}\033[0m")
        return

    new_hours_str = input(f"Số giờ làm việc (hiện tại: {current_hours_str}): ")
    hours = float(new_hours_str) if new_hours_str.strip() else float(current_hours_str)
    
    new_tasks_str = input(f"Số nhiệm vụ hoàn thành (hiện tại: {current_tasks_str}): ")
    tasks = int(new_tasks_str) if new_tasks_str.strip() else int(current_tasks_str)

    new_notes = input(f"Ghi chú (hiện tại: {current_notes}): ")
    notes = new_notes.strip() if new_notes.strip() else current_notes

    try:
        with open(filename, 'w', encoding='utf-8') as f_write:
            f_write.write(f"Tuần: {week}\n")
            f_write.write(f"Số giờ làm việc: {hours}\n")
            f_write.write(f"Nhiệm vụ hoàn thành: {tasks}\n")
            f_write.write(f"Ghi chú: {notes}\n")
        print(f"\033[92mĐã cập nhật thành công nhật ký tuần {week}\033[0m")
    except IOError as e:
        print(f"\033[91mLỗi khi ghi file cập nhật: {e}\033[0m")

def delete_weekly_log():
    """Xóa tệp nhật ký tuần."""
    print("\n--- Xóa Nhật Ký Tuần ---")
    week = get_week_number_input("Nhập số tuần cần xóa: ")
    filename = f"{FILE_PREFIX}{week}{FILE_SUFFIX}"

    if os.path.exists(filename):
        confirm = get_string_input(f"Bạn có chắc chắn muốn xóa nhật ký tuần {week} ({filename}) không? (y/n): ").lower()
        if confirm == 'y':
            try:
                os.remove(filename)
                print(f"\033[92mĐã xóa thành công nhật ký tuần {week}\033[0m")
            except OSError as e:
                print(f"\033[91mLỗi khi xóa file: {e}\033[0m")
        else:
            print("Hủy bỏ thao tác xóa.")
    else:
        print(f"\033[93mKhông tìm thấy nhật ký tuần {week} để xóa.\033[0m")

def generate_summary():
    """Tạo báo cáo tổng kết từ các file nhật ký."""
    print("\n--- Báo Cáo Tổng Kết ---")
    total_weeks = 0
    total_hours = 0.0
    total_tasks = 0
    log_files = sorted(glob.glob(f"{FILE_PREFIX}*{FILE_SUFFIX}")) # Sắp xếp file theo tên

    if not log_files:
        print("Không có dữ liệu nhật ký nào để tạo báo cáo.")
        return

    print(f"{'File Nhật Ký':<20} | {'Tuần':<5} | {'Giờ LV':<7} | {'N.Vụ HT':<8}")
    print("-" * 55)

    for filename in log_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if len(lines) < 3:
                    print(f"\033[91mBỏ qua file lỗi định dạng: {filename}\033[0m")
                    continue
                
                week_str = lines[0].split(": ")[1].strip()
                hours_str = lines[1].split(": ")[1].strip()
                tasks_str = lines[2].split(": ")[1].strip()

                week = int(week_str)
                hours = float(hours_str)
                tasks = int(tasks_str)

                print(f"{filename:<20} | {week:<5} | {hours:<7.1f} | {tasks:<8}")
                total_weeks += 1
                total_hours += hours
                total_tasks += tasks
        except (IOError, IndexError, ValueError) as e:
            print(f"\033[91mBỏ qua file lỗi ({e}): {filename}\033[0m")
            continue
    
    print("-" * 55)
    print(f"{'Tổng cộng':<20} | {total_weeks:<5} | {total_hours:<7.1f} | {total_tasks:<8}")
    if total_weeks > 0:
        avg_hours_per_week = total_hours / total_weeks
        avg_tasks_per_week = total_tasks / total_weeks
        print(f"{'Trung bình/tuần':<20} | {'':<5} | {avg_hours_per_week:<7.1f} | {avg_tasks_per_week:<8.1f}")
    print("=========================")

# --- Menu and Main Execution ---

MENU_OPTIONS = {
    "1": ("Tạo nhật ký tuần mới", create_weekly_log),
    "2": ("Đọc nhật ký tuần", read_weekly_log),
    "3": ("Cập nhật nhật ký tuần", update_weekly_log),
    "4": ("Xóa nhật ký tuần", delete_weekly_log),
    "5": ("Tạo báo cáo tổng kết", generate_summary),
    "6": ("Thoát", None)  # None for exit action
}

def display_menu():
    """Hiển thị menu chính."""
    print("\n\033[1;36m====== QUẢN LÝ NHẬT KÝ TUẦN LÀM VIỆC ======\033[0m") # Cyan color for title
    for key, (text, _) in MENU_OPTIONS.items():
        print(f"  {key}. {text}")
    print("=============================================")

def main():
    """Menu chính điều khiển chương trình."""
    while True:
        display_menu()
        choice = input("Chọn chức năng (1-6): ")

        if choice in MENU_OPTIONS:
            text, action = MENU_OPTIONS[choice]
            if action:
                action() # Call the corresponding function
            else: # Exit option
                print("\033[1;32mCảm ơn bạn đã sử dụng chương trình! Hẹn gặp lại.\033[0m")
                break
        else:
            print("\033[91mLựa chọn không hợp lệ. Vui lòng nhập một số từ 1 đến 6.\033[0m")

if __name__ == "__main__":
    main()