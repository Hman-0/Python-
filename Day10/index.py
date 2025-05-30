import pymongo
from pymongo import MongoClient
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OnlineStoreManager:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        try:
            self.client = MongoClient(connection_string)
            self.client.admin.command('ping')
            logging.info("Kết nối MongoDB thành công!")
        except Exception as e:
            logging.error(f"Lỗi kết nối MongoDB: {e}")
            raise
        
        self.db = None
        self.products_collection = None
        self.orders_collection = None

    def setup_database(self):
        try:
            self.db = self.client["online_store"]
            logging.info("Tạo/Kết nối database 'online_store' thành công!")
            existing_collections = self.db.list_collection_names()
            if "products" not in existing_collections:
                self.products_collection = self.db.create_collection("products")
                logging.info("Tạo collection 'products' thành công!")
            else:
                self.products_collection = self.db["products"]
                logging.info("Collection 'products' đã tồn tại!")
            if "orders" not in existing_collections:
                self.orders_collection = self.db.create_collection("orders")
                logging.info("Tạo collection 'orders' thành công!")
            else:
                self.orders_collection = self.db["orders"]
                logging.info("Collection 'orders' đã tồn tại!")
            return True
        except Exception as e:
            logging.error(f"Lỗi tạo database/collection: {e}")
            return False

    def add_data(self):
        try:
            products_data = [
                {"product_id": "SP001", "name": "Áo thun nam", "price": 150000.0, "stock": 50},
                {"product_id": "SP002", "name": "Quần jean nữ", "price": 300000.0, "stock": 30},
                {"product_id": "SP003", "name": "Giày thể thao", "price": 500000.0, "stock": 25},
                {"product_id": "SP004", "name": "Túi xách da", "price": 800000.0, "stock": 15},
                {"product_id": "SP005", "name": "Đồng hồ thông minh", "price": 1200000.0, "stock": 8}
            ]
            if self.products_collection.count_documents({}) == 0:
                result = self.products_collection.insert_many(products_data)
                logging.info(f"Thêm {len(result.inserted_ids)} sản phẩm thành công!")
            else:
                logging.info("Dữ liệu sản phẩm đã tồn tại!")
            orders_data = [
                {"order_id": "DH001", "customer_name": "Nguyễn Văn A", "product_id": "SP001", 
                 "quantity": 2, "total_price": 300000.0, "order_date": "2025-04-10"},
                {"order_id": "DH002", "customer_name": "Trần Thị B", "product_id": "SP002", 
                 "quantity": 1, "total_price": 300000.0, "order_date": "2025-04-10"},
                {"order_id": "DH003", "customer_name": "Lê Văn C", "product_id": "SP003", 
                 "quantity": 1, "total_price": 500000.0, "order_date": "2025-04-11"},
                {"order_id": "DH004", "customer_name": "Nguyễn Văn A", "product_id": "SP004", 
                 "quantity": 1, "total_price": 800000.0, "order_date": "2025-04-11"},
                {"order_id": "DH005", "customer_name": "Phạm Thị D", "product_id": "SP001", 
                 "quantity": 3, "total_price": 450000.0, "order_date": "2025-04-12"},
                {"order_id": "DH006", "customer_name": "Trần Thị B", "product_id": "SP005", 
                 "quantity": 1, "total_price": 1200000.0, "order_date": "2025-04-12"},
                {"order_id": "DH007", "customer_name": "Lê Văn C", "product_id": "SP002", 
                 "quantity": 2, "total_price": 600000.0, "order_date": "2025-04-13"},
                {"order_id": "DH008", "customer_name": "Hoàng Văn E", "product_id": "SP003", 
                 "quantity": 1, "total_price": 500000.0, "order_date": "2025-04-13"},
                {"order_id": "DH009", "customer_name": "Nguyễn Văn A", "product_id": "SP001", 
                 "quantity": 1, "total_price": 150000.0, "order_date": "2025-04-14"},
                {"order_id": "DH010", "customer_name": "Vũ Thị F", "product_id": "SP004", 
                 "quantity": 1, "total_price": 800000.0, "order_date": "2025-04-14"}
            ]
            if self.orders_collection.count_documents({}) == 0:
                result = self.orders_collection.insert_many(orders_data)
                logging.info(f"Thêm {len(result.inserted_ids)} đơn hàng thành công!")
            else:
                logging.info("Dữ liệu đơn hàng đã tồn tại!")
            return True
        except Exception as e:
            logging.error(f"Lỗi thêm dữ liệu: {e}")
            return False

    def query_orders(self, customer_name="Nguyễn Văn A"):
        try:
            print(f"\n=== TRUY VẤN ĐỚN HÀNG ===")
            print(f"Đơn hàng của {customer_name}:")
            customer_orders = self.orders_collection.find({"customer_name": {"$eq": customer_name}})
            for order in customer_orders:
                print(f"- Mã đơn: {order['order_id']}, Sản phẩm: {order['product_id']}, Tổng: {order['total_price']} VNĐ")
            print(f"\nĐơn hàng có giá trị > 500,000 VNĐ (sắp xếp giảm dần, giới hạn 5):")
            high_value_orders = self.orders_collection.find(
                {"total_price": {"$gt": 500000}}
            ).sort("total_price", -1).limit(5)
            for order in high_value_orders:
                print(f"- Mã đơn: {order['order_id']}, Khách hàng: {order['customer_name']}, "
                      f"Sản phẩm: {order['product_id']}, Tổng: {order['total_price']} VNĐ")
            return True
        except Exception as e:
            logging.error(f"Lỗi truy vấn đơn hàng: {e}")
            return False

    def update_order(self, order_id="DH001", new_quantity=3):
        try:
            order = self.orders_collection.find_one({"order_id": order_id})
            if not order:
                logging.warning(f"Không tìm thấy đơn hàng {order_id}")
                return False
            product = self.products_collection.find_one({"product_id": order["product_id"]})
            if not product:
                logging.warning(f"Không tìm thấy sản phẩm {order['product_id']}")
                return False
            new_total_price = product["price"] * new_quantity
            result = self.orders_collection.update_one(
                {"order_id": order_id},
                {"$set": {
                    "quantity": new_quantity,
                    "total_price": new_total_price
                }}
            )
            if result.modified_count > 0:
                print(f"\n=== CẬP NHẬT ĐỚN HÀNG ===")
                print(f"Cập nhật đơn hàng {order_id} thành công!")
                print(f"Số lượng mới: {new_quantity}")
                print(f"Tổng giá mới: {new_total_price} VNĐ")
                return True
            else:
                logging.warning(f"Không có thay đổi nào cho đơn hàng {order_id}")
                return False
        except Exception as e:
            logging.error(f"Lỗi cập nhật đơn hàng: {e}")
            return False

    def delete_order(self, min_price=100000):
        try:
            print(f"\n=== XÓA ĐỚN HÀNG GIÁ TRỊ THẤP ===")
            count_to_delete = self.orders_collection.count_documents(
                {"total_price": {"$lt": min_price}}
            )
            if count_to_delete == 0:
                print(f"Không có đơn hàng nào có giá trị dưới {min_price} VNĐ")
                return True
            result = self.orders_collection.delete_many(
                {"total_price": {"$lt": min_price}}
            )
            print(f"Đã xóa {result.deleted_count} đơn hàng có giá trị dưới {min_price} VNĐ")
            return True
        except Exception as e:
            logging.error(f"Lỗi xóa đơn hàng: {e}")
            return False

    def generate_report(self):
        try:
            print(f"\n=== BÁO CÁO CỬA HÀNG ===")
            pipeline = [
                {"$group": {
                    "_id": "$product_id",
                    "total_revenue": {"$sum": "$total_price"},
                    "total_quantity": {"$sum": "$quantity"}
                }},
                {"$sort": {"total_revenue": -1}}
            ]
            revenue_by_product = self.orders_collection.aggregate(pipeline)
            print("Doanh thu theo sản phẩm:")
            for item in revenue_by_product:
                print(f"- Sản phẩm {item['_id']}: Doanh thu {item['total_revenue']} VNĐ "
                      f"(Đã bán: {item['total_quantity']} sản phẩm)")
            low_stock_count = self.products_collection.count_documents(
                {"stock": {"$lt": 10}}
            )
            print(f"- Sản phẩm tồn kho thấp: {low_stock_count} sản phẩm")
            if low_stock_count > 0:
                print("Chi tiết sản phẩm tồn kho thấp:")
                low_stock_products = self.products_collection.find({"stock": {"$lt": 10}})
                for product in low_stock_products:
                    print(f"  + {product['name']} (ID: {product['product_id']}): "
                          f"Còn lại {product['stock']} sản phẩm")
            return True
        except Exception as e:
            logging.error(f"Lỗi tạo báo cáo: {e}")
            return False

    def cleanup_database(self, confirm=False):
        try:
            if not confirm:
                print(f"\n=== CẢNH BÁO ===")
                print("Bạn có chắc chắn muốn xóa toàn bộ dữ liệu đơn hàng?")
                print("Thao tác này không thể hoàn tác!")
                return False
            if "orders" in self.db.list_collection_names():
                self.orders_collection.drop()
                print(f"\n=== DỌN DẸP DỮ LIỆU ===")
                print("Đã xóa collection 'orders' thành công!")
                return True
            else:
                print("Collection 'orders' không tồn tại!")
                return False
        except Exception as e:
            logging.error(f"Lỗi xóa collection: {e}")
            return False

    def close_connection(self):
        try:
            self.client.close()
            logging.info("Đã đóng kết nối MongoDB!")
        except Exception as e:
            logging.error(f"Lỗi đóng kết nối: {e}")

