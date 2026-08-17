import os
import json
import requests
import threading
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8811972038:AAEupegBge-WDbG-D8G9nodoz1E8Nj7MYN0"
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🦁 <b>سلام رهبر کاویان!</b>\nمن KAVIAN GENESIS هستم.\n\n"
    msg += "🔍 <b>دستورات:</b>\n"
    msg += "/find [عبارت] : جستجو و ثبت پروژه\n"
    msg += "/track : لیست درخواست‌ها\n"
    msg += "/stats : 🧠 تحلیل هوشمند\n"
    msg += "/learn [موضوع] : 🌐 یادگیری از ویکی‌پدیا\n"
    msg += "/search [موضوع] : 🔎 بازیابی از حافظه\n"
    msg += "/export : دانلود فایل اکسل\n\n"
    msg += "⚙️ <b>مدیریت وضعیت:</b>\n"
    msg += "/interview [شماره]\n/hired [شماره]\n/rejected [شماره]"
    await update.message.reply_text(msg, parse_mode='HTML')

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memory = load_memory()
    apps = memory.get('applications', [])
    if not apps:
        await update.message.reply_text("📋 لیست خالی است.")
        return
    report = "📋 <b>درخواست‌ها:</b>\n"
    for i, app in enumerate(apps[-10:], 1):
        report += f"{i}. {app['title']} - {app['status']}\n"
    await update.message.reply_text(report, parse_mode='HTML')

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memory = load_memory()
    apps = memory.get('applications', [])
    if not apps and not memory.get('knowledge_base'):
        await update.message.reply_text("📊 هنوز داده‌ای نیست.")
        return
    
    total = len(apps)
    hired = len([a for a in apps if a['status'] == 'hired'])
    rate = round((hired / total) * 100, 1) if total > 0 else 0
    
    report = f"🧠 <b>داشبورد KAVIAN GENESIS</b>\n"
    report += f"🎯 کل: {total} | 🎉 استخدام: {hired} | 📈 نرخ: {rate}٪\n"
    
    kb = memory.get('knowledge_base', [])
    if kb:
        report += f"\n📚 <b>دانش:</b> {len(kb)} موضوع"
    
    golden = memory.get('golden_keywords', [])
    blacklisted = memory.get('blacklisted_keywords', [])
    if golden: report += f"\n🧬 DNA مثبت: {', '.join(golden)}"
    if blacklisted: report += f"\n🛡️ DNA منفی: {', '.join(blacklisted)}"
    
    await update.message.reply_text(report, parse_mode='HTML')

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ فرمت: /learn [موضوع]")
        return
    
    topic = ' '.join(context.args)
    await update.message.reply_text(f"⏳ در حال یادگیری '{topic}'...")
    
    try:
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={topic}&format=json&srlimit=1"
        response = requests.get(search_url, timeout=10)
        results = response.json().get('query', {}).get('search', [])
        
        if not results:
            await update.message.reply_text(f"❌ '{topic}' پیدا نشد.")
            return
        
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
        
        msg = f"🧠 <b>یادگیری موفق!</b>\n\n📚 <b>{title}</b>\n💡 <i>{summary[:400]}...</i>\n\n✅ ذخیره شد."
        await update.message.reply_text(msg, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"⚠️ خطا: {str(e)}")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ فرمت: /search [موضوع]")
        return
    
    query = ' '.join(context.args).lower()
    memory = load_memory()
    kb = memory.get('knowledge_base', [])
    
    if not kb:
        await update.message.reply_text("📚 حافظه خالی است. اول /learn بزن!")
        return
    
    found_items = []
    for item in kb:
        if query in item['topic'].lower() or query in item['title'].lower() or query in item['summary'].lower():
            found_items.append(item)
    
    if not found_items:
        await update.message.reply_text(f"🔍 چیزی درباره‌ی '{query}' پیدا نکردم.")
        return
    
    report = f"🧠 <b>یافته‌ها درباره‌ی '{query}':</b>\n\n"
    for i, item in enumerate(found_items[:3], 1):
        report += f"{i}. <b>{item['title']}</b>\n<i>{item['summary']}</i>\n\n"
    
    await update.message.reply_text(report, parse_mode='HTML')

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ فرمت: /find [عبارت]")
        return
    
    query = ' '.join(context.args).lower()
    search_terms = query.split()
    memory = load_memory()
    apps = memory.get('applications', [])
    
    try:
        r1 = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=15)
        all_new_jobs = []
        for job in r1.json().get('data', []):
            title = job.get('title', '').lower()
            if any(k in title for k in search_terms) and 'remote' in job.get('location', '').lower():
                all_new_jobs.append({'title': job.get('title'), 'company': job.get('company_name'), 'url': job.get('url')})
    except:
        await update.message.reply_text("⚠️ خطا در جستجو.")
        return
    
    if len(all_new_jobs) > 0:
        job = all_new_jobs[0]
        today = datetime.now().strftime("%Y-%m-%d")
        apps.append({'title': job['title'], 'company': job['company'], 'url': job['url'], 'date': today, 'status': 'applied'})
        memory['applications'] = apps
        save_memory(memory)
        msg = f"💎 <b>{job['title']}</b>\n🏢 {job['company']}\n🔗 <a href='{job['url']}'>مشاهده</a>\n✅ اضافه شد."
        await update.message.reply_text(msg, parse_mode='HTML')
    else:
        await update.message.reply_text("❌ یافت نشد.")

# ==========================================
# 🦁 ترفند حرفه‌ای: سرور نمایشی برای راضی کردن Render
# ==========================================
def run_dummy_server():
    app = Flask(name)
    
    @app.route('/')
    def home():
        return "🦁 KAVIAN GENESIS is alive and running!"
    
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def main():
    # ۱. اجرای سرور نمایشی در پس‌زمینه (برای جلوگیری از خطای پورت رندر)
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    # ۲. اجرای ربات تلگرام
    app_bot = Application.builder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("track", track))
    app_bot.add_handler(CommandHandler("stats", stats))
    app_bot.add_handler(CommandHandler("learn", learn))
    app_bot.add_handler(CommandHandler("search", search))
    app_bot.add_handler(CommandHandler("find", find))
    
    print("🦁 KAVIAN GENESIS: ربات 24/7 فعال شد!")
    app_bot.run_polling()

if name == 'main':
    main()
