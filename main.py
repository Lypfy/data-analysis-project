"""
File chính để chạy ứng dụng
Đặt file này trong thư mục data-analysis (cùng cấp với thư mục src)
"""

import tkinter as tk
from src.app import DynamicDataApp
import openpyxl

def main():
    """Hàm main để khởi chạy ứng dụng"""
    # Khởi tạo cửa sổ giao diện GUI
    root = tk.Tk()
    
    # Khởi tạo ứng dụng
    app = DynamicDataApp(root)
    
    # Chạy vòng lặp sự kiện
    root.mainloop()

if __name__ == "__main__":
    main()