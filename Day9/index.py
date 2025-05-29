import mysql.connector
from mysql.connector import errorcode

# Thông tin kết nối MySQL (sửa lại cho phù hợp)
DB_CONFIG = {
    'user': 'root',
    'password': 'your_password',  # Thay bằng mật khẩu MySQL của bạn
    'host': 'localhost',
    'raise_on_warnings': True
}

DB_NAME = 'project_progress'

def get_connection(database=None):
    config = DB_CONFIG.copy()
    if database:
        config['database'] = database
    return mysql.connector.connect(**config)

def setup_database():
    """Tạo database và các bảng nếu chưa tồn tại."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Tạo database nếu chưa có
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        conn.database = DB_NAME

        # Tạo bảng members
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                role VARCHAR(50)
            )
        """)
        # Tạo bảng weekly_progress
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weekly_progress (
                progress_id INT AUTO_INCREMENT PRIMARY KEY,
                member_id INT,
                week_number INT,
                hours_worked FLOAT CHECK (hours_worked >= 0),
                tasks_completed INT,
                notes TEXT,
                FOREIGN KEY (member_id) REFERENCES members(member_id)
            )
        """)
        print("Đã thiết lập database và các bảng.")
    except mysql.connector.Error as err:
        print("Lỗi khi thiết lập database:", err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def add_data():
    """Thêm dữ liệu mẫu vào bảng members và weekly_progress."""
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()

        # Thêm 5 thành viên
        members = [
            ("An", "Developer"),
            ("Bình", "Tester"),
            ("Cường", "Project Manager"),
            ("Dương", "Developer"),
            ("Hà", "Designer")
        ]
        cursor.executemany("INSERT INTO members (name, role) VALUES (%s, %s)", members)
        conn.commit()

        # Lấy member_id để thêm tiến độ
        cursor.execute("SELECT member_id FROM members")
        member_ids = [row[0] for row in cursor.fetchall()]

        # Thêm 10 bản ghi tiến độ cho 2 tuần
        progresses = [
            (member_ids[0], 1, 40.0, 5, "Hoàn thành đúng hạn"),
            (member_ids[1], 1, 38.5, 4, "Cần hỗ trợ thêm"),
            (member_ids[2], 1, 42.0, 6, "Quản lý tốt tiến độ"),
            (member_ids[3], 1, 36.0, 3, "Chưa hoàn thành hết nhiệm vụ"),
            (member_ids[4], 1, 39.0, 4, "Thiết kế đẹp"),
            (member_ids[0], 2, 41.0, 6, "Vượt chỉ tiêu"),
            (member_ids[1], 2, 37.0, 4, "Ổn định"),
            (member_ids[2], 2, 43.0, 7, "Xuất sắc"),
            (member_ids[3], 2, 35.0, 3, "Cần cải thiện"),
            (member_ids[4], 2, 40.0, 5, "Tiến bộ rõ rệt")
        ]
        cursor.executemany("""
            INSERT INTO weekly_progress (member_id, week_number, hours_worked, tasks_completed, notes)
            VALUES (%s, %s, %s, %s, %s)
        """, progresses)
        conn.commit()
        print("Đã thêm dữ liệu mẫu.")
    except mysql.connector.Error as err:
        print("Lỗi khi thêm dữ liệu:", err)
    finally:
        cursor.close()
        conn.close()

def query_progress(week_number):
    """Truy vấn tiến độ của một tuần cụ thể."""
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()
        query = """
            SELECT m.name, w.hours_worked, w.tasks_completed, w.notes
            FROM weekly_progress w
            JOIN members m ON w.member_id = m.member_id
            WHERE w.week_number = %s
            ORDER BY w.tasks_completed DESC
            LIMIT 5
        """
        cursor.execute(query, (week_number,))
        results = cursor.fetchall()
        print(f"Tuần {week_number}:")
        for row in results:
            print(f"- {row[0]}: {row[1]} giờ, {row[2]} nhiệm vụ, Ghi chú: {row[3]}")
    except mysql.connector.Error as err:
        print("Lỗi khi truy vấn tiến độ:", err)
    finally:
        cursor.close()
        conn.close()

def update_progress(progress_id, hours_worked, notes):
    """Cập nhật số giờ làm việc và ghi chú của một bản ghi tiến độ."""
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE weekly_progress
            SET hours_worked = %s, notes = %s
            WHERE progress_id = %s
        """, (hours_worked, notes, progress_id))
        conn.commit()
        if cursor.rowcount:
            print(f"Đã cập nhật bản ghi progress_id={progress_id}.")
        else:
            print("Không tìm thấy bản ghi để cập nhật.")
    except mysql.connector.Error as err:
        print("Lỗi khi cập nhật tiến độ:", err)
    finally:
        cursor.close()
        conn.close()

def delete_progress(week_number):
    """Xóa các bản ghi tiến độ của một tuần cụ thể."""
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM weekly_progress WHERE week_number = %s", (week_number,))
        conn.commit()
        if cursor.rowcount:
            print(f"Đã xóa {cursor.rowcount} bản ghi tuần {week_number}.")
        else:
            print("Không có bản ghi nào bị xóa.")
    except mysql.connector.Error as err:
        print("Lỗi khi xóa tiến độ:", err)
    finally:
        cursor.close()
        conn.close()

def generate_summary():
    """Tạo báo cáo tổng kết cho từng thành viên."""
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()
        query = """
            SELECT m.name, SUM(w.hours_worked), SUM(w.tasks_completed)
            FROM members m
            JOIN weekly_progress w ON m.member_id = w.member_id
            GROUP BY m.member_id
        """
        cursor.execute(query)
        results = cursor.fetchall()
        print("Báo cáo tổng kết:")
        for row in results:
            print(f"- {row[0]}: Tổng {row[1]} giờ, {row[2]} nhiệm vụ")
    except mysql.connector.Error as err:
        print("Lỗi khi tạo báo cáo:", err)
    finally:
        cursor.close()
        conn.close()

def cleanup_database():
    """Xóa bảng weekly_progress nếu tồn tại."""
    try:
        conn = get_connection(DB_NAME)
        cursor = conn.cursor()
        # Kiểm tra bảng có tồn tại không
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = %s AND table_name = 'weekly_progress'
        """, (DB_NAME,))
        if cursor.fetchone()[0]:
            cursor.execute("DROP TABLE weekly_progress")
            conn.commit()
            print("Đã xóa bảng weekly_progress.")
        else:
            print("Bảng weekly_progress không tồn tại.")
    except mysql.connector.Error as err:
        print("Lỗi khi dọn dẹp database:", err)
    finally:
        cursor.close()
        conn.close()

def main():
    setup_database()
    add_data()
    query_progress(1)  # Truy vấn tuần 1
    # Lấy một progress_id để cập nhật (ví dụ: id=1)
    update_progress(1, 45.0, "Hoàn thành sớm")
    delete_progress(2)  # Xóa dữ liệu tuần 2
    generate_summary()
    # cleanup_database()  # Bỏ comment dòng này nếu muốn xóa bảng weekly_progress

if __name__ == "__main__":
    main()