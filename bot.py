import requests
import json
import os
import sys
from datetime import datetime

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
    return {'seen_urls': [], 'total_seen': 0, 'keywords': ['python', 'ai', 'bot', 'developer', 'engineer'], 'rejected_keywords': ['intern', 'junior'], 'applications': []}

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def send_message(text):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api_url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'})

if len(sys.argv) > 1:
    command = sys.argv[1]
    memory = load_memory()
    
    if command == '/start':
        send_message("🦁 <b>سلام!</b>\nدستورات:\n/find [عبارت]\n/track : لیست درخواست‌ها\n/applied [شماره]\n/hired [شماره]")
        sys.exit()
    
    elif command == '/track':
        apps = memory.get('applications', [])
        if not apps:
            send_message("📋 لیست خالی است.")
            sys.exit()
        report = "📋 <b>درخواست‌های شما:</b>\n"
        for i, app in enumerate(apps[-5:], 1):
            report += f"{i}. {app['title']} - {app['status']}\n"
        send_message(report)
        sys.exit()
    
    elif command.startswith('/applied '):
        try:
            num = int(command.split(' ')[1]) - 1
            apps = memory.get('applications', [])
            if 0 <= num < len(apps):
                apps[num]['status'] = 'applied'
                memory['applications'] = apps
                save_memory(memory)
                send_message(f"✅ به‌روز شد: {apps[num]['title']}")
            sys.exit()
        except:
            send_message("⚠️ فرمت: /applied 1")
            sys.exit()
    
    elif command.startswith('/hired '):
        try:
            num = int(command.split(' ')[1]) - 1
            apps = memory.get('applications', [])
            if 0 <= num < len(apps):
                apps[num]['status'] = 'hired'
                memory['applications'] = apps
                save_memory(memory)
                send_message(f"🎉 استخدام شدی: {apps[num]['title']}")
            sys.exit()
        except:
            send_message("⚠️ فرمت: /hired 1")
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
                    all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url')})
        except:
            pass
        
        if len(all_new_jobs) > 0:
            job = all_new_jobs[0]
            today = datetime.now().strftime("%Y-%m-%d")
            apps = memory.get('applications', [])
            apps.append({'title': job['title'], 'company': job['company'], 'url': job['url'], 'date': today, 'status': 'applied'})
            memory['applications'] = apps
            save_memory(memory)
            
            report = f"💎 <b>{job['title']}</b>\n🏢 {job['company']}\n🔗 <a href='{job['url']}'>مشاهده</a>\n\n✅ به لیست درخواست‌ها اضافه شد!"
            send_message(report)
        else:
            send_message("❌ موردی یافت نشد.")
        sys.exit()

print("🦁 شکارچی بیدار شد!")
memory = load_memory()
all_new_jobs = []
keywords = memory.get('keywords', ['python', 'ai', 'bot', 'developer', 'engineer'])
try:
    r1 = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=15)
    for job in r1.json().get('data', []):
        title = job.get('title', '').lower()
        if any(k in title for k in keywords) and 'remote' in job.get('location', '').lower():
            if job.get('url') not in memory['seen_urls']:
                all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url')})
except:
    pass

if len(all_new_jobs) > 0:
    job = all_new_jobs[0]
    report = f"💰 <b>شکار امروز:</b>\n💎 <b>{job['title']}</b>\n🏢 {job['company']}\n🔗 <a href='{job['url']}'>مشاهده</a>"
    send_message(report)
    for j in all_new_jobs:
        memory['seen_urls'].append(j['url'])
    memory['total_seen'] = memory.get('total_seen', 0) + len(all_new_jobs)
    save_memory(memory)
else:
    send_message("⏸️ پروژه جدیدی نیست.")
