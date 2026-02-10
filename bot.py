import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

AUTHORIZED_USERS = set([OWNER_ID])

API_URL = "https://amane.djsouravrooj33.workers.dev/?rc="

OWNER_USERNAME = "@amane_loyal_me"


# 🔐 Channel check
async def check_join(update: Update):
    user = update.effective_user
    member = await update.bot.get_chat_member(CHANNEL_ID, user.id)
    return member.status in ["member", "administrator", "creator"]


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joined = await check_join(update)
    if not joined:
        keyboard = [
            [InlineKeyboardButton("🔔 Join Channel", url="https://t.me/amane_loyal_me")]
        ]
        await update.message.reply_text(
            "❌ আগে Channel Join করো",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text(
        f"✅ Bot Ready!\nOwner: {OWNER_USERNAME}\n\nRC Number পাঠাও"
    )


# /help
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Bot start\n"
        "/adduser <id> - Authorize user (Owner only)\n"
        "RC Number পাঠিয়ে search করো"
    )


# /adduser
async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    try:
        uid = int(context.args[0])
        AUTHORIZED_USERS.add(uid)
        await update.message.reply_text(f"✅ User {uid} Authorized")
    except:
        await update.message.reply_text("❌ Use: /adduser user_id")


# RC search
async def search_rc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in AUTHORIZED_USERS:
        await update.message.reply_text("❌ You are not authorized")
        return

    rc = update.message.text.strip()
    res = requests.get(API_URL + rc).text

    await update.message.reply_text(
        f"🔍 Result by {OWNER_USERNAME}\n\n{res}"
    )


# Main
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("adduser", add_user))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_rc))

app.run_polling()