def main():
    print("=== HỆ THỐNG QUẢN LÝ ĐỚN HÀNG CỬA HÀNG TRỰC TUYẾN ===\n")
    try:
        store_manager = OnlineStoreManager()
        print("1. Thiết lập cơ sở dữ liệu...")
        if not store_manager.setup_database():
            print("Lỗi thiết lập database!")
            return
        print("\n2. Thêm dữ liệu mẫu...")
        if not store_manager.add_data():
            print("Lỗi thêm dữ liệu!")
            return
        print("\n3. Truy vấn đơn hàng...")
        store_manager.query_orders("Nguyễn Văn A")
        print("\n4. Cập nhật đơn hàng...")
        store_manager.update_order("DH001", 3)
        print("\n5. Xóa đơn hàng giá trị thấp...")
        store_manager.delete_order(200000)
        print("\n6. Tạo báo cáo doanh thu...")
        store_manager.generate_report()
        print("\n7. Tùy chọn dọn dẹp dữ liệu...")
        user_input = input("Bạn có muốn dọn dẹp dữ liệu (xóa collection 'orders') không? (y/n): ")
        if user_input.lower() == "y":
            store_manager.cleanup_database(confirm=True)
        else:
            print("Không thực hiện xóa collection để bảo toàn dữ liệu")
        print("\n=== HOÀN THÀNH TẤT CẢ CÁC THAO TÁC ===")
    except Exception as e:
        logging.error(f"Lỗi trong chương trình chính: {e}")
    finally:
        if 'store_manager' in locals():
            store_manager.close_connection()

if __name__ == "__main__":
    main()