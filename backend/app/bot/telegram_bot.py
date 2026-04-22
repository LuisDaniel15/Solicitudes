import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

API_URL = "http://localhost:8000"  # tu backend


# 🔥 comando /estado
async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        solicitud_id = context.args[0]

        res = requests.get(f"{API_URL}/solicitudes/{solicitud_id}/estado")
        data = res.json()

        mensaje = f"Tu solicitud {data['codigo']} está en estado: {data['estado']}"

        await update.message.reply_text(mensaje)

    except:
        await update.message.reply_text("Error consultando la solicitud")


# 🔥 comando /mis_solicitudes
async def mis_solicitudes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        usuario_id = context.args[0]

        res = requests.get(f"{API_URL}/solicitudes/usuario/{usuario_id}")
        data = res.json()

        mensaje = "Tus solicitudes:\n"

        for s in data:
            mensaje += f"{s['codigo']} - {s['estado_actual']}\n"

        await update.message.reply_text(mensaje)

    except:
        await update.message.reply_text("Error consultando solicitudes")


def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("estado", estado))
    app.add_handler(CommandHandler("mis_solicitudes", mis_solicitudes))

    print("Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()