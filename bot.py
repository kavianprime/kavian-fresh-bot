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
    return {
        'seen_urls': [], 
        'total_seen': 0, 
        'keywords': ['python', 'ai', 'bot', 'developer', 'engineer'], 
        'rejected_keywords': ['intern', 'junior'], 
        'applications': [],
        'golden_keywords': []
    }

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
        msg += "/stats : 🧠 تحلیل هوشمند و DNA تکامل‌یافته\n"
        msg += "/export : دانلود فایل اکسل\n\n"
        msg += "⚙️ <b>مدیریت وضعیت:</b>\n"
        msg += "/interview [شماره] : مصاحبه (یادگیری)\n"
        msg += "/hired [شماره] : استخدام (یادگیری)\n"
        msg += "/rejected [شماره] : رد شد"
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
        
        report = "🧠 <b>داشبورد تحلیل و تکامل KAVIAN GENESIS</b>\n"
        report += "━━━━━━━━━━━━━━━━━━━━\n"
        report += f"🎯 <b>کل درخواست‌ها:</b> {total}\n"
        report += f"📤 <b>در حال انتظار:</b> {applied}\n"
        report += f"🎤 <b>موفق (مصاحبه):</b> {interview}\n"
        report += f"❌ <b>رد شده:</b> {rejected}\n"
        report += f"🎉 <b>استخدام شده:</b> {hired}\n\n"
        report += f"📈 <b>نرخ موفقیت:</b> <b>{success_rate}٪</b>\n"
        report += "━━━━━━━━━━━━━━━━━━━━\n"
        
        golden = memory.get('golden_keywords', [])
        if golden:
            report += f"\n🧬 <b>الگوهای طلایی آموخته‌شده (DNA تکامل‌یافته):</b>\n"
            report += "، ".join(golden) + "\n"
            report += "<i>(سیستم در شکارهای بعدی به این کلمات امتیاز ویژه می‌دهد)</i>\n"
        else:
            report += "\n💡 <b>بینش:</b> هنوز الگوی طلایی کشف نشده. با /interview یا /hired به سیستم یاد بده چه چیزهایی برایت ارزشمندند.\n"
            
        send_message(report)
        sys.exit()
    
    elif command == '/export':
        if not apps:
            send_message("📋 لیست خالی است.")
            sys.exit()
            csv_content = "Title,Company,Date,Status,URL\n"
        for app in apps:
            csv_content += f'"{app["title"]}","{app["company"]}","{app["date"]}","{app["status"]}","{app["url"]}"\n'
        with open('applications.csv', 'w', encoding='utf-8') as f:
            f.write(csv_content)
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open('applications.csv', 'rb') as f:
            requests.post(api_url, files={'document': f}, data={'chat_id': CHAT_ID, 'caption': '📊 <b>گزارش اکسل</b>'})
        sys.exit()
    
    elif command.startswith('/interview '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'interview'
                memory['applications'] = apps
                
                # Genesis Learning Engine: Extract Golden Patterns
                title = apps[num]['title'].lower()
                tech_words = ['python', 'ai', 'react', 'node', 'aws', 'docker', 'crypto', 'web3', 'bot', 'api', 'data', 'ml', 'llm', 'gpt', 'rust', 'go', 'java']
                learned = []
                for tw in tech_words:
                    if tw in title and tw not in memory.get('golden_keywords', []):
                        memory.setdefault('golden_keywords', []).append(tw)
                        learned.append(tw)
                save_memory(memory)
                
                msg = f"🎤 عالی! وضعیت به‌روز شد: {apps[num]['title']}\n"
                if learned:
                    msg += f"\n🧬 <b>سیستم یاد گرفت!</b> کلمات طلایی جدید به DNA اضافه شد: {', '.join(learned)}"
                send_message(msg)
            sys.exit()
        except:
            send_message("⚠️ فرمت صحیح: /interview 1")
            sys.exit()
            
    elif command.startswith('/hired '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'hired'
                memory['applications'] = apps
                
                # Genesis Learning Engine
                title = apps[num]['title'].lower()
                tech_words = ['python', 'ai', 'react', 'node', 'aws', 'docker', 'crypto', 'web3', 'bot', 'api', 'data', 'ml', 'llm', 'gpt', 'rust', 'go', 'java']
                learned = []
                for tw in tech_words:
                    if tw in title and tw not in memory.get('golden_keywords', []):
                        memory.setdefault('golden_keywords', []).append(tw)
                        learned.append(tw)
                save_memory(memory)
                
                msg = f"🎉🔥 تبریک رهبر! استخدام شدی: {apps[num]['title']}\n"
                if learned:
                    msg += f"\n🧬 <b>سیستم تکامل یافت!</b> DNA جدید: {', '.join(learned)}"
                send_message(msg)
            sys.exit()
        except:
            send_message("⚠️ فرمت صحیح: /hired 1")
            sys.exit()
            
    elif command.startswith('/rejected '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'rejected'
                memory['applications'] = apps
                save_memory(memory)
                send_message(f"❌ ثبت شد: {apps[num]['title']} (سیستم از این الگو دوری می‌کند)")
            sys.exit()
        except:
            send_message("⚠️ فرمت صحیح: /rejected 1")
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
            report += "✅ <b>به لیست درخواست‌ها اضافه شد.</b>"
            send_message(report)
        else:
            send_message("❌ موردی یافت نشد.")
        sys.exit()

print("🦁 KAVIAN GENESIS: روز ۲۳ - موتور تکامل بیدار شد!")
memory = load_memory()
all_new_jobs = []
keywords = memory.get('keywords', ['python', 'ai', 'bot', 'developer', 'engineer'])
golden = memory.get('golden_keywords', [])

try:
    r1 = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=15)
    for job in r1.json().get('data', []):
        title = job.get('title', '').lower()
        if any(k in title for k in keywords) and 'remote' in job.get('location', '').lower():
            if job.get('url') not in memory['seen_urls']:
                # Genesis Scoring: Boost if Golden Pattern found
                score = 70
                for gk in golden:
                    if gk in title:
                        score += 30 
                if 'senior' in title or 'lead' in title: score += 15
                
                all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url'), 'score': score})
except:
    pass

if len(all_new_jobs) > 0:
    all_new_jobs.sort(key=lambda x: x['score'], reverse=True)
    job = all_new_jobs[0]
    
    msg = f"💰 <b>شکار خودکار امروز (با هوش تکامل‌یافته):</b>\n"
    msg += f"💎 <b>{job['title']}</b> (امتیاز: {job['score']})\n"
    msg += f"🏢 {job['company']}\n"
    msg += f"🔗 <a href='{job['url']}'>مشاهده</a>"
    
    if job['score'] >= 100:
        msg += "\n\n🧬 <b>هشدار DNA:</b> این پروژه دارای الگوهای طلایی آموخته‌شده است! اولویت بسیار بالا."
        
    send_message(msg)
    for j in all_new_jobs:
        memory['seen_urls'].append(j['url'])
    memory['total_seen'] = memory.get('total_seen', 0) + len(all_new_jobs)
    save_memory(memory)
else:
    send_message("⏸️ پروژه جدیدی نیست. سیستم در حال اسکن مداوم است.")
