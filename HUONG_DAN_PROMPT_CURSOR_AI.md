# Hướng Dẫn Prompt Cursor AI Tạo Báo Cáo Mua Hàng

## Mục đích
Tài liệu này hướng dẫn cách sử dụng Cursor AI để tạo ra hệ thống tạo báo cáo mua hàng tự động từ dữ liệu Excel.

---

## BƯỚC 1: Phân tích yêu cầu và tạo code ban đầu

### Prompt mẫu:

```
DỮ LIỆU CHO SẴN 
file Excel "Doanh thu 2024" 
Có các cột: ngày; Mã HH; Tên HH; dvt; SL bán; SL tồn; DonGiaBan; ThanhTienBan;  
file Excel "No NCC" (Sheet NCC) 
Có các cột Mã NCC; Tên NCC; Tổng giá trị mua 
file Excel "NCC mua them" (Sheet q) 
Có các cột Mã NCC; Tên NCC  

Yêu cầu rõ: Tạo báo cáo mua hàng 
"Cần tạo báo cáo mua hàng file Excel gồm sheet: ChiTietmuahang + Đối chieu + File xuat nhap ton 

* File Chi tiết mua hàng 
  + Tổng phiếu mua từ 150-250 phieu 
  + Số lượng mua đảm bảo không âm kho mọi thời điểm; Có thể gộp 1 phiếu mua bán nhiều ngày 
  + Giá mua = TổngDoanh thu hàng tháng của từng Mã HH/Tổng số lượng bán Mã HHx(88%-86%). 
    Giá mua dùng hàm (Roundup,2), làm tròn đến hàng trăm 
  + Giá mua/mã HH/SL mua Mã HH mỗi lần mua là khác nhau 
  + Tổng giá trị mua theo từng NCC bằng tuyệt đối tổng giá trị mua đã cho trong file No NCC.
    Giá trị mua từ 10 triệu-200 triệu/lần mua. 
  + Nếu vẫn còn âm kho thì dùng NCC trong file NCC mua them để mua 
  + Giá trị mua từ 10-200 triệu/lần mua/NCC 
  + Phiếu nhập có giá trị lớn xen phiếu có giá trị nhỏ/cùng 1 mã hàng 
  + Giá mua không thuế 

Kết quả: Tạo ra file excel báo cáo muahàng có 3 sheet, sheet chi tiết và tổng hợp (mỗi lần xuất ra 1 tên gọi khác nhau). 

* File Chi tiết mua hàng có các cột STT; Mã HH; Tên HH; Mã NCC; tên NCC; Ngày mua; DVT; SL mua; Don gia mua; Thanhtienmua 
* File Doi chieu có cột Mã NCC; Tên NCC; Tổng giá trị mua ; đối chiếu với tổng giá trị mua 
* File Ton kho có các cột: STT; Mã HH; Tên HH; DVT; SL nhap; Gia tri nhap; SL xuất; Giá vốn xuất bán; SL tồn; Giá trị tồn 

ok dùng code python để làm đi nè bạn ơi và code phải tối ưu nha-> bạn là 1 Expert Python Developer
```

### Kết quả mong đợi:
- AI sẽ tạo một file Python với các class cơ bản
- Code sẽ có các chức năng: đọc Excel, tính giá mua, tạo phiếu mua, xuất báo cáo

---

## BƯỚC 2: Tối ưu code với OOP

### Prompt mẫu:

```
OK code dài quá ta có thể dùng OOP để làm code ngắn và tối ưu code không?
```

### Hoặc prompt chi tiết hơn:

```
Code hiện tại quá dài và khó bảo trì. Hãy refactor code thành cấu trúc OOP với các class riêng biệt:
1. DataLoader - xử lý đọc file Excel
2. PriceCalculator - tính toán giá mua
3. InventoryManager - quản lý tồn kho
4. PurchaseOrderGenerator - tạo phiếu mua
5. ReportExporter - xuất báo cáo
6. PurchaseReportGenerator - class chính điều phối

Mỗi class nên có trách nhiệm rõ ràng và code phải ngắn gọn, dễ đọc.
```

