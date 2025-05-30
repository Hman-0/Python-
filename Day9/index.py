import mysql.connector
from mysql.connector import Error
import sys

class ProjectProgressManager:
    def __init__(self):
        """Khởi tạo kết nối MySQL"""
        self.connection = None
        self.cursor = None
        
    def connect_to_mysql(self, host='localhost', user='root', password=''):
        """Kết nối đến MySQL server"""
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            print("✓ Kết nối MySQL thành công!")
            return True
        except Error as e:
            print(f"✗ Lỗi kết nối MySQL: {e}")
            return False
    
    def setup_database(self):
        """
        Tạo cơ sở dữ liệu và các bảng cần thiết
        - Tạo database project_progress
        - Tạo bảng members và weekly_progress
        """
        try:
     
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS project_progress")
            print("✓ Database 'project_progress' đã được tạo/kiểm tra")
      
            self.cursor.execute("USE project_progress")
            
       
            create_members_table = """
            CREATE TABLE IF NOT EXISTS members (
                member_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                role VARCHAR(50) NOT NULL
            )
            """
            self.cursor.execute(create_members_table)
            print("✓ Bảng 'members' đã được tạo/kiểm tra")
            
         
            create_progress_table = """
            CREATE TABLE IF NOT EXISTS weekly_progress (
                progress_id INT AUTO_INCREMENT PRIMARY KEY,
                member_id INT NOT NULL,
                week_number INT NOT NULL,
                hours_worked FLOAT NOT NULL CHECK (hours_worked >= 0),
                tasks_completed INT NOT NULL DEFAULT 0,
                notes TEXT,
                FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE CASCADE
            )
            """
            self.cursor.execute(create_progress_table)
            print("✓ Bảng 'weekly_progress' đã được tạo/kiểm tra")
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"✗ Lỗi tạo database/bảng: {e}")
            return False
    
    def add_data(self):
        """
        Thêm dữ liệu mẫu vào các bảng
        - Thêm 5 thành viên
        - Thêm 10+ bản ghi tiến độ qua 2 tuần
        """
        try:

            self.cursor.execute("SELECT COUNT(*) FROM members")
            member_count = self.cursor.fetchone()[0]
            
            if member_count == 0:
              
                members_data = [
                    ('Nguyễn Văn An', 'Developer'),
                    ('Trần Thị Bình', 'Designer'),
                    ('Lê Văn Cường', 'Tester'),
                    ('Phạm Thị Dung', 'Project Manager'),
                    ('Hoàng Văn Em', 'DevOps')
                ]
                
                insert_member_query = "INSERT INTO members (name, role) VALUES (%s, %s)"
                self.cursor.executemany(insert_member_query, members_data)
                print(f"✓ Đã thêm {len(members_data)} thành viên")
            else:
                print("✓ Dữ liệu thành viên đã tồn tại")
       
            self.cursor.execute("SELECT COUNT(*) FROM weekly_progress")
            progress_count = self.cursor.fetchone()[0]
            
            if progress_count == 0:

                progress_data = [
  
                    (1, 1, 40.5, 8, 'Hoàn thành module đăng nhập'),
                    (2, 1, 35.0, 6, 'Thiết kế giao diện chính'),
                    (3, 1, 42.0, 12, 'Test các chức năng cơ bản'),
                    (4, 1, 38.5, 5, 'Quản lý tiến độ dự án'),
                    (5, 1, 45.0, 7, 'Cấu hình server và database'),
                    
             
                    (1, 2, 44.0, 10, 'Phát triển API REST'),
                    (2, 2, 40.0, 8, 'Hoàn thiện UI/UX'),
                    (3, 2, 38.5, 15, 'Kiểm tra tích hợp hệ thống'),
                    (4, 2, 42.0, 6, 'Lập kế hoạch sprint tiếp theo'),
                    (5, 2, 41.5, 9, 'Triển khai môi trường production'),
                    
   
                    (1, 3, 36.0, 7, 'Tối ưu hóa hiệu suất'),
                    (3, 3, 40.0, 11, 'Regression testing')
                ]
                
                insert_progress_query = """
                INSERT INTO weekly_progress (member_id, week_number, hours_worked, tasks_completed, notes) 
                VALUES (%s, %s, %s, %s, %s)
                """
                self.cursor.executemany(insert_progress_query, progress_data)
                print(f"✓ Đã thêm {len(progress_data)} bản ghi tiến độ")
            else:
                print("✓ Dữ liệu tiến độ đã tồn tại")
            
            self.connection.commit()
            return True
            
        except Error as e:
            print(f"✗ Lỗi thêm dữ liệu: {e}")
            self.connection.rollback()
            return False
    
    def query_progress(self, week_number):
        """
        Truy vấn tiến độ của một tuần cụ thể
        Sử dụng JOIN, WHERE, ORDER BY, LIMIT
        """
        try:
            query = """
            SELECT m.name, wp.hours_worked, wp.tasks_completed, wp.notes
            FROM members m
            JOIN weekly_progress wp ON m.member_id = wp.member_id
            WHERE wp.week_number = %s
            ORDER BY wp.tasks_completed DESC
            LIMIT 5
            """
            
            self.cursor.execute(query, (week_number,))
            results = self.cursor.fetchall()
            
            if results:
                print(f"\n📊 Tuần {week_number}:")
                for name, hours, tasks, notes in results:
                    print(f"- {name}: {hours} giờ, {tasks} nhiệm vụ, Ghi chú: {notes}")
            else:
                print(f"❌ Không có dữ liệu cho tuần {week_number}")
            
            return results
            
        except Error as e:
            print(f"✗ Lỗi truy vấn tiến độ: {e}")
            return []
    
    def update_progress(self, progress_id, new_hours, new_notes):
        """
        Cập nhật thông tin tiến độ của một bản ghi cụ thể
        Sử dụng UPDATE và WHERE
        """
        try:
        
            check_query = "SELECT COUNT(*) FROM weekly_progress WHERE progress_id = %s"
            self.cursor.execute(check_query, (progress_id,))
            
            if self.cursor.fetchone()[0] == 0:
                print(f"❌ Không tìm thấy bản ghi với ID {progress_id}")
                return False
            
     
            update_query = """
            UPDATE weekly_progress 
            SET hours_worked = %s, notes = %s 
            WHERE progress_id = %s
            """
            
            self.cursor.execute(update_query, (new_hours, new_notes, progress_id))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                print(f"✓ Đã cập nhật bản ghi ID {progress_id}: {new_hours} giờ, ghi chú: '{new_notes}'")
                return True
            else:
                print(f"❌ Không thể cập nhật bản ghi ID {progress_id}")
                return False
                
        except Error as e:
            print(f"✗ Lỗi cập nhật tiến độ: {e}")
            self.connection.rollback()
            return False
    
    def delete_progress(self, week_number):
        """
        Xóa tất cả bản ghi tiến độ của một tuần cụ thể
        Sử dụng DELETE và WHERE
        """
        try:
         
            check_query = "SELECT COUNT(*) FROM weekly_progress WHERE week_number = %s"
            self.cursor.execute(check_query, (week_number,))
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                print(f"❌ Không có bản ghi nào của tuần {week_number} để xóa")
                return False
            
       
            delete_query = "DELETE FROM weekly_progress WHERE week_number = %s"
            self.cursor.execute(delete_query, (week_number,))
            self.connection.commit()
            
            deleted_count = self.cursor.rowcount
            print(f"✓ Đã xóa {deleted_count} bản ghi của tuần {week_number}")
            return True
            
        except Error as e:
            print(f"✗ Lỗi xóa dữ liệu: {e}")
            self.connection.rollback()
            return False
    
    def generate_summary(self):
        """
        Tạo báo cáo tổng kết cho tất cả thành viên
        Sử dụng SELECT, JOIN, GROUP BY
        """
        try:
            query = """
            SELECT m.name, 
                   SUM(wp.hours_worked) as total_hours, 
                   SUM(wp.tasks_completed) as total_tasks
            FROM members m
            LEFT JOIN weekly_progress wp ON m.member_id = wp.member_id
            GROUP BY m.member_id, m.name
            ORDER BY total_hours DESC
            """
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            
            print("\n📈 Báo cáo tổng kết:")
            for name, total_hours, total_tasks in results:
                hours = total_hours if total_hours else 0
                tasks = total_tasks if total_tasks else 0
                print(f"- {name}: Tổng {hours} giờ, {tasks} nhiệm vụ")
            
            return results
            
        except Error as e:
            print(f"✗ Lỗi tạo báo cáo: {e}")
            return []
    
    def cleanup_database(self, confirm=False):
        """
        Xóa bảng weekly_progress nếu được yêu cầu
        Sử dụng DROP TABLE
        """
        try:
            if not confirm:
                response = input("Bạn có chắc chắn muốn xóa bảng 'weekly_progress'? (y/N): ")
                if response.lower() != 'y':
                    print("Hủy bỏ thao tác xóa bảng")
                    return False
            check_query = """
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'project_progress' 
            AND table_name = 'weekly_progress'
            """
            self.cursor.execute(check_query)
            if self.cursor.fetchone()[0] == 0:
                print("Bảng 'weekly_progress' không tồn tại")
                return False
            self.cursor.execute("DROP TABLE weekly_progress")
            self.connection.commit()
            print("Đã xóa bảng 'weekly_progress'")
            return True
        except Error as e:
            print(f"Lỗi xóa bảng: {e}")
            return False
    
    def close_connection(self):
        """Đóng kết nối database"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("✓ Đã đóng kết nối MySQL")
        except Error as e:
            print(f"✗ Lỗi đóng kết nối: {e}")


def main():
    """
    Hàm chính - chạy toàn bộ hệ thống quản lý tiến độ dự án
    """
    print("🚀 Khởi động Hệ thống Quản lý Tiến độ Dự án Hàng tuần")
    print("=" * 60)
    

    manager = ProjectProgressManager()
    
    try:

        print("\n📡 BƯỚC 1: Kết nối MySQL")
        if not manager.connect_to_mysql(
            host='localhost',
            user='root',
            password='' 
        ):
            print("❌ Không thể tiếp tục do lỗi kết nối")
            return
        

        print("\n🏗️  BƯỚC 2: Tạo Database và Bảng")
        if not manager.setup_database():
            print("❌ Không thể tạo database/bảng")
            return
        
        
        print("\n📝 BƯỚC 3: Thêm Dữ liệu Mẫu")
        manager.add_data()

        print("\n🔍 BƯỚC 4: Truy vấn Tiến độ")
        manager.query_progress(1)
        manager.query_progress(2)
        

        print("\n✏️  BƯỚC 5: Cập nhật Dữ liệu")
        manager.update_progress(1, 45.0, "Hoàn thành sớm hơn dự kiến")
        
     
        print("\n🗑️  BƯỚC 6: Xóa Dữ liệu")
        manager.delete_progress(3)
        
   
        print("\n📊 BƯỚC 7: Báo cáo Tổng kết")
        manager.generate_summary()
        

        print("BƯỚC 8: Dọn dẹp (Tùy chọn)")
        dapan = input("Bạn có muốn xóa bảng weekly_progress không? (y/N): ")
        if dapan.lower() == 'y':
            manager.cleanup_database(confirm=True)
        print("Hoàn thành tất cả các bước!")
        
        print("\n✅ Hoàn thành tất cả các bước!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Chương trình bị ngắt bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
    finally:
        # Đóng kết nối
        manager.close_connection()
        print("\n👋 Cảm ơn bạn đã sử dụng hệ thống!")


if __name__ == "__main__":
    main()