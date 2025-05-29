import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def create_sample_data():
    print("🔄 Đang tạo dữ liệu mẫu...")
    
    data = {
        'Ten': ['An', 'Binh', 'Chi', 'Duc', 'Manh'] * 3,
        'Tuan': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
        'Bai_tap': [5, 4, 6, 3, 5, 6, 5, 7, 4, 6, 7, 6, 8, 5, 7],
        'Diem': [8.5, 7.0, 9.2, 6.5, 8.0, 9.0, 7.5, 9.5, 7.0, 8.5, 9.2, 8.0, 9.8, 7.5, 9.0]
    }
    
    df = pd.DataFrame(data)
    
    try:
        df.to_csv('progress.csv', index=False, encoding='utf-8')
        print("✅ Đã tạo và lưu dữ liệu vào progress.csv")
        print("\n📊 Dữ liệu mẫu:")
        print(df.to_string(index=False))
        return df
    except Exception as e:
        print(f"❌ Lỗi khi lưu file CSV: {e}")
        return None

def analyze_weekly_progress(week=None):
    print(f"\n🔍 Đang phân tích tiến độ học tập...")
    
    try:
        if not os.path.exists('progress.csv'):
            print("❌ File progress.csv không tồn tại!")
            return
            
        df = pd.read_csv('progress.csv', encoding='utf-8')
        
        if df.empty:
            print("❌ Dữ liệu trống!")
            return
            
        weeks = df['Tuan'].unique()
        
        for w in sorted(weeks):
            week_data = df[df['Tuan'] == w]
            
            avg_exercises = week_data['Bai_tap'].mean()
            avg_score = week_data['Diem'].mean()
            top_student = week_data.loc[week_data['Diem'].idxmax()]
            
            print(f"\n📈 Phân tích tuần {w}:")
            print(f"- Bài tập trung bình: {avg_exercises:.1f}")
            print(f"- Điểm trung bình: {avg_score:.2f}")
            print(f"- Học viên xuất sắc: {top_student['Ten']} ({top_student['Diem']})")
        
        print(f"\n🏆 Học viên hoàn thành trên 4 bài tập:")
        high_performers = df[df['Bai_tap'] > 4]
        for _, row in high_performers.iterrows():
            print(f"- {row['Ten']}: Tuần {row['Tuan']}, {row['Bai_tap']} bài tập, {row['Diem']} điểm")
            
    except Exception as e:
        print(f"❌ Lỗi khi phân tích dữ liệu: {e}")

def visualize_progress():
    print(f"\n📊 Đang tạo biểu đồ trực quan...")
    
    try:
        df = pd.read_csv('progress.csv', encoding='utf-8')
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        students = df['Ten'].unique()
        colors = plt.cm.Set3(np.linspace(0, 1, len(students)))
        
        for i, student in enumerate(students):
            student_data = df[df['Ten'] == student].sort_values('Tuan')
            ax1.plot(student_data['Tuan'], student_data['Diem'], 
                    marker='o', label=student, color=colors[i], linewidth=2, markersize=6)
        
        ax1.set_title('Xu hướng điểm trung bình qua các tuần', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Tuần', fontsize=12)
        ax1.set_ylabel('Điểm', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xticks(df['Tuan'].unique())
        
        weekly_exercises = df.groupby('Tuan')['Bai_tap'].mean()
        bars = ax2.bar(weekly_exercises.index, weekly_exercises.values, 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8, width=0.6)
        
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        ax2.set_title('Số bài tập hoàn thành trung bình theo tuần', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Tuần', fontsize=12)
        ax2.set_ylabel('Số bài tập', fontsize=12)
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_xticks(weekly_exercises.index)
        
        plt.tight_layout()
        plt.savefig('trend_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Đã lưu biểu đồ vào trend_comparison.png")
        
    except Exception as e:
        print(f"❌ Lỗi khi tạo biểu đồ: {e}")

def generate_weekly_report():
    print(f"\n📋 Đang tạo báo cáo tổng kết...")
    
    try:
        df = pd.read_csv('progress.csv', encoding='utf-8')
        
        summary = df.groupby('Ten').agg({
            'Bai_tap': 'sum',
            'Diem': 'mean'
        }).round(2)
        
        progress_data = df.pivot(index='Ten', columns='Tuan', values='Diem')
        first_week = progress_data.columns[0]
        last_week = progress_data.columns[-1]
        
        improvement = progress_data[last_week] - progress_data[first_week]
        most_improved = improvement.idxmax()
        max_improvement = improvement.max()
        
        report_content = "🎓 BÁO CÁO TỔNG KẾT TIẾN ĐỘ HỌC TẬP\n"
        report_content += "=" * 45 + "\n\n"
        
        report_content += "📊 THỐNG KÊ TỔNG KẾT:\n"
        for student, data in summary.iterrows():
            report_content += f"- Tổng bài tập của {student}: {data['Bai_tap']} bài\n"
            report_content += f"- Điểm trung bình của {student}: {data['Diem']:.2f}\n\n"
        
        report_content += f"🏆 Học viên tiến bộ nhất: {most_improved} (tăng {max_improvement:.1f} điểm)\n"
        
        with open('report.txt', 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print("✅ Đã lưu báo cáo vào report.txt")
        print("\n" + report_content)
        
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(summary)))
        
        wedges, texts, autotexts = plt.pie(summary['Bai_tap'], 
                                          labels=summary.index,
                                          autopct='%1.1f%%',
                                          colors=colors,
                                          startangle=90,
                                          explode=[0.05] * len(summary))
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        for text in texts:
            text.set_fontsize(12)
            text.set_fontweight('bold')
        
        plt.title('Tỷ lệ đóng góp bài tập của từng học viên', 
                 fontsize=16, fontweight='bold', pad=20)
        
        total_exercises = summary['Bai_tap'].sum()
        plt.figtext(0.02, 0.95, f"Tổng số bài tập: {total_exercises}", 
                   fontsize=12, fontweight='bold')
        plt.figtext(0.02, 0.92, f"Học viên tiến bộ nhất: {most_improved}", 
                   fontsize=12, fontweight='bold', color='green')
        
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('contribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Đã lưu biểu đồ tròn vào contribution.png")
        
    except Exception as e:
        print(f"❌ Lỗi khi tạo báo cáo: {e}")

def main():
    print("🚀 KHỞI ĐỘNG CÔNG CỤ PHÂN TÍCH TIẾN ĐỘ HỌC TẬP")
    print("=" * 50)
    
    try:
        df = create_sample_data()
        if df is None:
            print("❌ Không thể tạo dữ liệu. Chương trình dừng.")
            return
        
        analyze_weekly_progress()
        
        visualize_progress()
        
        generate_weekly_report()
        
        print(f"\n🎉 HOÀN THÀNH! Đã tạo các file:")
        print("📄 progress.csv - Dữ liệu gốc")
        print("📄 report.txt - Báo cáo tổng kết")
        print("🖼️ trend_comparison.png - Biểu đồ xu hướng và so sánh")
        print("🖼️ contribution.png - Biểu đồ tỷ lệ đóng góp")
        
    except Exception as e:
        print(f"❌ Lỗi trong quá trình thực thi: {e}")

if __name__ == "__main__":
    main()