### Kết quả mong đợi:
- Code được tách thành nhiều module riêng biệt
- Mỗi class có một trách nhiệm cụ thể
- Code ngắn gọn và dễ bảo trì hơn

---

## BƯỚC 3: Tạo cấu trúc thư mục chuyên nghiệp

### Prompt mẫu:

```
Chưa đạt giờ tạo 1 folder riêng ra rồi làm 1 cái structure hoàn chỉnh nha -> bạn là 1 expert Python mà
```

### Hoặc prompt chi tiết hơn:

```
Tạo một cấu trúc thư mục chuyên nghiệp cho project Python:
- Tách code thành các module trong package riêng
- Tạo thư mục data/input và data/output
- Tạo file requirements.txt
- Tạo README.md
- Tạo file __init__.py cho package
- Tạo entry point main.py ở root

Cấu trúc nên theo chuẩn Python project best practices.
```

### Kết quả mong đợi:
```
purchase_report_generator/
├── src/
│   └── purchase_report/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── price_calculator.py
│       ├── inventory_manager.py
│       ├── purchase_order_generator.py
│       ├── report_exporter.py
│       └── main.py
├── data/
│   ├── input/
│   └── output/
├── main.py
├── requirements.txt
└── README.md
```

---

## BƯỚC 4: Tổ chức file input/output

### Prompt mẫu:

```
OK giờ file generate_purchase_report.py xóa đi nè với tạo 2 cái folder INPUT là các file excel đầu vào và OUTPUT là các file Excel đầu ra đi nè
```

### Kết quả mong đợi:
- Xóa file code cũ ở root
- Tạo folder INPUT/ chứa file Excel đầu vào
- Tạo folder OUTPUT/ chứa file Excel đầu ra
- Cập nhật code để đọc từ INPUT/ và ghi vào OUTPUT/

---

## BƯỚC 5: Test và sửa lỗi

### Prompt khi gặp lỗi:

```
Chạy thử đi
```

### Nếu có lỗi encoding:

```
Có lỗi encoding với tiếng Việt trên Windows console. Hãy sửa lại.
```

### Nếu có lỗi import:

```
Có lỗi import module. Hãy kiểm tra và sửa lại đường dẫn import.
```

### ⚠️ Lỗi PowerShell với `&&`:

**Khi gặp lỗi này:**
```
The token '&&' is not a valid statement separator in this version.
```

**Prompt để sửa:**
```
Lỗi PowerShell: không dùng được &&. Hãy sửa lại command dùng `;` thay vì `&&` hoặc tách thành nhiều lệnh riêng.
```

**Ví dụ sửa:**
- ❌ `cd folder && python script.py` 
- ✅ `cd folder; python script.py`
- ✅ Hoặc tách: `cd folder` rồi `python script.py`

---

## CÁC PROMPT HỮU ÍCH KHÁC

### 1. Thêm tính năng mới:

```
Thêm tính năng [mô tả tính năng] vào code hiện tại
```

### 2. Tối ưu hiệu suất:

```
Code chạy chậm. Hãy tối ưu hiệu suất cho phần [mô tả phần code]
```

### 3. Thêm validation:

```
Thêm validation để kiểm tra dữ liệu đầu vào trước khi xử lý
```

### 4. Thêm logging:

```
Thêm logging để theo dõi quá trình xử lý
```

### 5. Tạo unit test:

```
Tạo unit test cho các class trong project
```

---

## TIPS QUAN TRỌNG KHI PROMPT

### ✅ Nên làm:

1. **Mô tả rõ ràng yêu cầu**: Càng chi tiết càng tốt
2. **Đưa ra ví dụ cụ thể**: Ví dụ về input/output mong đợi
3. **Yêu cầu từng bước**: Chia nhỏ yêu cầu phức tạp
4. **Yêu cầu giải thích**: "Hãy giải thích cách code hoạt động"
5. **Yêu cầu tối ưu**: "Code phải tối ưu và dễ đọc"

### ❌ Không nên:

