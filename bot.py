if learned:
                    msg += f"\n🧬 <b>سیستم تکامل یافت!</b> DNA مثبت: {', '.join(learned)}"
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
                
                title = apps[num]['title'].lower()
                bad_words = ['intern', 'junior', 'unpaid', 'volunteer', 'commission', 'trainee', 'entry-level', 'part-time']
                learned_bad = [bw for bw in bad_words if bw in title and bw not in memory.get('blacklisted_keywords', [])]
                if learned_bad:
                    memory.setdefault('blacklisted_keywords', []).extend(learned_bad)
                save_memory(memory)
                
                msg = f"❌ ثبت شد: {apps[num]['title']}\n"
                if learned_bad:
                    msg += f"\n🛡️ <b>سیستم ایمنی فعال شد!</b> DNA منفی: {', '.join(learned_bad)}"
                else:
                    msg += "\n🛡️ <b>سیستم ایمنی:</b> این پروژه در حافظه منفی ثبت شد."
                send_message(msg)
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
            
            golden = memory.get('golden_keywords', [])
            pitch = generate_smart_pitch(job['title'], job['company'], golden)
            
            report = f"💎 <b>{job['title']}</b>\n"
            report += f"🏢 {job['company']}\n"
            report += f"🔗 <a href='{job['url']}'>مشاهده آگهی</a>\n\n"
            report += f"🎨 <b>پیشنهاد طراحی‌شده توسط موتور مولد (آماده ارسال):</b>\n"
            report += f"<i>{pitch}</i>\n\n"
            report += "✅ <b>به لیست درخواست‌ها اضافه شد.</b>"
            send_message(report)
        else:
            send_message("❌ موردی یافت نشد.")
        sys.exit()

print("🦁 KAVIAN GENESIS: روز ۲۵ - موتور طراحی مولد بیدار شد!")
memory = load_memory()
all_new_jobs = []
keywords = memory.get('keywords', ['python', 'ai', 'bot', 'developer', 'engineer'])
golden = memory.get('golden_keywords', [])
blacklisted = memory.get('blacklisted_keywords', []) + memory.get('rejected_keywords', [])

try:
    r1 = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=15)
    for job in r1.json().get('data', []):
        title = job.get('title', '').lower()
        
        if any(bw in title for bw in blacklisted):
            continue 
            
        if any(k in title for k in keywords) and 'remote' in job.get('location', '').lower():
            if job.get('url') not in memory['seen_urls']:
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
    
    msg = f"💰 <b>شکار خودکار امروز:</b>\n"
    msg += f"💎 <b>{job['title']}</b> (امتیاز: {job['score']})\n"
    msg += f"🏢 {job['company']}\n"
    msg += f"🔗 <a href='{job['url']}'>مشاهده</a>\n\n"
    
    if job['score'] >= 100:
        pitch = generate_smart_pitch(job['title'], job['company'], golden)
        msg += f"🎨 <b>پیشنهاد اختصاصی (اولویت بالا):</b>\n<i>{pitch}</i>\n\n"
        msg += "🧬 <b>هشدار DNA:</b> این پروژه دارای الگوهای طلایی است!\n"
        
    send_message(msg)
    for j in all_new_jobs:
        memory['seen_urls'].append(j['url'])
    memory['total_seen'] = memory.get('total_seen', 0) + len(all_new_jobs)
    save_memory(memory)
