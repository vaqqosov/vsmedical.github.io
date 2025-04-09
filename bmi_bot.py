
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

ASK_HEIGHT, ASK_WEIGHT = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Bo'yingizni kiriting (sm):")
    return ASK_HEIGHT

async def get_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['height'] = float(update.message.text)
        await update.message.reply_text("Endi vazningizni kiriting (kg):")
        return ASK_WEIGHT
    except:
        await update.message.reply_text("Iltimos, to‘g‘ri son kiriting.")
        return ASK_HEIGHT

async def get_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        weight = float(update.message.text)
        height = context.user_data['height']
        bmi = weight / ((height / 100) ** 2)

        if bmi < 18.5:
            category = "Kam vazn"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Ortiqcha vazn"
        else:
            category = "Semizlik"

        await update.message.reply_text(f"Sizning BMI: {bmi:.2f} — {category}")
        return ConversationHandler.END
    except:
        await update.message.reply_text("Raqam kiriting.")
        return ASK_WEIGHT

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bekor qilindi.")
    return ConversationHandler.END

async def main():
    app = ApplicationBuilder().token("8067556005:AAERU4NwYwTtzj4SrZz7s389JfQr-Qd41ZY").build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_height)],
            ASK_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_weight)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv)
    print("Bot ishga tushdi!")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
