import json
import datetime
import requests
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

WEBHOOK_URL = "https://discord.com/api/webhooks/1550886464844337192/-JxFQDMJSMQsUL-b83LOdt6lAq2lWiqaK54yPa53shYWOK9NGdX0v8zFXh7OqOjUT4Fb"

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
                    "color": 3447003,
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

def kiem_tra_va_gui():
    # Lấy ngày hiện tại theo giờ Việt Nam (UTC+7)
    gio_utc = datetime.datetime.now(datetime.timezone.utc)
    gio_vn = gio_utc + datetime.timedelta(hours=7)
    thu_hien_tai = gio_vn.weekday()  # 0: T2, 1: T3, 2: T4, 3: T5, 4: T6, 5: T7, 6: CN

    with open("lich_hoc.json", "r", encoding="utf-8") as f:
        data_json = json.load(f)

    cac_ngay_hoc = data_json.get("days", [])

    # 1. Nếu là Chủ Nhật (6) -> Gửi tổng hợp tuần
    if thu_hien_tai == 6:
        print("Hôm nay là Chủ Nhật -> Gửi lịch tổng quan tuần mới.")
        gui_thong_bao("📅 [TỔNG HỢP] Lịch học Automation Test tuần mới")
    
    # 2. Nếu là ngày học trùng trong JSON -> Gửi nhắc nhở
    elif thu_hien_tai in cac_ngay_hoc:
        print(f"Hôm nay (Thứ {thu_hien_tai + 2}) có lịch học -> Gửi nhắc nhở.")
        gui_thong_bao("⏰ [NHẮC NHỞ] Lớp học Automation Test sẽ bắt đầu sau 30 phút nữa (20h00)!")
    
    # 3. Không phải ngày học -> Bỏ qua
    else:
        print(f"Hôm nay (Thứ {thu_hien_tai + 2}) không có lịch học. Bỏ qua.")

if __name__ == "__main__":
    kiem_tra_va_gui()
