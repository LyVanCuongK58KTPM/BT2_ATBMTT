# BÀI TẬP VỀ NHÀ – MÔN: AN TOÀN VÀ BẢO MẬT THÔNG TIN
# Chủ đề: Chữ ký số trong file PDF
# Giảng viên: Đỗ Duy Cốp
# Thời điểm giao: 2025-10-24 11:45
# Đối tượng áp dụng: Toàn bộ sv lớp học phần 58KTPM
# Hạn nộp: Sv upload tất cả lên github trước 2025-10-31 23:59:59

---------------------------------------------------
# Demo file
- Tải OpenSSL:
  <img width="1040" height="758" alt="image" src="https://github.com/user-attachments/assets/12579195-6a30-4a96-aa73-d676eb92f1cb" />

- Chuẩn bị trước 1 file PDF gốc(chukiso.pdf)
  <img width="978" height="759" alt="image" src="https://github.com/user-attachments/assets/b77c7129-a5a3-401d-8191-8443e5f6d16e" />
- Tạo mycert.pem và mykey.pem sử dụng OpenSSL để tạo chứng chỉ và khóa:
  <img width="1468" height="351" alt="image" src="https://github.com/user-attachments/assets/7f58462d-c375-4627-b2ab-be9bf1a4adb5" />

- Ta được 2 file:
<img width="442" height="63" alt="image" src="https://github.com/user-attachments/assets/7f1349aa-ecaa-46cc-a7fc-0cef2b357d1e" />

- Chuẩn bị trước 1 ảnh chữ kí của em tự kí:
   <img width="707" height="662" alt="image" src="https://github.com/user-attachments/assets/c75fdc17-0edf-498d-965e-9d6142546d43" />
- Tạo 1 file chukiso.py với cấu hình:
+ PDF_INPUT = "chukiso.pdf"               
+ PDF_TEMP = "chukiso_temp.pdf"          
+ PDF_OUTPUT = "signed_output.pdf"      
+ SIGN_IMAGE = "signature.png"           
+ PRIVATE_KEY = "mykey.pem"            
+ CERT_FILE = "mycert.pem"
- Sau khi chạy code py, chữ kí từ ảnh png sẽ được đưa vào file chukiso.pdf và cho ra file signed_output.pdf đã được kí:
  <img width="850" height="758" alt="image" src="https://github.com/user-attachments/assets/e5b19059-a5fe-4dbb-98d2-5d3f54bfe940" />

- Tạo 1 file py để kiểm tra xác thực chữ kí:
  
<img width="1410" height="799" alt="image" src="https://github.com/user-attachments/assets/4b4bd916-cb52-4a0d-a840-f98383eb7025" />

- Sau khi chạy file verify.py, sẽ tạo ra 1 file verify.txt để hiển thị kết quả kiểm tra chứng chỉ và log lại thời gian:
  <img width="900" height="656" alt="image" src="https://github.com/user-attachments/assets/14287ecc-ce27-40df-98d4-2b209063fe9f" />

==> Kết luận: Đã kiểm tra và đáp ứng đủ các yêu cầu xác thực chữ kí, còn thiếu phần kiểm tra OCSP/CRL và timestamp token



           



