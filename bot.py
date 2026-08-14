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
        msg = "🦁 <b>سلام رهبر کاویان!</b>\nمن KAVIAN GENESIS هستم.\n\n"
        msg += "🔍 <b>شکار و مدیریت:</b>\n"
        msg += "/find [عبارت] : جستجو و ثبت پروژه\n"
        msg += "/track : لیست درخواست‌ها\n"
        msg += "/stats : 🧠 تحلیل هوشمند و کشف الگو\n"
        msg += "/export : دانلود فایل اکسل\n\n"
        msg += "⚙️ <b>مدیریت وضعیت:</b>\n"
        msg += "/applied [شماره] : ارسال شد\n"
        msg += "/interview [شماره] : مصاحبه\n"
        msg += "/rejected [شماره] : رد شد\n"
        msg += "/hired [شماره] : استخدام!"
        send_message(msg)
        sys.exit()
    
    elif command == '/track':
        if not apps:
            send_message("📋 لیست درخواست‌های شما خالی است.")
            sys.exit()
        report = "📋 <b>آخرین درخواست‌های شما:</b>\n"
        for i, app in enumerate(apps[-10:], 1):
            report += f"{i}. {app['title']} - {app['status']}\n"
        send_message(report)
        sys.exit()
    
    elif command == '/stats':
        if not apps:
            send_message("📊 هنوز داده‌ای برای تحلیل وجود ندارد. با /find شروع کن!")
            sys.exit()
        
        total = len(apps)
        applied = len([a for a in apps if a['status'] == 'applied'])
        interview = len([a for a in apps if a['status'] == 'interview'])
        rejected = len([a for a in apps if a['status'] == 'rejected'])
        hired = len([a for a in apps if a['status'] == 'hired'])
        
        success_count = interview + hired
        success_rate = round((success_count / total) * 100, 1) if total > 0 else 0
        
        report = "🧠 <b>داشبورد تحلیل هوشمند KAVIAN GENESIS</b>\n"
        report += "━━━━━━━━━━━━━━━━━━━━\n"
        report += f"🎯 <b>کل درخواست‌های ثبت‌شده:</b> {total}\n"
        report += f"📤 <b>در حال انتظار (ارسال شده):</b> {applied}\n"
        report += f"🎤 <b>موفق (مرحله مصاحبه):</b> {interview}\n"
        report += f"❌ <b>رد شده:</b> {rejected}\n"
        report += f"🎉 <b>استخدام شده (پیروزی):</b> {hired}\n\n"
        report += f"📈 <b>نرخ پاسخ‌دهی و موفقیت:</b> <b>{success_rate}٪</b>\n"
        report += "━━━━━━━━━━━━━━━━━━━━\n"
        
        if success_rate >= 20:
            insight = "💡 <b>بینش هوشمند:</b> عالی است! استراتژی فعلی تو بسیار موفق است. همین مسیر را ادامه بده."
        elif success_rate >= 5:
            insight = "💡 <b>بینش هوشمند:</b> خوب است، اما جای رشد دارد. سعی کن کاور لترها را شخصی‌سازی‌تر کنی."
        else:
            insight = "💡 <b>بینش هوشمند:</b> نرخ موفقیت پایین است. پیشنهاد می‌کنم کلمات کلیدی (/keywords) را بازبینی کنی و فقط روی پروژه‌های 'الماس' تمرکز کنی."
            
        report += f"\n{insight}"
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
            requests.post(api_url, files={'document': f}, data={'chat_id': CHAT_ID, 'caption': '📊 <b>گزارش اکسل درخواست‌های شما</b>\nاین فایل را دانلود و در کامپیوتر باز کنید.'})
        sys.exit()
    
    elif command.startswith('/applied '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'applied'
                memory['applications'] = apps
                save_memory(memory)
                send_message(f"✅ وضعیت به‌روز شد: {apps[num]['title']}")
            sys.exit()
        except:
            send_message("⚠️ فرمت صحیح: /applied 1")
            sys.exit()
            
    elif command.startswith('/interview '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'interview'
                memory['applications'] = apps
                save_memory(memory)
                send_message(f"🎤 عالی! وضعیت به‌روز شد: {apps[num]['title']}")
            sys.exit()
        except:
            send_message("⚠️ فرمت صحیح: /interview 1")
            sys.exit()
            
    elif command.startswith('/rejected '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'rejected'
                memory['applications'] = apps
                save_memory(memory)
                send_message(f"❌ ثبت شد: {apps[num]['title']} (سیستم از این الگو یاد می‌گیرد)")
            sys.exit()
        except:
            send_message("⚠️ فرمت صحیح: /rejected 1")
            sys.exit()
    
    elif command.startswith('/hired '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'hired'
                memory['applications'] = apps
                save_memory(memory)
                send_message(f"🎉🔥 تبریک رهبر کاویان! استخدام شدی: {apps[num]['title']}")
            sys.exit()
        except:
            send_message("⚠️ فرمت صحیح: /hired 1")
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
            apps.append({'title': job['title'], 'company': job['company'], 'url': job['url'], 'date': today, 'status': 'applied'})
            memory['applications'] = apps
            save_memory(memory)
            
            report = f"💎 <b>{job['title']}</b>\n"
            report += f"🏢 {job['company']}\n"
            report += f"🔗 <a href='{job['url']}'>مشاهده و اقدام</a>\n\n"
            report += "✅ <b>این پروژه به لیست درخواست‌های شما اضافه شد و سیستم آن را ردیابی می‌کند.</b>"
            send_message(report)
        else:
            send_message("❌ موردی با این مشخصات یافت نشد.")
        sys.exit()
        
