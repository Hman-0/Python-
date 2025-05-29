import numpy as np
from scipy import stats
from scipy.optimize import minimize
import os

def create_performance_data():
    np.random.seed(42)
    performance_data = []
    for week in range(4):
        week_data = []
        for member in range(5):
            hours = np.random.normal(40, 3)
            hours = max(30, min(50, hours))
            tasks = int(hours / 8 + np.random.normal(0, 0.5))
            tasks = max(1, tasks)
            week_data.append([hours, tasks])
        performance_data.append(week_data)
    performance_array = np.array(performance_data)
    np.save('performance.npy', performance_array)
    print("✓ Đã tạo và lưu dữ liệu hiệu suất vào performance.npy")
    return performance_array

def basic_analysis(week_index=0):
    try:
        if not os.path.exists('performance.npy'):
            raise FileNotFoundError("Tệp performance.npy không tồn tại!")
        data = np.load('performance.npy')
        if week_index >= len(data):
            raise IndexError(f"Tuần {week_index + 1} không tồn tại trong dữ liệu!")
        week_data = data[week_index]
        hours = week_data[:, 0]
        tasks = week_data[:, 1]
        avg_hours = np.mean(hours)
        std_hours = np.std(hours)
        total_tasks = np.sum(tasks)
        best_member_index = np.argmax(tasks)
        best_member_tasks = tasks[best_member_index]
        print(f"\n--- Phân tích tuần {week_index + 1} ---")
        print(f"- Trung bình giờ làm: {avg_hours:.2f} giờ")
        print(f"- Độ lệch chuẩn giờ: {std_hours:.2f}")
        print(f"- Tổng nhiệm vụ: {int(total_tasks)} nhiệm vụ")
        print(f"- Thành viên xuất sắc: Thành viên {best_member_index + 1} ({int(best_member_tasks)} nhiệm vụ)")
        return {
            'avg_hours': avg_hours,
            'std_hours': std_hours,
            'total_tasks': total_tasks,
            'best_member': best_member_index,
            'best_tasks': best_member_tasks
        }
    except Exception as e:
        print(f"Lỗi trong phân tích cơ bản: {e}")
        return None

def advanced_analysis():
    try:
        if not os.path.exists('performance.npy'):
            raise FileNotFoundError("Tệp performance.npy không tồn tại!")
        data = np.load('performance.npy')
        all_hours = data[:, :, 0].flatten()
        all_tasks = data[:, :, 1].flatten()
        slope, intercept, r_value, p_value, std_err = stats.linregress(all_hours, all_tasks)
        correlation, p_corr = stats.pearsonr(all_hours, all_tasks)
        mean_hours = np.mean(all_hours)
        std_hours = np.std(all_hours)
        lower_bound = mean_hours - 2 * std_hours
        upper_bound = mean_hours + 2 * std_hours
        outliers = all_hours[(all_hours < lower_bound) | (all_hours > upper_bound)]
        print(f"\n--- Phân tích nâng cao ---")
        print(f"Hồi quy tuyến tính:")
        print(f"- Độ dốc: {slope:.4f}")
        print(f"- Hệ số tương quan: {correlation:.4f}")
        if len(outliers) > 0:
            print(f"- Giá trị ngoại lai (giờ làm): {[f'{x:.2f}' for x in outliers]}")
        else:
            print(f"- Giá trị ngoại lai (giờ làm): Không có")
        return {
            'slope': slope,
            'intercept': intercept,
            'correlation': correlation,
            'outliers': outliers
        }
    except Exception as e:
        print(f"Lỗi trong phân tích nâng cao: {e}")
        return None

def optimize_workload(regression_params, num_members=5):
    try:
        if regression_params is None:
            print("Không thể tối ưu hóa: thiếu tham số hồi quy")
            return None
        slope = regression_params['slope']
        intercept = regression_params['intercept']
        def objective(hours):
            return -(slope * np.sum(hours) + intercept * num_members)
        constraints = [
            {'type': 'ineq', 'fun': lambda x: 200 - np.sum(x)},
        ]
        bounds = [(30, 50) for _ in range(num_members)]
        initial_guess = np.array([40.0] * num_members)
        result = minimize(
            objective,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        if result.success:
            optimal_hours = result.x
            print(f"\n--- Tối ưu hóa phân bổ công việc ---")
            print(f"Phân bổ giờ làm tuần tới:")
            for i, hours in enumerate(optimal_hours):
                print(f"- Thành viên {i + 1}: {hours:.1f} giờ")
            print(f"Tổng giờ: {np.sum(optimal_hours):.1f}/200 giờ")
            predicted_tasks = slope * np.sum(optimal_hours) + intercept * num_members
            print(f"Dự kiến tổng nhiệm vụ: {predicted_tasks:.1f}")
            return optimal_hours
        else:
            print(f"Tối ưu hóa thất bại: {result.message}")
            return None
    except Exception as e:
        print(f"Lỗi trong tối ưu hóa: {e}")
        return None

def main():
    print("=== CÔNG CỤ PHÂN TÍCH HIỆU SUẤT TUẦN LÀM VIỆC ===")
    try:
        print("\n1. Tạo dữ liệu hiệu suất...")
        performance_data = create_performance_data()
        print("\n2. Phân tích thống kê cơ bản...")
        basic_stats = basic_analysis(week_index=0)
        print("\n3. Phân tích nâng cao...")
        regression_params = advanced_analysis()
        print("\n4. Tối ưu hóa phân bổ công việc...")
        optimal_schedule = optimize_workload(regression_params)
        print("\n=== HOÀN THÀNH PHÂN TÍCH ===")
        if os.path.exists('performance.npy'):
            data = np.load('performance.npy')
            total_weeks = data.shape[0]
            total_members = data.shape[1]
            print(f"\nTổng quan: Đã phân tích {total_weeks} tuần với {total_members} thành viên")
    except Exception as e:
        print(f"Lỗi trong chương trình chính: {e}")

if __name__ == "__main__":
    main()