```python
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", "10000"))
URL = os.environ["RENDER_EXTERNAL_URL"]

GRUPO = "@textudoofertas"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Bot de Ofertas ativado!\n\n"
        "Envie o link de um produto para começar."
    )

async def receber_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text

    mensagem = (
        "🔥 OFERTA ENCONTRADA! 🔥\n\n"
        "🛍️ Confira o produto:\n\n"
        f"🔗 {link}\n\n"
        "👉 Aproveite enquanto estiver disponível!"
    )

    await context.bot.send_message(
        chat_id=GRUPO,
        text=mensagem
    )

    await update.message.reply_text(
        "✅ Oferta publicada no grupo!"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_link))

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"{URL}/{TOKEN}"
)
```
