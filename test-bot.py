from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from telegram import Bot
import time

# --- KONFIGURASI ---
API_KEY_TELEGRAM = "7848219954:AAHry5Az7HkYpEvZgM46EUhDyahiXoTTako"
CHAT_ID = "@GlobalEkonomiBot"

bot = Bot(token=API_KEY_TELEGRAM)

# Kirim pesan tes otomatis ke bot Telegram
try:
    bot.send_message(chat_id=CHAT_ID, text="Tes kirim pesan otomatis dari bot Telegram!")
    print("Pesan tes berhasil dikirim ke Telegram.")
except Exception as e:
    print("Gagal kirim pesan tes ke Telegram:", e)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.investing.com/economic-calendar/")
time.sleep(10)  

soup = BeautifulSoup(driver.page_source, "html.parser")

# Selector event alternatif berdasarkan struktur umum tabel
events = soup.select("table.genTbl tr")
print("Jumlah event ditemukan:", len(events))

if not events:
    print("Tidak ada event ditemukan.")
else:
    for event in events[:20]:
        tds = event.find_all("td")
        # Filter agar hanya event valid yang dikirim
        if len(tds) >= 5 and tds[3].get_text(strip=True) and tds[3].get_text(strip=True).lower() != "event":
            time_event = tds[0].get_text(strip=True)
            currency = tds[1].get_text(strip=True)
            impact = tds[2].get_text(strip=True)
            event_name = tds[3].get_text(strip=True)
            actual = tds[4].get_text(strip=True)
            # Kirim hanya event berdampak tinggi
            if "High" in impact:
                message = f"📰 {event_name}\n⏰ {time_event}\n💱 {currency}\n🔥 {impact}\n📊 {actual}"
                print(message)
                try:
                    bot.send_message(chat_id=CHAT_ID, text=message)
                except Exception as e:
                    print("Gagal kirim ke Telegram:", e)

driver.quit()
