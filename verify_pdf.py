from pyhanko.sign.validation import validate_pdf_signature
from pyhanko.pdf_utils.reader import PdfFileReader
from pyhanko_certvalidator import ValidationContext
from datetime import datetime
import os

# ======== Cấu hình =========
PDF_FILE = "signed_output.pdf"      # Tệp PDF đã ký
LOG_FILE = "verify_log.txt"         # File log kết quả
CA_FILE = "ca-trust.pem"            # File CA tin cậy (nếu có)
# ===========================

print("🔍 Bắt đầu kiểm tra chữ ký PDF...")

# 1️⃣ Tạo ValidationContext (kiểm tra chain, OCSP, CRL)
if os.path.exists(CA_FILE):
    vc = ValidationContext(trust_roots=[CA_FILE], allow_fetching=True)
else:
    vc = ValidationContext(allow_fetching=True)  # nếu không có CA thì vẫn cho phép OCSP/CRL

with open(PDF_FILE, "rb") as f:
    reader = PdfFileReader(f)
    sigs = reader.embedded_signatures

    with open(LOG_FILE, "w", encoding="utf-8") as log:
        log.write("=== KẾT QUẢ XÁC THỰC CHỮ KÝ PDF ===\n")
        log.write(f"Thời gian kiểm tra: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        log.write(f"Tệp kiểm tra: {PDF_FILE}\n\n")

        # 2️⃣ Duyệt qua từng chữ ký trong PDF
        for sig in sigs:
            sig_name = sig.field_name
            log.write(f"🔍 Chữ ký: {sig_name}\n")
            print(f"🔍 Kiểm tra chữ ký: {sig_name}")

            # 3️⃣ Xác thực chữ ký (truyền vc như positional argument)
            status = validate_pdf_signature(sig, vc)
            summary = status.summary()
            log.write(f"Trạng thái tổng quát: {summary}\n")

            # 4️⃣ Kiểm tra sửa đổi sau khi ký
            if status.modification_level.name == "MODIFIED":
                log.write("❌ PDF đã bị chỉnh sửa sau khi ký.\n")
            else:
                log.write("✅ PDF không bị thay đổi sau khi ký.\n")

            # 5️⃣ Kiểm tra chứng chỉ tin cậy (chain → CA)
            if status.trusted:
                log.write("✅ Chứng chỉ hợp lệ và nằm trong CA tin cậy.\n")
            else:
                log.write("⚠️ Chứng chỉ không thuộc CA tin cậy hoặc tự ký.\n")

            # 6️⃣ Kiểm tra OCSP/CRL (tình trạng thu hồi chứng chỉ)
            try:
                if hasattr(status, "revinfo_validity") and status.revinfo_validity:
                    if status.revinfo_validity.name == "VALID":
                        log.write("✅ OCSP/CRL: Chứng chỉ chưa bị thu hồi.\n")
                    else:
                        log.write("⚠️ Không thể xác minh hoặc chứng chỉ có thể đã bị thu hồi.\n")
                else:
                    log.write("⚠️ Không có thông tin OCSP/CRL.\n")
            except Exception:
                log.write("⚠️ Không thể kiểm tra OCSP/CRL.\n")

            # 7️⃣ Kiểm tra timestamp (nếu có)
            try:
                ts_info = getattr(status.signer_report, "timestamp_validity", None)
                if ts_info:
                    log.write("✅ Timestamp token hợp lệ.\n")
                else:
                    log.write("⚠️ Không có hoặc timestamp không hợp lệ.\n")
            except Exception:
                log.write("⚠️ Không thể kiểm tra timestamp.\n")

            # 8️⃣ Ghi thông tin kỹ thuật về chữ ký
            log.write("Chi tiết thuật toán:\n")
            try:
                log.write(f" - Thuật toán ký: {status.signing_cert.signature_algo}\n")
                log.write(f" - Thuật toán hash: {status.signing_cert.hash_algo}\n")
            except Exception:
                log.write("⚠️ Không thể đọc thuật toán ký hoặc hash.\n")

            try:
                signer_cert = status.signing_cert.subject.human_friendly
                log.write(f"Người ký: {signer_cert}\n")
            except Exception:
                log.write("⚠️ Không thể đọc thông tin người ký.\n")

            log.write("\n")

        log.write("=== KẾT THÚC XÁC THỰC ===\n")

print("✅ Hoàn tất kiểm tra chữ ký. Kết quả đã lưu tại:", LOG_FILE)
