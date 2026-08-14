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
        'golden_keywords': [],
        'blacklisted_keywords': []
    }

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def send_message(text):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api_url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'})

def generate_pitch(title, company, golden):
    tech = ", ".join(golden[:3]) if golden else "تکنولوژی‌های پیشرفته"
    pitch = f"تیم محترم {company}،\n\nبا سلام،\nآگهی '{title}' توجه من را جلب کرد. تخصص من در {tech} دقیقاً با نیازهای شما همخوانی دارد. آمادگی دارم در جلسه‌ای کوتاه، ایده‌هایم را ارائه دهم.\n\nبا سپاس."
    return pitch

if len(sys.argv) > 1:
    command = sys.argv[1]
    memory = load_memory()
    apps = memory.get('applications', [])
    
    if command == '/start':
        msg = "🦁 <b>سلام رهبر کاویان!</b>\nدستورات:\n/find [عبارت]\n/track\n/stats\n/export\n/interview [شماره]\n/hired [شماره]\n/rejected [شماره]"
        send_message(msg)
        sys.exit()
    
    elif command == '/track':
        if not apps:
            send_message("📋 لیست خالی است.")
            sys.exit()
        report = "📋 <b>درخواست‌ها:</b>\n"
        for i, app in enumerate(apps[-10:], 1):
            report += f"{i}. {app['title']} - {app['status']}\n"
        send_message(report)
        sys.exit()
    
    elif command == '/stats':
        if not apps:
            send_message("📊 داده‌ای نیست.")
            sys.exit()
        total = len(apps)
        applied = len([a for a in apps if a['status'] == 'applied'])
        interview = len([a for a in apps if a['status'] == 'interview'])
        rejected = len([a for a in apps if a['status'] == 'rejected'])
        hired = len([a for a in apps if a['status'] == 'hired'])
        success = interview + hired
        rate = round((success / total) * 100, 1) if total > 0 else 0
        
        report = f"🧠 <b>داشبورد KAVIAN GENESIS</b>\n"
        report += f"🎯 کل: {total}\n📤 ارسال: {applied}\n🎤 مصاحبه: {interview}\n❌ رد: {rejected}\n🎉 استخدام: {hired}\n📈 نرخ موفقیت: {rate}٪\n"
        
        golden = memory.get('golden_keywords', [])
        blacklisted = memory.get('blacklisted_keywords', [])
        if golden:
            report += f"\n🧬 DNA مثبت: {', '.join(golden)}\n"
        if blacklisted:
            report += f"\n🛡️ DNA منفی: {', '.join(blacklisted)}\n"
        send_message(report)
        sys.exit()
    
    elif command == '/export':
        if not apps:
            send_message("📋 لیست خالی است.")
            sys.exit()
        csv = "Title,Company,Date,Status,URL\n"
        for app in apps:
            csv += f'"{app["title"]}","{app["company"]}","{app["date"]}","{app["status"]}","{app["url"]}"\n'
        with open('apps.csv', 'w', encoding='utf-8') as f:
            f.write(csv)
        api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open('apps.csv', 'rb') as f:
            requests.post(api_url, files={'document': f}, data={'chat_id': CHAT_ID})
        sys.exit()
    
    elif command.startswith('/interview '):
        try:
            num = int(command.split(' ')[1]) - 1
          if 0 <= num < len(apps):
                apps[num]['status'] = 'interview'
                memory['applications'] = apps
                title = apps[num]['title'].lower()
                tech = ['python', 'ai', 'react', 'node', 'aws', 'docker', 'crypto', 'web3', 'bot', 'api', 'data', 'ml', 'llm', 'gpt', 'rust', 'go', 'java']
                learned = [t for t in tech if t in title and t not in memory.get('golden_keywords', [])]
                if learned:
                    memory.setdefault('golden_keywords', []).extend(learned)
                save_memory(memory)
                msg = f"🎤 {apps[num]['title']}\n"
                if learned:
                    msg += f"\n🧬 DNA مثبت: {', '.join(learned)}"
                send_message(msg)
        except:
            send_message("⚠️ /interview 1")
        sys.exit()
    
    elif command.startswith('/hired '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'hired'
                memory['applications'] = apps
                title = apps[num]['title'].lower()
                tech = ['python', 'ai', 'react', 'node', 'aws', 'docker', 'crypto', 'web3', 'bot', 'api', 'data', 'ml', 'llm', 'gpt', 'rust', 'go', 'java']
                learned = [t for t in tech if t in title and t not in memory.get('golden_keywords', [])]
                if learned:
                    memory.setdefault('golden_keywords', []).extend(learned)
                save_memory(memory)
                msg = f"🎉 {apps[num]['title']}\n"
                if learned:
                    msg += f"\n🧬 DNA مثبت: {', '.join(learned)}"
                send_message(msg)
        except:
            send_message("⚠️ /hired 1")
        sys.exit()
    
    elif command.startswith('/rejected '):
        try:
            num = int(command.split(' ')[1]) - 1
            if 0 <= num < len(apps):
                apps[num]['status'] = 'rejected'
                memory['applications'] = apps
                title = apps[num]['title'].lower()
                bad = ['intern', 'junior', 'unpaid', 'volunteer', 'commission', 'trainee', 'entry-level', 'part-time']
                learned_bad = [b for b in bad if b in title and b not in memory.get('blacklisted_keywords', [])]
                if learned_bad:
                    memory.setdefault('blacklisted_keywords', []).extend(learned_bad)
                save_memory(memory)
                msg = f"❌ {apps[num]['title']}\n"
                if learned_bad:
                    msg += f"\n🛡️ DNA منفی: {', '.join(learned_bad)}"
                send_message(msg)
        except:
            send_message("⚠️ /rejected 1")
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
            pitch = generate_pitch(job['title'], job['company'], golden)
          report = f"💎 <b>{job['title']}</b>\n🏢 {job['company']}\n🔗 <a href='{job['url']}'>مشاهده</a>\n\n"
            report += f"🎨 <b>پیشنهاد آماده:</b>\n<i>{pitch}</i>\n\n"
            report += "✅ به لیست اضافه شد."
            send_message(report)
        else:
            send_message("❌ یافت نشد.")
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
                if 'senior' in title or 'lead' in title:
                    score += 15
                all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url'), 'score': score})
except:
    pass

if len(all_new_jobs) > 0:
    all_new_jobs.sort(key=lambda x: x['score'], reverse=True)
    job = all_new_jobs[0]
    msg = f"💰 <b>شکار امروز:</b>\n💎 <b>{job['title']}</b> (امتیاز: {job['score']})\n🏢 {job['company']}\n🔗 <a href='{job['url']}'>مشاهده</a>\n"
    if job['score'] >= 100:
        pitch = generate_pitch(job['title'], job['company'], golden)
        msg += f"\n🎨 <b>پیشنهاد:</b>\n<i>{pitch}</i>\n\n🧬 <b>هشدار DNA:</b> الگوهای طلایی!"
    send_message(msg)
    for j in all_new_jobs:
        memory['seen_urls'].append(j['url'])
    memory['total_seen'] = memory.get('total_seen', 0) + len(all_new_jobs)
    save_memory(memory)
else:
    send_message("⏸️ پروژه جدیدی نیست.")
