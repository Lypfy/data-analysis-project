"""
Module App - Lớp chính của ứng dụng
Kết nối tất cả các module lại với nhau
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

from .data_handler import DataHandler
from .ui_components import UIComponents
from .visualizer import Visualizer

import os


class DynamicDataApp:
    """Lớp chính của ứng dụng quản lý dữ liệu động"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Dữ liệu Động (Import Excel/CSV)")
        self.root.geometry("1000x700")
        
        # Khởi tạo các module con
        self.data_handler = DataHandler()
        self.ui = UIComponents(root)
        self.visualizer = Visualizer(root)
        
        # Tạo giao diện
        self._setup_ui()
    
    def _setup_ui(self):
        """Thiết lập giao diện"""
        # 1. Khung điều khiển trên
        self.ui.create_top_frame(self.load_file)
        
        # 2. Khung nhập liệu
        self.ui.create_input_frame()
        
        # 3. Khung chức năng
        self.ui.create_button_frame(
            add_cmd=self.add_data,
            update_cmd=self.update_data,
            delete_cmd=self.delete_data,
            clean_cmd=self.clean_data,
            plot_cmd=self.show_visualization_popup
        )
        
        # 4. Bảng dữ liệu
        self.ui.create_tree_view(self.on_item_select)
    
    def load_file(self):
        """Mở hộp thoại chọn file và load dữ liệu"""
        # Mở hộp thoại chọn file
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel/CSV Files", "*.xlsx *.xls *.csv")]
        )
        if not file_path:
            return # Người dùng hủy
        
        try:
            # Load file qua DataHandler
            self.data_handler.load_file(file_path)
            
            # Cập nhật label trạng thái
            self.ui.update_status_label(
                #f"Đang mở: {file_path.split('/')[-1]}",
                f"Đang mở: {os.path.basename(file_path)}",
                "green"
            )

            # Cập nhật cấu trúc UI theo cột của file
            self.refresh_ui_structure()
            # Cập nhật và hiển thị dữ liệu lên bảng
            self.refresh_table()
            
            messagebox.showinfo("Thành công", "Đã tải dữ liệu thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")
    
    def refresh_ui_structure(self):
        """Tạo lại cột bảng và ô nhập liệu dựa trên số cột của file"""
        columns = list(self.data_handler.df.columns)
        
        # Cập nhật TreeView
        self.ui.refresh_tree_columns(columns)
        
        # Cập nhật Input widget
        self.ui.refresh_input_widgets(columns)
    
    def refresh_table(self):
        """Đổ dữ liệu từ DataFrame vào TreeView"""
        self.ui.populate_tree(self.data_handler.df)
    
    def on_item_select(self, event):
        """Khi chọn dòng, điền dữ liệu vào các ô input"""

        # Kiểm tra xem có chọn dòng chưa
        index = self.ui.get_selected_item()
        if index is None:
            return
        
        # Lấy dữ liệu từ DataFrame tại dòng đang chọn
        row_data = self.data_handler.df.iloc[index]
        
        # Điền vào các ô input
        self.ui.fill_entry_values(row_data)
    
    def add_data(self):
        """Thêm dữ liệu từ các ô input vào DataFrame"""
        if self.data_handler.df.empty:
            return
        
        try:
            # Lấy dữ liệu từ các ô nhập liệu
            entry_values = self.ui.get_entry_values()
            new_row = {}
            
            # Duyệt qua các ô nhập liệu (col là tên cột, val là ô tương ứng)
            for col, val in entry_values.items():
                # Lấy và ép kiểu dữ liệu
                new_row[col] = self.data_handler.parse_value(val)
            
            # Kiểm tra dữ liệu trong các ô input bằng hàm validata_data
            is_valid, error_msg = self.data_handler.validate_data(new_row)
            if not is_valid:
                messagebox.showerror("Lỗi nhập liệu", error_msg)
                return
            
            # Thêm vào cuối DataFrame
            self.data_handler.add_row(new_row)
            
            # Lưu file vào thư mục data/
            filepath = self.data_handler.save_file()
            
            # Cập nhật bảng
            self.refresh_table()
            messagebox.showinfo("Thành công", f"Đã thêm dòng mới và lưu vào {filepath}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def update_data(self):
        """Cập nhật dòng đang chọn"""
        index = self.ui.get_selected_item()
        
        # Kiểm tra xem đã chọn dòng chưa
        if index is None:
            messagebox.showwarning("Chú ý", "Hãy chọn một dòng để cập nhật")
            return
        
        try:
            # Lấy dữ liệu từ các ô nhập liệu
            entry_values = self.ui.get_entry_values()
            temp_row = {}
            
            # Duyệt qua các ô nhập liệu (col là tên cột, val là giá trị ô tương ứng) và cập nhật giá trị
            for col, val in entry_values.items():
                temp_row[col] = self.data_handler.parse_value(val)
            
            # Kiểm tra dữ liệu trong các ô input bằng hàm validate_data
            is_valid, error_msg = self.data_handler.validate_data(temp_row)
            if not is_valid:
                messagebox.showerror("Lỗi nhập liệu", error_msg)
                return
            
            # Cập nhật vào DataFrame
            self.data_handler.update_row(index, temp_row)
            
            # Lưu file vào thư mục data/
            filepath = self.data_handler.save_file()
            
            # Cập nhật bảng
            self.refresh_table()
            messagebox.showinfo("Thành công", f"Đã cập nhật và lưu vào {filepath}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def delete_data(self):
        """Xóa dòng đang chọn"""
        index = self.ui.get_selected_item()
        
        # Kiểm tra xem đã chọn dòng chưa
        if index is None:
            messagebox.showwarning("Chú ý", "Hãy chọn một dòng để xóa")
            return
        
        # Xác nhận xóa
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa dòng này?")
        if not confirm:
            return
        
        try:
            # Xóa khỏi DataFrame
            self.data_handler.delete_row(index)
            
            # Lưu file vào thư mục data/
            filepath = self.data_handler.save_file()
            
            # Cập nhật bảng
            self.refresh_table()
            messagebox.showinfo("Thành công", f"Đã xóa dòng và lưu vào {filepath}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def clean_data(self):
        """Làm sạch dữ liệu"""
        try:
            # Gọi hàm clean từ DataHandler (đã tự động lưu file)
            self.data_handler.clean_data()
            
            filename = self.data_handler.file_name

            # Cập nhật bảng
            self.refresh_table()
            messagebox.showinfo("Thành công", f"Đã làm sạch dữ liệu và lưu vào {filename}")
            
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def show_visualization_popup(self):
        """Hiển thị popup vẽ biểu đồ"""
        self.visualizer.show_visualization_popup(self.data_handler.df)