1. **Prompt quá ngắn**: "Làm đi" → Không rõ ràng
2. **Yêu cầu quá nhiều cùng lúc**: Chia nhỏ ra
3. **Không kiểm tra kết quả**: Luôn test sau mỗi bước
4. **Bỏ qua lỗi**: Sửa lỗi ngay khi phát hiện

### ⚠️ LƯU Ý QUAN TRỌNG VỀ POWERSHELL:

**KHÔNG dùng `&&` trong PowerShell!**

PowerShell không hỗ trợ toán tử `&&` như bash. Sử dụng `&&` sẽ gây lỗi và tốn token không cần thiết.

#### ❌ SAI (không hoạt động trong PowerShell):
```powershell
cd folder && python script.py
```

#### ✅ ĐÚNG (cách viết cho PowerShell):
```powershell
cd folder; python script.py
```

Hoặc tách thành 2 lệnh riêng:
```powershell
cd folder
python script.py
```

#### Khi prompt AI tạo command:
Luôn nhắc AI: **"Nhớ dùng `;` thay vì `&&` vì đây là PowerShell, không phải bash"**

Ví dụ prompt:
```
Tạo command để chạy script Python. Lưu ý: dùng PowerShell nên phải dùng `;` thay vì `&&`
```

---

## QUY TRÌNH HOÀN CHỈNH

### Bước 1: Chuẩn bị
- Chuẩn bị file Excel mẫu
- Xác định rõ yêu cầu

### Bước 2: Prompt tạo code cơ bản
- Sử dụng prompt ở BƯỚC 1
- Kiểm tra code được tạo

### Bước 3: Test code
- Chạy thử code
- Kiểm tra lỗi

### Bước 4: Tối ưu code
- Sử dụng prompt ở BƯỚC 2
- Refactor thành OOP

### Bước 5: Tổ chức cấu trúc
- Sử dụng prompt ở BƯỚC 3
- Tạo cấu trúc thư mục

### Bước 6: Hoàn thiện
- Sử dụng prompt ở BƯỚC 4
- Tổ chức file input/output

### Bước 7: Test cuối cùng
- Chạy toàn bộ hệ thống
- Kiểm tra kết quả

---

## VÍ DỤ PROMPT HOÀN CHỈNH

### Prompt cho người mới bắt đầu:

```
Tôi cần tạo một hệ thống Python để:
1. Đọc 3 file Excel (Doanh thu, NCC, NCC mua thêm)
2. Tính toán giá mua tự động
3. Tạo 150-250 phiếu mua hàng
4. Đảm bảo không âm kho
5. Xuất báo cáo Excel với 3 sheet

Hãy tạo code Python hoàn chỉnh, có comment tiếng Việt, và dễ hiểu.
Tôi là người mới học Python nên code cần rõ ràng.
```

### Prompt cho người có kinh nghiệm:

```
Refactor code này thành architecture clean code với:
- Separation of concerns
- Dependency injection
- Error handling đầy đủ
- Type hints
- Docstrings theo chuẩn Google
- Unit tests với pytest
```

---

## KẾT LUẬN

Với các prompt trên, bạn có thể hướng dẫn khách hàng sử dụng Cursor AI để:
- ✅ Tạo code từ đầu
- ✅ Tối ưu code hiện có
- ✅ Tổ chức cấu trúc project
- ✅ Sửa lỗi và cải thiện

**Lưu ý**: Luôn test code sau mỗi lần AI generate và yêu cầu AI giải thích logic phức tạp.

---

## VÍ DỤ PROMPT THỰC TẾ ĐÃ SỬ DỤNG

