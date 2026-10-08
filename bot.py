import os
import re
import random
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]
PORT = int(os.environ.get("PORT", "10000"))
URL = os.environ["RENDER_EXTERNAL_URL"]

GRUPO = "@textudoofertas"

FRASES = [
    "😂 Seu bolso pediu calma, mas você não ouviu!",
    "👀 Olhou, gostou... agora segura a vontade!",
    "😎 Achadinho desses não aparece todo dia!",
    "😂 Não precisava, mas esse preço ajuda a convencer!",
    "🔥 O preço caiu e a vontade de comprar subiu!",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Bot de Ofertas ativado!\n\n"
        "Envie o link de um produto para começar."
    )

async def receber_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text

    try:
        resposta = requests.get(
            link,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=15
        )

        soup = BeautifulSoup(resposta.text, "html.parser")

        titulo = soup.title.string if soup.title else "Produto Shopee"
        titulo = titulo.strip()

        texto = soup.get_text(" ", strip=True)

        precos = re.findall(r'R\$\s?[\d.,]+', texto)

        if len(precos) >= 2:
            preco_antigo = precos[0]
            preco_atual = precos[1]

            mensagem = (
                "🔥 OFERTA ENCONTRADA! 🔥\n\n"
                "🛍️ " + titulo + "\n\n"
                "💰 De: " + preco_antigo + "\n"
                "🔥 Por: " + preco_atual + "\n\n"
                + random.choice(FRASES) + "\n\n"
                "🔗 COMPRAR:\n" + link
            )

        elif len(precos) == 1:
            mensagem = (
                "🛍️ ACHADINHO DO DIA! 🛍️\n\n"
                + titulo + "\n\n"
                "💰 Preço: " + precos[0] + "\n\n"
                + random.choice(FRASES) + "\n\n"
                "🔗 COMPRAR:\n" + link
            )

        else:
            mensagem = (
                "🔥 OFERTA ENCONTRADA! 🔥\n\n"
                "🛍️ " + titulo + "\n\n"
                + random.choice(FRASES) + "\n\n"
                "🔗 COMPRAR:\n" + link
            )

    except Exception:
        mensagem = (
            "🔥 OFERTA ENCONTRADA! 🔥\n\n"
            "🛍️ Confira o produto!\n\n"
            + random.choice(FRASES) + "\n\n"
            "🔗 COMPRAR:\n" + link
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
    webhook_url=URL + "/" + TOKEN
            )