else:
    send_message("⏸️ پروژه جدیدی نیست. سیستم در حال اسکن مداوم است.")
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
        blacklisted = memory.get('blacklisted_keywords', []) + memory.get('rejected_keywords', [])
        
        if golden:
            report += f"\n🧬 <b>الگوهای طلایی (DNA مثبت):</b>\n"
            report += "، ".join(golden) + "\n"
        if blacklisted:
            report += f"\n🛡️ <b>لیست سیاه (DNA منفی):</b>\n"
            report += "، ".join(list(set(blacklisted))) + "\n"
            
        if not golden and not blacklisted:
            report += "\n💡 <b>بینش:</b> هنوز الگویی آموخته نشده. با /hired یا /rejected به سیستم یاد بده.\n"
            
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
            requests.post(api_url, files={'document': f}, data={'chat_id': CHAT_ID, 'caption': '📊 <b>گزارش اکسل درخواست‌ها</b>'})
        sys.exit()
    
    elif command.startswith('/interview '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'interview'
                memory['applications'] = apps
                
                title = apps[num]['title'].lower()
                tech_words = ['python', 'ai', 'react', 'node', 'aws', 'docker', 'crypto', 'web3', 'bot', 'api', 'data', 'ml', 'llm', 'gpt', 'rust', 'go', 'java', 'telegram']
                learned = [tw for tw in tech_words if tw in title and tw not in memory.get('golden_keywords', [])]
                if learned:
                    memory.setdefault('golden_keywords', []).extend(learned)
                save_memory(memory)
                
                msg = f"🎤 عالی! وضعیت به‌روز شد: {apps[num]['title']}\n"
                if learned:
                    msg += f"\n🧬 <b>سیستم یاد گرفت!</b> DNA مثبت: {', '.join(learned)}"
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
                
                title = apps[num]['title'].lower()
                tech_words = ['python', 'ai', 'react', 'node', 'aws', 'docker', 'crypto', 'web3', 'bot', 'api', 'data', 'ml', 'llm', 'gpt', 'rust', 'go', 'java', 'telegram']
                learned = [tw for tw in tech_words if tw in title and tw not in memory.get('golden_keywords', [])]
                if learned:
                    memory.setdefault('golden_keywords', []).extend(learned)
                save_memory(memory)
                
                msg = f"🎉🔥 تبریک رهبر! استخدام شدی: {apps[num]['title']}\n"
                import requests
import json
import os
import sys
from datetime import datetime
import random

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
        'golden_keywords': [],
        'blacklisted_keywords': []
    }

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def send_message(text):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api_url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'})

def generate_smart_pitch(title, company, golden):
    # 🎨 موتور طراحی مولد: ساخت پیشنهاد اختصاصی بر اساس DNA سیستم
    tech_stack = ", ".join(golden[:3]) if golden else "تکنولوژی‌های پیشرفته و مقیاس‌پذیر"
    
    pitches = [
        f"تیم محترم {company}،\n\nبا سلام و احترام،\nمن با اشتیاق فراوان آگهی شما برای موقعیت '{title}' را مطالعه کردم. با توجه به تخصص عمیق من در {tech_stack} و سابقه‌ی موفق در پیاده‌سازی راه‌حل‌های کارآمد، اطمینان دارم که می‌توانم از روز اول ارزش‌افزوده‌ی ملموسی برای تیم شما ایجاد کنم.\n\nآمادگی دارم تا در یک جلسه‌ی کوتاه، ایده‌هایم را برای بهینه‌سازی فرآیندهای شما ارائه دهم.\n\nبا سپاس از زمان و توجه شما.",
        f"سلام تیم {company}،\n\nآگهی استخدام '{title}' توجه من را جلب کرد. تجربه‌ی عملی من در کار با {tech_stack} دقیقاً با نیازهای پروژه‌ی شما همخوانی دارد. من به ساخت کدهای تمیز، بهینه و قابل نگهداری متعهد هستم و مشتاقم که مهارت‌هایم را در خدمت اهداف نوآورانه‌ی شما قرار دهم.\n\nخوشحال می‌شوم فرصتی برای گفتگو و بررسی جزئیات فنی داشته باشیم.\n\nارادتمند،\nتیم توسعه کاویان"
    ]
    return random.choice(pitches)

if len(sys.argv) > 1:
    command = sys.argv[1]
    memory = load_memory()
    apps = memory.get('applications', [])
    
    if command == '/start':
        msg = "🦁 <b>سلام رهبر کاویان!</b>\nمن KAVIAN GENESIS هستم.\n\n"
        msg += "🔍 <b>شکار و مدیریت:</b>\n"
        msg += "/find [عبارت] : جستجو، ثبت و <b>طراحی پیشنهاد</b>\n"
        msg += "/track : لیست درخواست‌ها\n"
        msg += "/stats : 🧠 تحلیل هوشمند و DNA\n"
        msg += "/export : دانلود فایل اکسل\n\n"
        msg += "⚙️ <b>مدیریت وضعیت:</b>\n"
        msg += "/interview [شماره] : مصاحبه (یادگیری مثبت)\n"
        msg += "/hired [شماره] : استخدام (یادگیری مثبت)\n"
        msg += "/rejected [شماره] : رد شد (یادگیری منفی)"
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