### Prompt 1: Tạo code ban đầu
```
DỮ LIỆU CHO SẴN 
file Excel "Doanh thu 2024" 
Có các cột: ngày; Mã HH; Tên HH; dvt; SL bán; SL tồn; DonGiaBan; ThanhTienBan;  
file Excel "No NCC" (Sheet NCC) 
Có các cột Mã NCC; Tên NCC; Tổng giá trị mua 
file Excel "NCC mua them" (Sheet q) 
Có các cột Mã NCC; Tên NCC  

Yêu cầu rõ: Tạo báo cáo mua hàng 
"Cần tạo báo cáo mua hàng file Excel gồm sheet: ChiTietmuahang + Đối chieu + File xuat nhap ton 
* File Chi tiết mua hàng 
  + Tổng phiếu mua từ 150-250 phieu 
  + Số lượng mua đảm bảo không âm kho mọi thời điểm; Có thể gộp 1 phiếu mua bán nhiều ngày 
  + Giá mua = TổngDoanh thu hàng tháng của từng Mã HH/Tổng số lượng bán Mã HHx(88%-86%). 
    Giá mua dùng hàm (Roundup,2), làm tròn đến hàng trăm 
  + Giá mua/mã HH/SL mua Mã HH mỗi lần mua là khác nhau 
  + Tổng giá trị mua theo từng NCC bằng tuyệt đối tổng giá trị mua đã cho trong file No NCC.
    Giá trị mua từ 10 triệu-200 triệu/lần mua. 
  + Nếu vẫn còn âm kho thì dùng NCC trong file NCC mua them để mua 
  + Giá trị mua từ 10-200 triệu/lần mua/NCC 
  + Phiếu nhập có giá trị lớn xen phiếu có giá trị nhỏ/cùng 1 mã hàng 
  + Giá mua không thuế 

Kết quả: Tạo ra file excel báo cáo muahàng có 3 sheet, sheet chi tiết và tổng hợp (mỗi lần xuất ra 1 tên gọi khác nhau). 
* File Chi tiết mua hàng có các cột STT; Mã HH; Tên HH; Mã NCC; tên NCC; Ngày mua; DVT; SL mua; Don gia mua; Thanhtienmua 
* File Doi chieu có cột Mã NCC; Tên NCC; Tổng giá trị mua ; đối chiếu với tổng giá trị mua 
* File Ton kho có các cột: STT; Mã HH; Tên HH; DVT; SL nhap; Gia tri nhap; SL xuất; Giá vốn xuất bán; SL tồn; Giá trị tồn 

ok dùng code python để làm đi nè bạn ơi và code phải tối ưu nha-> bạn là 1 Expert Python Developer
```

### Prompt 2: Tối ưu với OOP
```
OK code dài quá ta có thể dùng OOP để làm code ngắn và tối ưu code không?
```

### Prompt 3: Tạo cấu trúc folder
```
Chưa đạt giờ tạo 1 folder riêng ra rồi làm 1 cái structure hoàn chỉnh nha -> bạn là 1 expert Python mà
```

### Prompt 4: Tổ chức file
```
OK giờ file generate_purchase_report.py xóa đi nè với tạo 2 cái folder INPUT là các file excel đầu vào và OUTPUT là các file Excel đầu ra đi nè
```

### Prompt 5: Test code
```
Chạy thử đi
```

**Lưu ý**: Khi AI tạo command terminal, nhắc AI dùng `;` thay vì `&&` cho PowerShell

---

## CHECKLIST KHI DẠY KHÁCH HÀNG

### ✅ Trước khi bắt đầu:
- [ ] Giải thích cách Cursor AI hoạt động
- [ ] Hướng dẫn cài đặt Cursor
- [ ] Chuẩn bị file Excel mẫu
- [ ] Giải thích yêu cầu rõ ràng

### ✅ Trong quá trình:
- [ ] Copy prompt từng bước
- [ ] Kiểm tra code được tạo
- [ ] Giải thích từng phần code
- [ ] Test code sau mỗi bước

### ✅ Sau khi hoàn thành:
- [ ] Kiểm tra toàn bộ chức năng
- [ ] Hướng dẫn cách sử dụng
- [ ] Giải thích cách maintain code
- [ ] Đưa ra tips tối ưu

---

## TÀI LIỆU THAM KHẢO

- [Cursor AI Documentation](https://cursor.sh/docs)
- [Python Best Practices](https://docs.python-guide.org/writing/style/)
- [Clean Code Principles](https://github.com/ryanmcdermott/clean-code-javascript)

---

**Tác giả**: Expert Python Developer  
**Ngày tạo**: 2025-01-17  
**Phiên bản**: 1.0

