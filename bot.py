import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import requests as req
import speech_recognition as sr
# تنظیم لاگ‌ها
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
from keep_alive import keep_alive

keep_alive()

# دستور شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام، به ربات لرنیتکس امدید 🌟\n"
        "(طراح:امیرمحمد)\n"
        "لطفاً سوال یا متن خود را ارسال کنید تا پاسخ آن را برایتان بنویسم. 📝"
    )

# عملکرد دریافت پیام و پاسخ متنی از سرور
async def make_text_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    print("متن دریافتی از کاربر:", user_text)

    try:
        response = req.get(f"http://5.161.91.18/chat?text={user_text}", timeout=10)
        print("وضعیت پاسخ:", response.status_code)

        if response.status_code == 200:
            try:
                result = response.json()
                print("پاسخ JSON دریافتی:", result)

                # بررسی وجود کلیدهای مورد نظر
                if "answer" in result:
                    reply_text = result["answer"]
                elif "text" in result:
                    reply_text = result["text"]
                else:
                    reply_text = str(result)

                await update.message.reply_text(f"✅ پاسخ:\n{reply_text}")

            except Exception as e:
                print("❌ خطا در تجزیه JSON:", e)
                await update.message.reply_text("❌ خطا در پردازش پاسخ JSON.")
        else:
            print("❌ کد وضعیت نامعتبر:", response.status_code)
            await update.message.reply_text("❌ پاسخ نامعتبر از سرور دریافت شد.")
    except Exception as e:
        print("❌ خطا در اتصال به سرور:", e)
        await update.message.reply_text("❌ خطا در ارتباط با سرور. لطفاً بعداً دوباره تلاش کنید.")

# راه‌اندازی ربات
application = ApplicationBuilder().token('8136031342:AAFEs9nQyEqRByLTF3v7pxqvd0btI-ELSUU').build()
application.add_handler(CommandHandler('start', start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, make_text_response))
application.run_polling()
