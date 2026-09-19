import json
import time
import requests
import schedule
import sys

# Ép mã hóa UTF-8 để không bị lỗi Icon/Emoji trên Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

WEBHOOK_URL = "https://discord.com/api/webhooks/1550886464844337192/-JxFQDMJSMQsUL-b83LOdt6lAq2lWiqaK54yPa53shYWOK9NGdX0v8zFXh7OqOjUT4Fb"

# Hàm gửi thông báo chung từ file lich_hoc.json
def gui_thong_bao(tieude_tuy_chinh=None):
    try:
        with open("lich_hoc.json", "r", encoding="utf-8") as f:
            data_json = json.load(f)

        title = tieude_tuy_chinh if tieude_tuy_chinh else data_json.get("title", "📅 Lịch học tuần này")
        description_text = "\n".join(data_json.get("schedule", []))

        payload = {
            "embeds": [
                {
                    "title": title,
                    "description": description_text,
                    "color": 3447003,  # Màu xanh dương
                    "footer": {
                        "text": data_json.get("footer", "")
                    }
                }
            ]
        }

        response = requests.post(WEBHOOK_URL, json=payload)

        if response.status_code == 204:
            print(f"[THÀNH CÔNG] Đã gửi thông báo: '{title}'")
        else:
            print(f"[LỖI {response.status_code}]:", response.text)

    except Exception as e:
        print("[LỖI THỰC THI]:", e)

# 1. Nhắc lịch học tổng quan tối Chủ Nhật (20h00)
def thong_bao_chu_nhat():
    gui_thong_bao("📅 [TỔNG HỢP] Lịch học Automation Test tuần mới")

# 2. Nhắc nhở trước giờ học 30 phút (19h00 Thứ 4 & Thứ 6)
def nhac_nho_truoc_buoi_hoc():
    gui_thong_bao("⏰ [NHẮC NHỞ] Lớp học Automation Test sẽ bắt đầu sau 30 phút nữa (20h00)!")


# ==============================================================================
# 🔥 PHẦN 1: CHẠY TEST NGAY LẬP TỨC (Sau khi test xong, hãy COMMENT đoạn này lại)
# ==============================================================================
if __name__ == "__main__":
    print("⏳ Đang gửi tin nhắn TEST lên Discord...")
    gui_thong_bao("🧪 [TEST] Thông báo thử nghiệm hệ thống Discord Webhook")


# ==============================================================================
# ⏰ PHẦN 2: CHẠY LỊCH TỰ ĐỘNG NẾU MÁY TÍNH TREO CHƯƠNG TRÌNH NGẦM 
# (Nếu dùng GitHub Actions ở bước dưới thì KHÔNG CẦN đoạn vòng lặp while True này)
# ==============================================================================
"""
schedule.every().sunday.at("20:00").do(thong_bao_chu_nhat)
schedule.every().wednesday.at("19:00").do(nhac_nho_truoc_buoi_hoc)
schedule.every().friday.at("19:00").do(nhac_nho_truoc_buoi_hoc)

print("🚀 Bot đang chạy ngầm trên máy cá nhân...")
while True:
    schedule.run_pending()
    time.sleep(30)
"""
