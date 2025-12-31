# Data Analysis Project (Python)

## Giới thiệu
Đây là project phân tích dữ liệu sử dụng **Python**, với các thư viện phổ biến như **Pandas**, **Matplotlib** và **OpenPyXL**.  
Project dùng để đọc dữ liệu CSV/Excel, xử lý, phân tích và trực quan hóa dữ liệu.

---

## Cấu trúc thư mục

data-analysis-project/
data/ # Thư mục lưu dữ liệu
original_data/ # Dữ liệu gốc ban đầu
src/ # Chứa source code
main.py # File chạy chính của chương trình
requirements.txt # Danh sách thư viện cần cài đặt
README.md # Tài liệu hướng dẫn
.gitignore # File cấu hình Git ignore


**Lưu ý**:
- Thư mục `data/` được giữ lại để chứa dữ liệu phát sinh khi chạy chương trình.
- Dữ liệu gốc nằm trong `original_data/`.
- Các file dữ liệu sinh ra trong quá trình chạy **không được commit**.

---

## Yêu cầu môi trường

- Python **3.8 trở lên**
- Hệ điều hành: Windows / macOS / Linux

---

## Cài đặt thư viện

Các thư viện cần thiết được liệt kê trong file `requirements.txt`:
- **pandas**: Xử lý và phân tích dữ liệu dạng bảng (CSV, Excel)
- **matplotlib**: Vẽ biểu đồ trực quan hóa dữ liệu
- **openpyxl**: Đọc/ghi file Excel (.xlsx)

Cài đặt các thư viện bằng lệnh:

```bash
pip install -r requirements.txt
```
---

## Cách chạy chương trình

Sau khi cài đặt đầy đủ thư viện, chạy chương trình bằng lệnh: (hoặc chạy file main.py)

```bash
python main.py
```
