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

def send_message_with_button(text, url, parse_mode='HTML'):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    keyboard = {"inline_keyboard": [[{"text": "🔗 مشاهده و اقدام سریع", "url": url}]]}
    payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': parse_mode, 'reply_markup': json.dumps(keyboard)}
    requests.post(api_url, json=payload)

def send_message(text, parse_mode='HTML'):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(api_url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': parse_mode})

if len(sys.argv) > 1:
    command = sys.argv[1]
    memory = load_memory()
    keywords = memory.get('keywords', ['python', 'ai', 'bot', 'developer', 'engineer'])
    rejected = memory.get('rejected_keywords', ['intern', 'junior'])
    
    if command == '/start':
        msg = "🦁 <b>سلام رهبر کاویان!</b>\nمن KAVIAN PRIME هستم.\n\n"
        msg += "دستورات:\n"
        msg += "/status : گزارش وضعیت\n"
        msg += "/keywords : کلمات کلیدی فعال\n"
        msg += "/add [کلمه] : افزودن به شکار\n"
        msg += "/reject [کلمه] : افزودن به لیست سیاه\n"
        msg += "/remove [کلمه] : حذف از لیست سیاه\n"
        msg += "/find [عبارت] : جستجوی فوری"
        send_message(msg)
        sys.exit()
    
    elif command == '/status':
        msg = "📊 <b>گزارش وضعیت:</b>\n\n"
        msg += f"🧠 کل پروژه‌ها: {memory.get('total_seen', 0)}\n"
        msg += f"💾 حافظه: {len(memory.get('seen_urls', []))} لینک\n"
        msg += f"⚡ وضعیت: <b>آنلاین ✅</b>"
        send_message(msg)
        sys.exit()
    
    elif command == '/keywords':
        send_message("🔑 <b>کلمات کلیدی فعال:</b>\n\n" + "، ".join(keywords))
        sys.exit()
    
    elif command.startswith('/add '):
        new_kw = command.split(' ', 1)[1].strip().lower()
        if new_kw and new_kw not in keywords:
            keywords.append(new_kw)
            memory['keywords'] = keywords
            save_memory(memory)
            send_message(f"✅ کلمه‌ی <b>{new_kw}</b> اضافه شد!")
        else:
            send_message("⚠️ این کلمه از قبل وجود دارد.")
        sys.exit()

    elif command.startswith('/reject '):
        bad_kw = command.split(' ', 1)[1].strip().lower()
        if bad_kw and bad_kw not in rejected:
            rejected.append(bad_kw)
            memory['rejected_keywords'] = rejected
            save_memory(memory)
            send_message(f"🚫 کلمه‌ی <b>{bad_kw}</b> به لیست سیاه اضافه شد!")
        else:
            send_message("⚠️ این کلمه از قبل در لیست سیاه است.")
        sys.exit()

    elif command.startswith('/remove '):
        rem_kw = command.split(' ', 1)[1].strip().lower()
        if rem_kw in rejected:
            rejected.remove(rem_kw)
            memory['rejected_keywords'] = rejected
            save_memory(memory)
            send_message(f"✅ کلمه‌ی <b>{rem_kw}</b> از لیست سیاه حذف شد.")
        else:
            send_message("⚠️ این کلمه در لیست سیاه نبود.")
        sys.exit()

    elif command.startswith('/find '):
        query = command.split(' ', 1)[1].strip().lower()
        search_terms = query.split()
        print(f"🔍 جستجوی فوری برای: {query}")
        all_new_jobs = []
        try:
            response1 = requests.get("https://www.arbeitnow.com/api/job-board-api", headers={'User-Agent': 'KavianPrimeBot/9.0'}, timeout=15)
            data1 = response1.json().get('data', [])
            for job in data1:
                title = job.get('title', '').lower()
                job_url = job.get('url', '')
                if any(k in title for k in search_terms) and 'remote' in job.get('location', '').lower():
                    if not any(bad in title for bad in rejected):
                        score = 70
                        if 'senior' in title or 'lead' in title: score += 15
                        if 'ai' in title or 'machine learning' in title: score += 10
                        all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name', 'Unknown'), 'url': job_url, 'score': min(score, 99), 'perks': ''})
        except Exception as e:
            print(f"⚠️ خطا در منبع اول: {e}")
        try:
            response2 = requests.get("https://remotive.com/api/remote-jobs", headers={'User-Agent': 'KavianPrimeBot/9.0'}, timeout=15)
            data2 = response2.json().get('jobs', [])
            for job in data2:
                title = job.get('title', '').lower()
                job_url = job.get('url', '')
                if any(k in title for k in search_terms):
                    if not any(bad in title for bad in rejected):
                        score = 70
                        if 'senior' in title or 'lead' in title: score += 15
                        if 'ai' in title or 'machine learning' in title: score += 10
                        salary = job.get('salary', '')
                        perks = f"💰 {salary}" if salary else "💼 دورکاری"
                        all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name', 'Unknown'), 'url': job_url, 'score': min(score, 99), 'perks': perks})
        except Exception as e:
            print(f"⚠️ خطا در منبع دوم: {e}")
        
        if len(all_new_jobs) > 0:
            all_new_jobs.sort(key=lambda x: x['score'], reverse=True)
            send_message("🔍 <b>نتایج جستجوی فوری:</b>\n\n")
            for i, job in enumerate(all_new_jobs[:4], 1):
                emoji = "🚨" if job['score'] >= 90 else "🔥" if job['score'] >= 80 else "✅"
                msg = f"{i}. {emoji} <b>{job['title']}</b> (امتیاز: {job['score']}٪)\n"
                msg += f"   🏢 {job['company']}\n"
                perks_text = job.get('perks', '')
                if perks_text != '':
                    msg += f"   🎁 {perks_text}\n"
                send_message_with_button(msg, job['url'])
            print(f"✅ {len(all_new_jobs[:4])} پروژه ارسال شد.")
        else:
            send_message("🧠 <b>گزارش:</b>\nموردی با این مشخصات یافت نشد.")
        sys.exit()

print("🦁 شکارچی هوشمند بیدار شد!")
memory = load_memory()
all_new_jobs = []
keywords = memory.get('keywords', ['python', 'ai', 'bot', 'developer', 'engineer'])
rejected = memory.get('rejected_keywords', ['intern', 'junior'])

try:
    print("اسکن منبع اول...")
    response1 = requests.get("https://www.arbeitnow.com/api/job-board-api", headers={'User-Agent': 'KavianPrimeBot/9.0'}, timeout=15)
    data1 = response1.json().get('data', [])
    for job in data1:
        title = job.get('title', '').lower()
        job_url = job.get('url', '')
        if any(k in title for k in keywords) and 'remote' in job.get('location', '').lower():
            if not any(bad in title for bad in rejected):
                if job_url not in memory['seen_urls']:
                    score = 70
                    if 'senior' in title or 'lead' in title: score += 15
                    if 'ai' in title or 'machine learning' in title: score += 10
                    all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name', 'Unknown'), 'url': job_url, 'score': min(score, 99), 'perks': ''})
    print("✅ منبع اول تکمیل شد")
except Exception as e:
    print(f"⚠️ خطا در منبع اول: {e}")
    try:
    print("اسکن منبع دوم...")
    response2 = requests.get("https://remotive.com/api/remote-jobs", headers={'User-Agent': 'KavianPrimeBot/9.0'}, timeout=15)
    data2 = response2.json().get('jobs', [])
    for job in data2:
        title = job.get('title', '').lower()
        job_url = job.get('url', '')
        if any(k in title for k in keywords):
            if not any(bad in title for bad in rejected):
                if job_url not in memory['seen_urls']:
                    score = 70
                    if 'senior' in title or 'lead' in title: score += 15
                    if 'ai' in title or 'machine learning' in title: score += 10
                    salary = job.get('salary', '')
                    perks = f"💰 {salary}" if salary else "💼 دورکاری"
                    all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name', 'Unknown'), 'url': job_url, 'score': min(score, 99), 'perks': perks})
    print("✅ منبع دوم تکمیل شد")
except Exception as e:
    print(f"⚠️ خطا در منبع دوم: {e}")

if len(all_new_jobs) > 0:
    all_new_jobs.sort(key=lambda x: x['score'], reverse=True)
    send_message("💰 <b>شکارهای هوشمند از ۲ جبهه:</b>\n\n")
    for i, job in enumerate(all_new_jobs[:4], 1):
        emoji = "🚨" if job['score'] >= 90 else "🔥" if job['score'] >= 80 else "✅"
        msg = f"{i}. {emoji} <b>{job['title']}</b> (امتیاز: {job['score']}٪)\n"
        msg += f"   🏢 {job['company']}\n"
        perks_text = job.get('perks', '')
        if perks_text != '':
            msg += f"   🎁 {perks_text}\n"
        if i == 1 and job['score'] >= 80:
            msg += f"\n📝 <b>پیشنهاد آماده:</b>\n<i>سلام تیم {job['company']}،\nمن متخصص {job['title']} هستم. آمادگی دارم راه‌حل بهینه ارائه دهم.</i>\n"
            msg += "━━━━━━━━━━━━━━━━━━━━"
        send_message_with_button(msg, job['url'])
    print(f"✅ {len(all_new_jobs[:4])} پروژه ارسال شد.")
    for job in all_new_jobs:
        memory['seen_urls'].append(job['url'])
    memory['total_seen'] = memory.get('total_seen', 0) + len(all_new_jobs)
    save_memory(memory)
else:
    print("⏸️ پروژه جدیدی نیست.")
    send_message("🧠 <b>گزارش:</b>\nامروز شکار جدیدی یافت نشد. ✅")
    print("اسکن خودکار روزانه شروع شد...")
daily_jobs = scan_sources(keywords, rejected, is_manual=False)
format_and_send_jobs(daily_jobs, memory, is_manual=False)
