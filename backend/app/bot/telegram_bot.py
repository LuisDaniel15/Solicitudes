import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from telegram.ext import MessageHandler, filters

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

API_URL = "http://localhost:8000"  # tu backend

historial_usuarios = {}

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


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        mensaje = " ".join(context.args)

        res = requests.post(f"{API_URL}/solicitudes/chat", json={"mensaje": mensaje})

        # 🔍 DEBUG
        print("STATUS:", res.status_code)
        print("TEXT:", res.text)

        if res.status_code != 200:
            await update.message.reply_text("Error conectando con el servidor")
            return

        data = res.json()

        respuesta = data.get("respuesta")

        if respuesta:
            await update.message.reply_text(respuesta)
        else:
            await update.message.reply_text("No se pudo obtener respuesta")

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")


import asyncio
import requests

historial_usuarios = {}

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        mensaje = update.message.text
        mensaje_lower = mensaje.lower()

        # 🔹 respuestas rápidas (más humano)
        if "hola" in mensaje_lower:
            await update.message.reply_text("¡Hola! 👋 Soy tu asistente académico. ¿En qué puedo ayudarte?")
            return

        if "gracias" in mensaje_lower:
            await update.message.reply_text("¡Con gusto! 😊")
            return

        # 🔹 memoria por usuario
        if user_id not in historial_usuarios:
            historial_usuarios[user_id] = []

        historial_usuarios[user_id].append(mensaje)

        # solo últimas 3 interacciones
        contexto = " ".join(historial_usuarios[user_id][-3:])

        # 🔹 simula escritura
        await update.message.chat.send_action(action="typing")
        await asyncio.sleep(1)

        # 🔹 petición al backend (RAG)
        res = requests.post(
            f"{API_URL}/solicitudes/chat",
            json={"mensaje": contexto},
            timeout=10
        )

        print("STATUS:", res.status_code)
        print("TEXT:", res.text)

        if res.status_code != 200:
            await update.message.reply_text("⚠️ Error conectando con el servidor")
            return

        data = res.json()

        respuesta = data.get("respuesta", "🤔 No entendí tu pregunta")

        # 🔹 evitar respuestas muy largas
        respuesta = respuesta[:800]

        await update.message.reply_text(respuesta)

    except Exception as e:
        print("ERROR REAL:", e)
        await update.message.reply_text("❌ Ocurrió un error, intenta nuevamente")


def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("estado", estado))
    app.add_handler(CommandHandler("mis_solicitudes", mis_solicitudes))
    app.add_handler(CommandHandler("chat", chat))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))

    print("Bot corriendo...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()