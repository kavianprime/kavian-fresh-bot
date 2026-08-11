import requests
import json
import os

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
    return {'seen_urls': []}

def save_memory(memory):
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

print("🦁 شکارچی هوشمند بیدار شد!")

memory = load_memory()

url = "https://www.arbeitnow.com/api/job-board-api"
headers = {'User-Agent': 'KavianPrimeBot/1.0'}

try:
    response = requests.get(url, headers=headers, timeout=15)
    data = response.json().get('data', [])
    
    new_jobs = []
    for job in data:
        title = job.get('title', '').lower()
        job_url = job.get('url', '')
        if ('python' in title or 'ai' in title or 'bot' in title) and 'remote' in job.get('location', '').lower():
            if job_url not in memory['seen_urls']:
                new_jobs.append({'title': job.get('title'), 'company': job.get('company_name', 'Unknown'), 'url': job_url})

    if new_jobs:
        msg = "💰 <b>پروژه‌های جدید:</b>\n\n"
        for i, job in enumerate(new_jobs[:3], 1):
            msg += f"{i}. <b>{job['title']}</b>\n   🏢 {job['company']}\n   🔗 <a href='{job['url']}'>لینک</a>\n\n"
        
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'HTML'})
        
        for job in new_jobs:
            memory['seen_urls'].append(job['url'])
        save_memory(memory)
        print("✅ گزارش ارسال و ذخیره شد.")
    else:
        print("⏸️ پروژه جدیدی نیست.")

except Exception as e:
    print(f"❌ خطا: {e}")
