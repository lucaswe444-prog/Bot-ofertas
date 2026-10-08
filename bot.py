import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Bot de Ofertas ativado!\n\n"
        "Envie o link de um produto para começar."
    )

async def receber_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text

    await update.message.reply_text(
        "🔎 Recebi o produto!\n\n"
        f"🔗 {texto}\n\n"
        "Em breve vou analisar o produto e montar a oferta. 🚀"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_link))

app.run_polling()
