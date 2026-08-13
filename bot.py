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
    return {'seen_urls': [], 'total_seen': 0, 'keywords': ['python', 'ai', 'bot', 'developer', 'engineer'], 'rejected_keywords': ['intern', 'junior']}

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def send_message(text):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api_url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'})

if len(sys.argv) > 1:
    command = sys.argv[1]
    memory = load_memory()
    keywords = memory.get('keywords', ['python', 'ai', 'bot', 'developer', 'engineer'])
    rejected = memory.get('rejected_keywords', ['intern', 'junior'])
    
    if command == '/start':
        msg = "🦁 <b>سلام رهبر کاویان!</b>\nمن KAVIAN PRIME هستم.\n\n"
        msg += "دستورات:\n"
        msg += "/status : گزارش وضعیت\n"
        msg += "/keywords : کلمات کلیدی\n"
        msg += "/add [کلمه] : افزودن به شکار\n"
        msg += "/reject [کلمه] : لیست سیاه\n"
        msg += "/remove [کلمه] : حذف از لیست سیاه\n"
        msg += "/find [عبارت] : جستجوی فوری"
        send_message(msg)
        sys.exit()
    
    elif command == '/status':
        msg = f"📊 <b>وضعیت سیستم:</b>\nکل پروژه‌ها: {memory.get('total_seen', 0)}\nحافظه: {len(memory.get('seen_urls', []))} لینک\nوضعیت: <b>آنلاین ✅</b>"
        send_message(msg)
        sys.exit()
    
    elif command == '/keywords':
        send_message("🔑 <b>کلمات فعال:</b>\n" + "، ".join(keywords))
        sys.exit()
    
    elif command.startswith('/add '):
        new_kw = command.split(' ', 1)[1].strip().lower()
        if new_kw and new_kw not in keywords:
            keywords.append(new_kw)
            memory['keywords'] = keywords
            save_memory(memory)
            send_message(f"✅ <b>{new_kw}</b> اضافه شد!")
        sys.exit()
    
    elif command.startswith('/reject '):
        bad_kw = command.split(' ', 1)[1].strip().lower()
        if bad_kw and bad_kw not in rejected:
            rejected.append(bad_kw)
            memory['rejected_keywords'] = rejected
            save_memory(memory)
            send_message(f"🚫 <b>{bad_kw}</b> به لیست سیاه اضافه شد!")
        sys.exit()
    
    elif command.startswith('/remove '):
        rem_kw = command.split(' ', 1)[1].strip().lower()
        if rem_kw in rejected:
            rejected.remove(rem_kw)
            memory['rejected_keywords'] = rejected
            save_memory(memory)
            send_message(f"✅ <b>{rem_kw}</b> حذف شد.")
        sys.exit()
    
    elif command.startswith('/find '):
        query = command.split(' ', 1)[1].strip().lower()
        search_terms = query.split()
        all_new_jobs = []
        try:
            r1 = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=15)
            for job in r1.json().get('data', []):
                title = job.get('title', '').lower()
                if any(k in title for k in search_terms) and 'remote' in job.get('location', '').lower():
                    if not any(bad in title for bad in rejected):
                        all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url'), 'score': 85})
        except: pass
        try:
            r2 = requests.get("https://remotive.com/api/remote-jobs", timeout=15)
            for job in r2.json().get('jobs', []):
                title = job.get('title', '').lower()
                if any(k in title for k in search_terms):
                    if not any(bad in title for bad in rejected):
                        all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url'), 'score': 85})
        except: pass
        
        if len(all_new_jobs) > 0:
            all_new_jobs.sort(key=lambda x: x['score'], reverse=True)
            report = "🔍 <b>گزارش جستجوی فوری:</b>\n━━━━━━━━━━━━━━━━━━━━\n"
            for i, job in enumerate(all_new_jobs[:3], 1):
                badge = "💎 <b>الماس روز (بهترین تطابق)</b>\n" if i == 1 else ""
                report += f"{badge}{i}. 🔥 <b>{job['title']}</b>\n"
                report += f"   🏢 {job['company']}\n"
                if i == 1:
                    report += f"   📝 <i>پیشنهاد: سلام تیم {job['company']}، من آماده ارائه راه‌حل بهینه هستم.</i>\n"
                report += f"   🔗 <a href='{job['url']}'>مشاهده و اقدام</a>\n\n"
            send_message(report)
        else:
            send_message("❌ موردی با این مشخصات یافت نشد.")
        sys.exit()

print("🦁 شکارچی با گزارشگر اجرایی بیدار شد!")
memory = load_memory()
all_new_jobs = []
keywords = memory.get('keywords', ['python', 'ai', 'bot', 'developer', 'engineer'])
rejected = memory.get('rejected_keywords', ['intern', 'junior'])

try:
    r1 = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=15)
    for job in r1.json().get('data', []):
        title = job.get('title', '').lower()
        if any(k in title for k in keywords) and 'remote' in job.get('location', '').lower():
            if not any(bad in title for bad in rejected):
                if job.get('url') not in memory['seen_urls']:
                    score = 70
                    if 'senior' in title or 'lead' in title: score += 15
                    if 'ai' in title or 'machine learning' in title: score += 10
                    all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url'), 'score': score})
except: pass

try:
    r2 = requests.get("https://remotive.com/api/remote-jobs", timeout=15)
    for job in r2.json().get('jobs', []):
        title = job.get('title', '').lower()
        if any(k in title for k in keywords):
            if not any(bad in title for bad in rejected):
                if job.get('url') not in memory['seen_urls']:
                    score = 70
                    if 'senior' in title or 'lead' in title: score += 15
                    if 'ai' in title or 'machine learning' in title: score += 10
                    all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url'), 'score': score})
except: pass

if len(all_new_jobs) > 0:
    all_new_jobs.sort(key=lambda x: x['score'], reverse=True)
    report = "📊 <b>گزارش اجرایی هوشمند KAVIAN PRIME</b>\n"
    report += "━━━━━━━━━━━━━━━━━━━━\n"
    for i, job in enumerate(all_new_jobs[:3], 1):
        badge = "💎 <b>الماس روز (بهترین تطابق)</b>\n" if i == 1 else ""
        report += f"{badge}{i}. 🔥 <b>{job['title']}</b> (امتیاز: {job['score']}٪)\n"
        report += f"   🏢 {job['company']}\n"
        if i == 1:
            report += f"   📝 <i>پیشنهاد: سلام تیم {job['company']}، من متخصص {job['title']} هستم و آماده ارائه راه‌حل بهینه.</i>\n"
        report += f"   🔗 <a href='{job['url']}'>مشاهده و اقدام</a>\n\n"
    
    send_message(report)
    
    for job in all_new_jobs:
        memory['seen_urls'].append(job['url'])
    memory['total_seen'] = memory.get('total_seen', 0) + len(all_new_jobs)
    save_memory(memory)
    print(f"✅ گزارش اجرایی ارسال شد.")
else:
    send_message("⏸️ <b>گزارش:</b>\nامروز شکار جدیدی یافت نشد. ربات در حال اسکن مداوم است. ✅")
