import requests
import json
import os
import sys

BOT_TOKEN = "8811972038:AAEupegBge-WDbG-D8G9nodoz1E8Nj7MYN0"
CHAT_ID = "6128663089"
MEMORY_FILE = "kavian_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {'seen_urls': [], 'total_seen': 0, 'preferences': []}

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def send_message(text, parse_mode='HTML'):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': parse_mode})

# بررسی دستورات (Commands)
if len(sys.argv) > 1:
    command = sys.argv[1]
    
    if command == '/start':
        send_message("🦁 <b>سلام رهبر کاویان!</b>\nمن KAVIAN PRIME هستم، دستیار هوشمند و خودمختار تو.\n\nدستورات موجود:\n/status : گزارش وضعیت حافظه و شکارها\n/find [keyword] : جستجوی دستی (به زودی)")
        sys.exit()
        
    elif command == '/status':
        memory = load_memory()
        msg = f"📊 <b>گزارش وضعیت KAVIAN NEXUS:</b>\n\n"
        msg += f"🧠 کل پروژه‌های دیده شده: {memory.get('total_seen', 0)}\n"
        msg += f"💾 حجم حافظه: {len(memory.get('seen_urls', []))} لینک منحصر‌به‌فرد\n"
        msg += f"⚡ وضعیت سیستم: <b>کاملاً پایدار و آنلاین ✅</b>"
        send_message(msg)
        sys.exit()

# حالت پیش‌فرض: شکار روزانه (Daily Hunt)
print("🦁 شکارچی هوشمند بیدار شد!")
memory = load_memory()

url = "https://www.arbeitnow.com/api/job-board-api"
headers = {'User-Agent': 'KavianPrimeBot/1.0'}

try:
    response = requests.get(url, headers=headers, timeout=15)
    data = response.json().get('data', [])
    
    new_jobs = []
    for job in data:
        title = job.get('title', '').lower()
        job_url = job.get('url', '')
        if ('python' in title or 'ai' in title or 'bot' in title) and 'remote' in job.get('location', '').lower():
            if job_url not in memory['seen_urls']:
                new_jobs.append({'title': job.get('title'), 'company': job.get('company_name', 'Unknown'), 'url': job_url})

    if new_jobs:
        msg = "💰 <b>پروژه‌های جدید شکار شد:</b>\n\n"
        for i, job in enumerate(new_jobs[:3], 1):
            msg += f"{i}. <b>{job['title']}</b>\n   🏢 {job['company']}\n   🔗 <a href='{job['url']}'>مشاهده لینک</a>\n\n"
        
        # اضافه کردن دکمه‌های تعاملی (Inline Keyboard)
        keyboard = {
            "inline_keyboard": [
                [{"text": "✅ ذخیره در حافظه", "callback_data": "save"},
                 {"text": "❌ نادیده گرفتن", "callback_data": "ignore"}]
            ]
        }
        
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'HTML', 'reply_markup': json.dumps(keyboard)})
        print("✅ گزارش تعاملی ارسال شد.")
        
        for job in new_jobs:
            memory['seen_urls'].append(job['url'])
        memory['total_seen'] = memory.get('total_seen', 0) + len(new_jobs)
        save_memory(memory)
    else:
        print("⏸️ پروژه جدیدی نیست.")
        # ارسال پیام وضعیت حتی اگر کاری نباشد، تا بدانی ربات زنده است
        send_message("🧠 <b>گزارش روزانه:</b>\nامروز پروژه‌ی جدیدی مطابق معیارها یافت نشد. ربات در حالت آماده‌باش و اسکن مداوم است. ✅")

except Exception as e:
    print(f"❌ خطا: {e}")
    send_message(f"⚠️ <b>هشدار سیستم:</b>\nخطایی در اسکن رخ داد: {str(e)}")
