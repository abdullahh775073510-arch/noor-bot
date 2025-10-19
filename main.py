from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

BOT_TOKEN = "8108421327:AAGc-BPMvKSRYtOj4iKEP4Xg4W2EHDsE9go"

questions = [
"هل صليت الصلوات الخمس اليوم؟",
"هل ذكرت أذكار الصباح؟",
"هل ذكرت أذكار المساء؟",
"هل صليت الضحى؟",
"هل صليت نوافل؟",
"هل قمت الليل؟",
"هل قرأت وردك من القرآن؟"
]

user_data = {}

async def start_evaluation(update: Update, context: ContextTypes.DEFAULT_TYPE):
user_data.clear()
await update.message.reply_text("📋 نبدأ تقييم يومك مع الله 💜")
await send_question(update, context, 0, update.effective_chat.id)

async def send_question(update, context, index, chat_id, user_id=None):
if index < len(questions):
q = questions[index]
keyboard = [
[InlineKeyboardButton("✅ نعم", callback_data=f"yes_{index}"),
InlineKeyboardButton("❌ لا", callback_data=f"no_{index}")]
]
reply_markup = InlineKeyboardMarkup(keyboard)
await context.bot.send_message(chat_id=chat_id, text=f"{q}", reply_markup=reply_markup)
else:
await send_result(context, chat_id, user_id)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()
user = query.from_user
chat_id = query.message.chat.id

choice, index = query.data.split("_")  
index = int(index)  

if user.id not in user_data:  
    user_data[user.id] = {"score": 0, "current": 0}  

if choice == "yes":  
    user_data[user.id]["score"] += 1  

user_data[user.id]["current"] = index + 1  

if user_data[user.id]["current"] < len(questions):  
    await send_question(update, context, user_data[user.id]["current"], chat_id, user.id)  
else:  
    await send_result(context, chat_id, user.id)

async def send_result(context, chat_id, user_id):
score = user_data[user_id]["score"]
if score >= 6:
result = "🌟 ممتاز"
elif score >= 3:
result = "😊 وسط"
else:
result = "😔 قصّرت"

await context.bot.send_message(chat_id=chat_id, text=f"نتيجتك اليوم: {result}\nعدد النقاط: {score}/7")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("ابدأ_التقييم", start_evaluation))
app.add_handler(CallbackQueryHandler(handle_answer))

print("✅ البوت يعمل الآن...")
app.run_polling()

