"""
Module Visualizer
Chứa các hàm vẽ biểu đồ cho dữ liệu Titanic
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizer:
    """Lớp xử lý vẽ biểu đồ"""
    
    def __init__(self, parent_window):
        self.parent = parent_window  # Cửa sổ cha
        self.df = None  # DataFrame chứa dữ liệu
    
    def show_visualization_popup(self, df):
        """Popup chọn loại biểu đồ"""
        if df.empty:
            return  # Không làm gì nếu DataFrame rỗng
        
        self.df = df  # Lưu DataFrame
        
        # Tạo cửa sổ popup
        popup = tk.Toplevel(self.parent)
        popup.title("Chọn Biểu đồ")
        popup.geometry("350x300")
        
        # Tiêu đề
        tk.Label(
            popup,
            text="Chọn loại biểu đồ cần vẽ:",
            font=("Arial", 11, "bold")
        ).pack(pady=10)
        
        chart_type = tk.StringVar()  # Biến lưu lựa chọn
        
        # Danh sách các loại biểu đồ
        charts = [
            ("Sống sót vs Thiệt mạng", "survived"),
            ("Tỉ lệ Nam / Nữ", "sex"),
            ("Phân bố độ tuổi", "age"),
            ("Giá vé (Boxplot)", "fare"),
            ("Sống sót theo Giới tính", "sex_survived"),
            ("Sống sót theo hạng vé", "survived_pclass"),
            ("Mật độ tuổi theo Sống sót", "age_kde"),
            ("Ma trận tương quan", "corr")
        ]
        
        # Tạo radio buttons
        for text, value in charts:
            ttk.Radiobutton(
                popup,
                text=text,
                variable=chart_type,
                value=value
            ).pack(anchor="w", padx=30, pady=2)
        
        def plot():
            selected = chart_type.get()  # Lấy giá trị được chọn
            if selected:
                self.plot_selected_chart(selected)  # Vẽ biểu đồ
                #popup.destroy()  # Đóng popup, có thể đóng nếu muốn
        
        # Nút vẽ biểu đồ
        ttk.Button(
            popup,
            text="Vẽ biểu đồ",
            command=plot
        ).pack(pady=15)
    
    def plot_selected_chart(self, chart_type):
        """Điều hướng đến hàm vẽ biểu đồ tương ứng"""
        if chart_type == "survived":
            self.plot_survived_count()
        
        elif chart_type == "sex":
            self.plot_sex_distribution()
        
        elif chart_type == "age":
            self.plot_age_hist()
        
        elif chart_type == "fare":
            self.plot_fare_box()

        elif chart_type == "survived_pclass":
            self.plot_pclass_survived()
        
        elif chart_type == "sex_survived":
            self.plot_sex_survived()
        
        elif chart_type == "age_kde":
            self.plot_age_kde()
        
        elif chart_type == "corr":
            self.plot_correlation()
    
    def plot_survived_count(self):
        """1. Biểu đồ Cột: Số lượng Sống sót vs Thiệt mạng"""
        plt.figure(figsize=(6, 4))
        sns.countplot(data=self.df, x='Survived', palette='pastel')
        plt.title('Số lượng Sống sót (1) vs Thiệt mạng (0)')
        plt.ylabel('Số lượng')
        plt.show()

    def plot_sex_distribution(self):
        """2. Biểu đồ Tròn: Tỉ lệ Nam/Nữ"""
        plt.figure(figsize=(6, 6))
        self.df['Sex'].value_counts().plot.pie(autopct='%1.1f%%', colors=['skyblue', 'pink'])
        plt.title('Tỉ lệ Nam / Nữ')
        plt.ylabel('')
        plt.show()

    def plot_age_hist(self):
        """3. Biểu đồ Histogram: Phân bố độ tuổi"""
        plt.figure(figsize=(8, 5))
        sns.histplot(self.df['Age'], bins=20, kde=True, color='green')
        plt.title('Phân bố độ tuổi hành khách')
        plt.show()

    def plot_fare_box(self):
        """4. Biểu đồ Hộp: Kiểm tra ngoại lai giá vé"""
        plt.figure(figsize=(10, 5))
        sns.boxplot(x=self.df['Fare'], color='orange')
        plt.title('Biểu đồ hộp (Boxplot) Giá vé')
        plt.show()

    def plot_sex_survived(self):
        """5. Biểu đồ Cột nhóm: Tỉ lệ sống sót theo Giới tính"""
        plt.figure(figsize=(6, 4))
        sns.countplot(data=self.df, x='Sex', hue='Survived')
        plt.title('Tỉ lệ sống sót theo Giới tính')
        plt.show()

    def plot_pclass_survived(self):
        """6. Biểu đồ Cột nhóm: So sánh Sống/Chết Hạng 1 vs Hạng 3"""
        plt.figure(figsize=(8, 6))
        # Chỉ lấy Hạng 1 và Hạng 3
        df_filtered = self.df[self.df['Pclass'].isin([1, 3])].copy()
        sns.countplot(data=df_filtered, x='Pclass', hue='Survived', palette='Set2')
        plt.title('So sánh tỉ lệ Sống sót: Hạng Nhất (1) vs Hạng Ba (3)')
        plt.legend(title='Trạng thái', labels=['Thiệt mạng (0)', 'Sống sót (1)'])
        plt.show()

    def plot_age_kde(self):
        """7. Biểu đồ Mật độ (KDE): So sánh phân phối Tuổi (Sống vs Chết)"""
        plt.figure(figsize=(10, 6))
        # fill=True để tô màu vùng dưới đường cong
        sns.kdeplot(data=self.df, x='Age', hue='Survived', fill=True, palette='crest')
        #có thể dùng clip để cắt đi phần rìa (dưới 0 tuổi và trên 80 tuổi) nhưng sẽ đánh đổi về mặt chính xác toán học
        #sns.kdeplot(data=self.df, x='Age', hue='Survived', fill=True, palette='crest', clip=(0, 80))
        plt.title('Phân phối Độ tuổi: Nhóm Sống sót vs Thiệt mạng')
        plt.xlabel('Tuổi')
        plt.ylabel('Mật độ')
        # Chú thích thêm: Đỉnh nhỏ ở đoạn 0-10 tuổi của nhóm Sống (trẻ em được ưu tiên)
        plt.show()

    def plot_correlation(self):
        """8. Biểu đồ Nhiệt: Tương quan giữa các biến số"""
        plt.figure(figsize=(8, 6))
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Biểu đồ nhiệt tương quan (Correlation Heatmap)')
        plt.show()