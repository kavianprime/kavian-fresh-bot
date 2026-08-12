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
    return {'seen_urls': [], 'total_seen': 0}

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

def send_message(text, parse_mode='HTML'):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={'chat_id': CHAT_ID, 'text': text, 'parse_mode': parse_mode})

# بررسی دستورات
if len(sys.argv) > 1:
    command = sys.argv[1]
    if command == '/start':
        send_message("🦁 <b>سلام رهبر کاویان!</b>\nمن KAVIAN PRIME هستم.\n\nدستورات:\n/status : گزارش وضعیت\n/find : جستجوی فوری (به زودی)")
        sys.exit()
    elif command == '/status':
        memory = load_memory()
        msg = f"📊 <b>گزارش وضعیت KAVIAN NEXUS:</b>\n\n"
        msg += f"🧠 کل پروژه‌های بررسی شده: {memory.get('total_seen', 0)}\n"
        msg += f"💾 حافظه: {len(memory.get('seen_urls', []))} لینک منحصر‌به‌فرد\n"
        msg += f"⚡ وضعیت: <b>کاملاً پایدار و آنلاین ✅</b>"
        send_message(msg)
        sys.exit()

# حالت شکار روزانه
print("🦁 شکارچی هوشمند با مغز نویسنده بیدار شد!")
memory = load_memory()

url = "https://www.arbeitnow.com/api/job-board-api"
headers = {'User-Agent': 'KavianPrimeBot/3.0'}

try:
    response = requests.get(url, headers=headers, timeout=15)
    data = response.json().get('data', [])
    
    new_jobs = []
    for job in data:
        title = job.get('title', '').lower()
        job_url = job.get('url', '')
        if ('python' in title or 'ai' in title or 'bot' in title or 'developer' in title) and 'remote' in job.get('location', '').lower():
            if job_url not in memory['seen_urls']:
                
                # 🧠 الگوریتم امتیازدهی هوشمند
                score = 70
                if 'senior' in title or 'lead' in title: score += 15
                if 'ai' in title or 'machine learning' in title: score += 10
                if 'api' in title: score += 5
                
                new_jobs.append({
                    'title': job.get('title'), 
                    'company': job.get('company_name', 'Unknown'), 
                    'url': job_url,
                    'score': min(score, 99)
                })

    if new_jobs:
        new_jobs.sort(key=lambda x: x['score'], reverse=True)
        
        msg = "💰 <b>شکارهای هوشمند امروز:</b>\n\n"
        for i, job in enumerate(new_jobs[:3], 1): 
            emoji = "🔥" if job['score'] >= 90 else "⭐" if job['score'] >= 80 else "✅"
            msg += f"{i}. {emoji} <b>{job['title']}</b> (امتیاز: {job['score']}٪)\n"
            msg += f"   🏢 {job['company']}\n"
            msg += f"   🔗 <a href='{job['url']}'>مشاهده لینک</a>\n\n"
            
            # ✨ ویژگی روز نهم: تولید خودکار متن پیشنهاد برای بهترین گزینه
            if i == 1 and job['score'] >= 80:
                msg += f"📝 <b>پیشنهاد آماده‌ی ارسال برای این پروژه:</b>\n"
                msg += f"<i>سلام تیم {job['company']},\nمن توسعه‌دهنده‌ی متخصص در زمینه‌ی {job['title']} هستم. با توجه به نیازهای پروژه‌ی شما، آمادگی دارم راه‌حلی بهینه، مقیاس‌پذیر و با کیفیت بالا ارائه دهم. خوشحال می‌شوم در مورد جزئیات بیشتر گفتگو کنیم.</i>\n\n"
                msg += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        send_message(msg)
        print(f"✅ {len(new_jobs)} پروژه جدید با پیشنهاد آماده ارسال شد.")
        
        for job in new_jobs:
            memory['seen_urls'].append(job['url'])
        memory['total_seen'] = memory.get('total_seen', 0) + len(new_jobs)
        save_memory(memory)
    else:
        print("⏸️ پروژه جدیدی یافت نشد.")
        send_message("🧠 <b>گزارش روزانه:</b>\nامروز شکار جدیدی با معیارهای بالا یافت نشد. ربات در حال اسکن مداوم است. ✅")
        except Exception as e:
    print(f"❌ خطا: {e}")
    send_message(f"⚠️ <b>هشدار سیستم:</b>\nخطایی در اسکن رخ داد: {str(e)}")
