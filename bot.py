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
        'seen_urls': [], 'total_seen': 0, 
        'keywords': ['python', 'ai', 'bot', 'developer', 'engineer'], 
        'rejected_keywords': ['intern', 'junior'], 
        'applications': [], 
        'golden_keywords': [], 
        'blacklisted_keywords': [],
        'knowledge_base': []
    }

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def send_message(text):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api_url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'})

def learn_from_wikipedia(topic):
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={topic}&format=json&srlimit=1"
        response = requests.get(search_url, timeout=10)
        results = response.json().get('query', {}).get('search', [])
        
        if not results:
            return f"❌ موضوع '{topic}' در ویکی‌پدیا پیدا نشد."
        
        title = results[0]['title']
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        resp_summary = requests.get(summary_url, timeout=10)
        summary = resp_summary.json().get('extract', 'خلاصه‌ای یافت نشد.')
        
        memory = load_memory()
        memory.setdefault('knowledge_base', []).append({
            'topic': topic,
            'title': title,
            'summary': summary[:400] + "..."
        })
        save_memory(memory)
        
        return f"🧠 <b>یادگیری موفق!</b>\n\n📚 <b>موضوع:</b> {title}\n💡 <b>خلاصه:</b>\n<i>{summary[:400]}...</i>\n\n✅ این دانش در حافظه‌ی KAVIAN GENESIS ذخیره شد."
    except Exception as e:
        return f"⚠️ خطا در یادگیری: {str(e)}"

if len(sys.argv) > 1:
    command = sys.argv[1]
    memory = load_memory()
    apps = memory.get('applications', [])
    
    if command == '/start':
        msg = "🦁 <b>سلام رهبر کاویان!</b>\nمن KAVIAN GENESIS هستم.\n\n"
        msg += "🔍 <b>شکار و مدیریت:</b>\n"
        msg += "/find [عبارت] : جستجو و ثبت پروژه\n"
        msg += "/track : لیست درخواست‌ها\n"
        msg += "/stats : 🧠 تحلیل هوشمند و DNA\n"
        msg += "/learn [موضوع] : 🌐 یادگیری از ویکی‌پدیا\n"
        msg += "/search [موضوع] : 🔎 بازیابی از حافظه دانش\n"
        msg += "/export : دانلود فایل اکسل\n\n"
        msg += "⚙️ <b>مدیریت وضعیت:</b>\n"
        msg += "/interview [شماره]\n/hired [شماره]\n/rejected [شماره]"
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
        if not apps and not memory.get('knowledge_base'):
            send_message("📊 هنوز داده‌ای نیست. با /find یا /learn شروع کن!")
            sys.exit()
        
        total = len(apps)
        hired = len([a for a in apps if a['status'] == 'hired'])
        rate = round((hired / total) * 100, 1) if total > 0 else 0
        
        report = f"🧠 <b>داشبورد KAVIAN GENESIS</b>\n"
        report += f"🎯 کل درخواست‌ها: {total} | 🎉 استخدام: {hired} | 📈 نرخ موفقیت: {rate}٪\n"
        
        kb = memory.get('knowledge_base', [])
        if kb:
            report += f"\n📚 <b>دانش ذخیره‌شده:</b> {len(kb)} موضوع یاد گرفته شده."
        
        golden = memory.get('golden_keywords', [])
        blacklisted = memory.get('blacklisted_keywords', [])
        if golden: report += f"\n🧬 DNA مثبت: {', '.join(golden)}"
        if blacklisted: report += f"\n🛡️ DNA منفی: {', '.join(blacklisted)}"
        
        send_message(report)
        sys.exit()
        
    elif command.startswith('/learn '):
        topic = command.split(' ', 1)[1].strip()
        send_message(f"⏳ در حال جستجو و یادگیری درباره‌ی '{topic}' از ویکی‌پدیا...")
        result = learn_from_wikipedia(topic)
        send_message(result)
        sys.exit()

    elif command.startswith('/search '):
        query = command.split(' ', 1)[1].strip().lower()
        kb = memory.get('knowledge_base', [])
        if not kb:
            send_message("📚 حافظه‌ی دانش خالی است. اول با /learn چیزی یاد بگیر!")
            sys.exit()
        
        found_items = []
        for item in kb:
            if query in item['topic'].lower() or query in item['title'].lower() or query in item['summary'].lower():
                found_items.append(item)
                
        if not found_items:
            send_message(f"🔍 چیزی درباره‌ی '{query}' در حافظه‌ام پیدا نکردم. شاید باید آن را با /learn یاد بگیرم.")
            sys.exit()
            
        report = f"🧠 <b>یافته‌های حافظه درباره‌ی '{query}':</b>\n\n"
        for i, item in enumerate(found_items[:3], 1):
            report += f"{i}. <b>{item['title']}</b>\n<i>{item['summary']}</i>\n\n"
            
        if len(found_items) > 3:
            report += f"(... و {len(found_items) - 3} مورد دیگر)"
            
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
                if learned: memory.setdefault('golden_keywords', []).extend(learned)
                save_memory(memory)
                msg = f"🎤 {apps[num]['title']}"
                if learned: msg += f"\n🧬 DNA مثبت: {', '.join(learned)}"
                send_message(msg)
        except: send_message("⚠️ /interview 1")
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
                if learned: memory.setdefault('golden_keywords', []).extend(learned)
                save_memory(memory)
                msg = f"🎉 {apps[num]['title']}"
                if learned: msg += f"\n🧬 DNA مثبت: {', '.join(learned)}"
                send_message(msg)
        except: send_message("⚠️ /hired 1")
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
                if learned_bad: memory.setdefault('blacklisted_keywords', []).extend(learned_bad)
                save_memory(memory)
                msg = f"❌ {apps[num]['title']}"
                if learned_bad: msg += f"\n🛡️ DNA منفی: {', '.join(learned_bad)}"
                send_message(msg)
        except: send_message("⚠️ /rejected 1")
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
            send_message(f"💎 <b>{job['title']}</b>\n🏢 {job['company']}\n🔗 <a href='{job['url']}'>مشاهده</a>\n✅ به لیست اضافه شد.")
        else:
            send_message("❌ یافت نشد.")
        sys.exit()

print("🦁 KAVIAN GENESIS: مرحله ۲۴ - موتور بازیابی دانش فعال شد!")


