"""
Module xử lý dữ liệu - Data Handler
Chứa các hàm xử lý, validate, clean dữ liệu
"""

import pandas as pd
import os


class DataHandler:
    """Lớp xử lý dữ liệu"""
    
    def __init__(self):
        self.df = pd.DataFrame()
        self.data_dir = "data"
        self.file_name = "titanic.csv"
        
        # Tạo thư mục data nếu chưa tồn tại
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    @staticmethod
    def parse_value(val):
        """Ép kiểu dữ liệu an toàn"""
        val = val.strip()  # Xóa khoảng trắng
        if val == "":
            return None
        
        # Thử ép sang số nguyên
        try:
            return int(val)
        except ValueError:
            # Nếu không phải số nguyên, thử ép sang số thực
            try:
                return float(val)
            except ValueError:
                # Nếu không phải số thì giữ nguyên chuỗi
                return val
    
    @staticmethod
    def validate_data(row_data):
        """
        Kiểm tra tính hợp lệ của dữ liệu trước khi Thêm hoặc Update.
        Trả về: (True, "") nếu hợp lệ, (False, "Lỗi...") nếu không hợp lệ.
        """
        
        # 1. Kiểm tra Survived (0 hoặc 1)
        if 'Survived' in row_data:
            val = row_data['Survived']
            # Chấp nhận số 0, 1 hoặc chuỗi "0", "1"
            if str(val) not in ['0', '1']:
                return False, "Cột 'Survived' chỉ được nhập 0 hoặc 1."

        # 2. Kiểm tra Pclass (1, 2, 3)
        if 'Pclass' in row_data:
            val = row_data['Pclass']
            if str(val) not in ['1', '2', '3']:
                return False, "Cột 'Pclass' chỉ được nhập 1, 2 hoặc 3."

        # 3. Kiểm tra Sex (male hoặc female)
        if 'Sex' in row_data:
            val = str(row_data['Sex']).lower().strip()
            if val not in ['male', 'female']:
                return False, "Cột 'Sex' chỉ được nhập 'male' hoặc 'female'."

        # 4. Kiểm tra Age (>0 và <=146)
        if 'Age' in row_data:
            val = row_data['Age']
            # Kiểm tra xem có phải số không (int hoặc float)
            if not isinstance(val, (int, float)):
                return False, "Cột 'Age' phải là số."
            if not (0 < val <= 146):
                return False, "Cột 'Age' phải lớn hơn 0 và nhỏ hơn hoặc bằng 146."

        # 5. Các cột bắt buộc là số: SibSp, Parch, Fare
        numeric_cols = ['SibSp', 'Parch', 'Fare']
        for col in numeric_cols:
            if col in row_data:
                val = row_data[col]
                if not isinstance(val, (int, float)):
                    return False, f"Cột '{col}' bắt buộc phải nhập số."
                if val < 0:
                    return False, f"Cột '{col}' không được là số âm."

        return True, ""

    def load_file(self, file_path):
        """Load file CSV hoặc Excel"""
        # Cập nhật tên file hiện tại (self.file_name) dựa trên file vừa chọn
        # Hàm os.path.basename sẽ lấy tên file từ đường dẫn đầy đủ (VD: C:/data/file.xlsx -> file.xlsx)
        self.file_name = os.path.basename(file_path)

        # Logic đọc file
        if file_path.endswith('.csv'):
            self.df = pd.read_csv(file_path)
        else:
            self.df = pd.read_excel(file_path)
        return self.df
    
    def add_row(self, new_row):
        """Thêm dòng mới vào DataFrame"""
        self.df.loc[len(self.df)] = new_row
        return self.df
    
    def update_row(self, index, updated_row):
        """Cập nhật dòng tại index"""
        for col, val in updated_row.items():
            self.df.at[index, col] = val
        return self.df
    
    def delete_row(self, index):
        """Xóa dòng tại index (dòng đang chọn)"""
        self.df = self.df.drop(index).reset_index(drop=True)
        return self.df
    
    def save_file(self, filename=None):
        """
        Lưu DataFrame ra file CSV hoặc Excel trong thư mục data
        Tự động nhận diện định dạng dựa trên đuôi file gốc
        """
        # Nếu không truyền filename, dùng tên file gốc đã lưu ở hàm load_file
        if filename is None:
            filename = self.file_name
        
        # Tạo đường dẫn đầy đủ
        filepath = os.path.join(self.data_dir, filename)
        
        # Lấy đuôi file (extension) để kiểm tra: .csv hay .xlsx/.xls
        # file_extension sẽ lấy đuôi .csv... và chuyển các ký tự thành in thường
        _, file_extension = os.path.splitext(filename)
        file_extension = file_extension.lower()
        
        try:
            if file_extension == '.csv':
                # Trường hợp csv
                self.df.to_csv(filepath, index=False, encoding='utf-8')
                
            elif file_extension in ['.xlsx', '.xls']:
                # Trường hợp excel
                # Sử dụng engine='openpyxl' để ghi file Excel
                self.df.to_excel(filepath, index=False, engine='openpyxl')
                
            else:
                # Trường hợp đuôi lạ, mặc định ép về CSV và thêm đuôi .csv
                filepath = filepath + ".csv"
                self.df.to_csv(filepath, index=False, encoding='utf-8')

            print(f"Đã lưu file thành công tại: {filepath}")
                
        except Exception as e:
            print(f"Lỗi khi lưu file: {e}")
            raise e # Ném lỗi để bên App.py hiển thị popup thông báo
        
        return filepath

    def clean_data(self):

        data = self.df.copy()
        
        # Hàm dropna() loại bỏ các dòng có giá trị null
        # Nếu PassengerId hoặc Survived bị null -> Xóa dòng đó
        data = data.dropna(subset=['PassengerId', 'Survived'])

        # Danh sách các cột số nguyên (Int) cần điền 0
        columns_int = ['SibSp', 'Parch']

        for col in columns_int:
            if col in data.columns:
                # Điền giá trị thiếu bằng 0
                data[col] = data[col].fillna(0)

        # Danh sách các cột cần điền giá trị trung bình (Hàm median tự động bỏ qua NaN)
        columns_mean = ['Age', 'Fare']
        for col in columns_mean:
            if col in data.columns:
                data[col] = data[col].fillna(data[col].median())

        # Danh sách các cột điền giá trị phổ biến nhất     
        columns_mode = ['Pclass', 'Embarked']
        for col in columns_mode:
            if col in data.columns:
                data[col] = data[col].fillna(data[col].mode()[0])

        # Danh sách cột chuỗi có thể thiếu dữ liệu
        string_cols = ['Name', 'Sex', 'Cabin', 'Embarked', 'Ticket']

        # Điền chuỗi "no_info" vào các ô trống
        for col in string_cols:
            if col in data.columns:
                data[col] = data[col].fillna("no_info")
        
        #Hàm loại bỏ các bản ghi trùng lặp dựa PassengerId và trả về DataFrame đã được làm sạch
        data = data.drop_duplicates(subset=['PassengerId'], keep='first') 

        # Định dạng cột Sex thành chữ thường
        if 'Sex' in data.columns:
            # Ép kiểu chuỗi -> Chuyển chữ thường -> Cắt khoảng trắng thừa
            data['Sex'] = data['Sex'].astype(str).str.lower().str.strip()

        # Định dạng cột Embarked thành chữ hoa
        if 'Embarked' in data.columns:
            # Ép kiểu chuỗi -> Chuyển chữ HOA -> Cắt khoảng trắng thừa
            data['Embarked'] = data['Embarked'].astype(str).str.upper().str.strip()

        # Chuyển đổi cột Age sang kiểu số nguyên (Integer)
        if 'Age' in data.columns:
            data['Age'] = data['Age'].astype(int)

        # Chuyển đổi PassengerId sang kiểu chuỗi (String)
        if 'PassengerId' in data.columns:
            data['PassengerId'] = data['PassengerId'].astype(str)

        # Danh sách các cột số lượng bắt buộc phải dương
        cols_pos = ['Fare', 'SibSp', 'Parch']

        for col in cols_pos:
            if col in data.columns:
                # Lấy trị tuyệt đối cho toàn bộ cột
                data[col] = data[col].abs()
        
        # Lưu vào file csv, xlsx/xls tương ứng
        self.df = data
        self.save_file()

