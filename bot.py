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
    keywords = memory.get('keywords', ['python', 'ai', 'bot', 'developer', 'engineer'])
    rejected = memory.get('rejected_keywords', ['intern', 'junior'])
    applications = memory.get('applications', [])
    
    if command == '/start':
        send_message("🦁 <b>سلام!</b>\nدستورات:\n/find [عبارت]\n/track : لیست درخواست‌ها\n/applied [شماره]\n/interview [شماره]\n/rejected [شماره]\n/hired [شماره]")
        sys.exit()
    
    elif command == '/status':
        send_message(f"📊 کل: {memory.get('total_seen', 0)}\nدرخواست‌ها: {len(applications)}")
        sys.exit()
    
    elif command == '/track':
        if not applications:
            send_message("📋 لیست خالی است.")
            sys.exit()
        report = "📋 <b>درخواست‌های شما:</b>\n"
        for i, app in enumerate(applications[-5:], 1):
            report += f"{i}. {app['title']} - {app['status']}\n"
        send_message(report)
        sys.exit()
    
    elif command.startswith('/applied ') or command.startswith('/interview ') or command.startswith('/rejected ') or command.startswith('/hired '):
        parts = command.split(' ', 1)
        action = parts[0][1:]
        try:
            num = int(parts[1]) - 1
            if 0 <= num < len(applications):
                applications[num]['status'] = action
                memory['applications'] = applications
                save_memory(memory)
                send_message(f"✅ وضعیت به‌روز شد: {action}")
            else:
                send_message("⚠️ شماره معتبر نیست.")
        except:
            send_message("⚠️ فرمت: /applied 1")
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
                        all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url')})
        except:
            pass
        try:
            r2 = requests.get("https://remotive.com/api/remote-jobs", timeout=15)
            for job in r2.json().get('jobs', []):
                title = job.get('title', '').lower()
                if any(k in title for k in search_terms):
                    if not any(bad in title for bad in rejected):
                        all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url')})
        except:
            pass
        
        if len(all_new_jobs) > 0:job = all_new_jobs[0]
            today = datetime.now().strftime("%Y-%m-%d")
            applications.append({'title': job['title'], 'company': job['company'], 'url': job['url'], 'date': today, 'status': 'applied'})
            memory['applications'] = applications
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
rejected = memory.get('rejected_keywords', ['intern', 'junior'])

try:
    r1 = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=15)
    for job in r1.json().get('data', []):
        title = job.get('title', '').lower()
        if any(k in title for k in keywords) and 'remote' in job.get('location', '').lower():
            if not any(bad in title for bad in rejected):
                if job.get('url') not in memory['seen_urls']:
                    all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url')})
except:
    pass

try:
    r2 = requests.get("https://remotive.com/api/remote-jobs", timeout=15)
    for job in r2.json().get('jobs', []):
        title = job.get('title', '').lower()
        if any(k in title for k in keywords):
            if not any(bad in title for bad in rejected):
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
