send_message(f"✅ به‌روز شد: {apps[num]['title']}")
            sys.exit()
        except:
            send_message("⚠️ فرمت: /applied 1")
            sys.exit()
    
    elif command.startswith('/hired '):
        try:
            num = int(command.split(' ')[1]) - 1
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
        except: pass
        
        if len(all_new_jobs) > 0:
            job = all_new_jobs[0]
            today = datetime.now().strftime("%Y-%m-%d")
            apps.append({'title': job['title'], 'company': job['company'], 'url': job['url'], 'date': today, 'status': 'applied'})
            memory['applications'] = apps
            save_memory(memory)
            send_message(f"💎 <b>{job['title']}</b>\n🏢 {job['company']}\n🔗 <a href='{job['url']}'>مشاهده</a>\n\n✅ به لیست درخواست‌ها اضافه شد!")
        else:
            send_message("❌ موردی یافت نشد.")
        sys.exit()

print("🦁 شکارچی با تحلیلگر آماری بیدار شد!")
memory = load_memory()
all_new_jobs = []
keywords = memory.get('keywords', ['python', 'ai', 'bot', 'developer', 'engineer'])

# بررسی یادآورهای پیگیری
apps = memory.get('applications', [])
today_date = datetime.now().date()
for app in apps:
    if app['status'] == 'applied':
        try:
            app_date = datetime.strptime(app['date'], "%Y-%m-%d").date()
            if (today_date - app_date).days == 3:
                follow_msg = f"⏰ <b>یادآور هوشمند پیگیری:</b>\n\n"
                follow_msg += f"رهبر کاویان، ۳ روز از درخواست تو به <b>{app['company']}</b> گذشت.\n\n"
                follow_msg += f"📝 <b>متن پیگیری آماده:</b>\n"
                follow_msg += f"<i>موضوع: پیگیری درخواست - {app['title']}\n\nتیم محترم {app['company']}،\nپیرو درخواست قبلی‌ام، خواستم مجدداً علاقه‌مندی‌ام را اعلام کنم.\nبا سپاس.</i>"
                send_message(follow_msg)
        except: pass

# شکار روزانه
try:
    r1 = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=15)
    for job in r1.json().get('data', []):
        title = job.get('title', '').lower()
        if any(k in title for k in keywords) and 'remote' in job.get('location', '').lower():
            if job.get('url') not in memory['seen_urls']:
                all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url')})
except: pass

if len(all_new_jobs) > 0:
    job = all_new_jobs[0]
    send_message(f"💰 <b>شکار امروز:</b>\n💎 <b>{job['title']}</b>\n🏢 {job['company']}\n🔗 <a href='{job['url']}'>مشاهده</a>")
    for j in all_new_jobs:
        memory['seen_urls'].append(j['url'])
    memory['total_seen'] = memory.get('total_seen', 0) + len(all_new_jobs)
    save_memory(memory)
else:
    send_message("⏸️ پروژه جدیدی نیست.")
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
    apps = memory.get('applications', [])
    
    if command == '/start':
        send_message("🦁 <b>سلام رهبر کاویان!</b>\nدستورات:\n/find [عبارت]\n/track : لیست درخواست‌ها\n/stats : تحلیل آماری\n/export : دانلود اکسل\n/applied [شماره]\n/hired [شماره]")
        sys.exit()
    
    elif command == '/track':
        if not apps:
            send_message("📋 لیست خالی است.")
            sys.exit()
        report = "📋 <b>آخرین درخواست‌های شما:</b>\n"
        for i, app in enumerate(apps[-10:], 1):
            report += f"{i}. {app['title']} - {app['status']}\n"
        send_message(report)
        sys.exit()
    
    elif command == '/stats':
        if not apps:
            send_message("📊 هنوز داده‌ای برای تحلیل وجود ندارد.")
            sys.exit()
        
        total = len(apps)
        applied = len([a for a in apps if a['status'] == 'applied'])
        interview = len([a for a in apps if a['status'] == 'interview'])
        rejected = len([a for a in apps if a['status'] == 'rejected'])
        hired = len([a for a in apps if a['status'] == 'hired'])
        
        response_rate = round(((interview + hired) / total) * 100, 1) if total > 0 else 0
        
        report = "📊 <b>داشبورد تحلیل هوشمند KAVIAN NEXUS</b>\n"
        report += "━━━━━━━━━━━━━━━━━━━━\n"
        report += f"🎯 <b>کل درخواست‌ها:</b> {total}\n"
        report += f"📤 <b>ارسال شده:</b> {applied}\n"
        report += f"🎤 <b>در مرحله مصاحبه:</b> {interview}\n"
        report += f"❌ <b>رد شده:</b> {rejected}\n"
        report += f"🎉 <b>استخدام شده:</b> {hired}\n\n"
        report += f"📈 <b>نرخ پاسخ‌دهی (Response Rate):</b> <b>{response_rate}٪</b>\n"
        report += "━━━━━━━━━━━━━━━━━━━━\n"
        report += "<i>💡 نکته: برای بهبود این نرخ، کاور لترهای خود را شخصی‌سازی‌تر کنید.</i>"
        send_message(report)
        sys.exit()
    
    elif command == '/export':
        if not apps:
            send_message("📋 لیست خالی است، چیزی برای خروجی گرفتن نیست.")
            sys.exit()
        csv_content = "Title,Company,Date,Status,URL\n"
        for app in apps:
            csv_content += f'"{app["title"]}","{app["company"]}","{app["date"]}","{app["status"]}","{app["url"]}"\n'
        with open('applications.csv', 'w', encoding='utf-8') as f:
            f.write(csv_content)
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open('applications.csv', 'rb') as f:
            requests.post(api_url, files={'document': f}, data={'chat_id': CHAT_ID, 'caption': '📊 <b>گزارش اکسل درخواست‌های شما</b>'})
        sys.exit()
    
    elif command.startswith('/applied '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'applied'
                memory['applications'] = apps
                save_memory(memory)
