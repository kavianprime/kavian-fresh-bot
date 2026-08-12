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
    return {'seen_urls': [], 'total_seen': 0}

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def send_message(text, parse_mode='HTML'):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': parse_mode})

if len(sys.argv) > 1:
    command = sys.argv[1]
    if command == '/start':
        send_message("🦁 <b>سلام رهبر کاویان!</b>\nمن KAVIAN PRIME هستم.\n\nدستورات:\n/status : گزارش وضعیت")
        sys.exit()
    elif command == '/status':
        memory = load_memory()
        msg = f"📊 <b>گزارش وضعیت:</b>\n\n"
        msg += f"🧠 کل پروژه‌ها: {memory.get('total_seen', 0)}\n"
        msg += f"💾 حافظه: {len(memory.get('seen_urls', []))} لینک\n"
        msg += f"⚡ وضعیت: <b>آنلاین ✅</b>"
        send_message(msg)
        sys.exit()

print("🦁 شکارچی چندجبهه‌ای بیدار شد!")
memory = load_memory()
all_new_jobs = []
keywords = ['python', 'ai', 'bot', 'developer', 'engineer']

# منبع اول: Arbeitnow
try:
    response1 = requests.get("https://www.arbeitnow.com/api/job-board-api", headers={'User-Agent': 'KavianPrimeBot/4.0'}, timeout=15)
    data1 = response1.json().get('data', [])
    for job in data1:
        title = job.get('title', '').lower()
        job_url = job.get('url', '')
        if any(k in title for k in keywords) and 'remote' in job.get('location', '').lower():
            if job_url not in memory['seen_urls']:
                score = 70
                if 'senior' in title or 'lead' in title: score += 15
                if 'ai' in title or 'machine learning' in title: score += 10
                all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name', 'Unknown'), 'url': job_url, 'score': min(score, 99)})
except Exception as e:
    print(f"خطا در منبع اول: {e}")

# منبع دوم: Remotive
try:
    response2 = requests.get("https://remotive.com/api/remote-jobs", headers={'User-Agent': 'KavianPrimeBot/4.0'}, timeout=15)
    data2 = response2.json().get('jobs', [])
    for job in data2:
        title = job.get('title', '').lower()
        job_url = job.get('url', '')
        if any(k in title for k in keywords):
            if job_url not in memory['seen_urls']:
                score = 70
                if 'senior' in title or 'lead' in title: score += 15
                if 'ai' in title or 'machine learning' in title: score += 10
                all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name', 'Unknown'), 'url': job_url, 'score': min(score, 99)})
except Exception as e:
    print(f"خطا در منبع دوم: {e}")

if all_new_jobs:
    all_new_jobs.sort(key=lambda x: x['score'], reverse=True)
    msg = "💰 <b>شکارهای هوشمند از ۲ جبهه:</b>\n\n"
    for i, job in enumerate(all_new_jobs[:4], 1):
        emoji = "🔥" if job['score'] >= 90 else "⭐" if job['score'] >= 80 else "✅"
        msg += f"{i}. {emoji} <b>{job['title']}</b> (امتیاز: {job['score']}٪)\n"
        msg += f"   🏢 {job['company']}\n"
        msg += f"   🔗 <a href='{job['url']}'>مشاهده لینک</a>\n\n"
        
        if i == 1 and job['score'] >= 80:
            msg += f"📝 <b>پیشنهاد آماده:</b>\n"
            msg += f"<i>سلام تیم {job['company']}،\nمن متخصص {job['title']} هستم. آمادگی دارم راه‌حل بهینه ارائه دهم.</i>\n\n"
            msg += "━━━━━━━━━━━━━━━━━━━━\n\n"
    
    send_message(msg)print(f"✅ {len(all_new_jobs)} پروژه از ۲ منبع ارسال شد.")
    
    for job in all_new_jobs:
        memory['seen_urls'].append(job['url'])
    memory['total_seen'] = memory.get('total_seen', 0) + len(all_new_jobs)
    save_memory(memory)
else:
    print("⏸️ پروژه جدیدی نیست.")
    send_message("🧠 <b>گزارش:</b>\nامروز شکار جدیدی یافت نشد. ✅")
