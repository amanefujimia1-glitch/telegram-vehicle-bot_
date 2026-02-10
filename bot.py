import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from telegram.constants import ChatMemberStatus

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

authorized_users = set([OWNER_ID])

# ---------- JOIN CHECK ----------
async def is_user_joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER,
        ]
    except:
        return False

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not await is_user_joined(user_id, context):
        keyboard = [
            [InlineKeyboardButton("🔔 Join Channel", url="https://t.me/your_channel_username")]
        ]
        await update.message.reply_text(
            "❌ Bot use করতে হলে আগে channel join করো",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await update.message.reply_text(
        "✅ Bot Ready!\n"
        "Owner: @amane_loyal_me\n\n"
        "Commands:\n"
        "/help"
    )

# ---------- HELP ----------
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Help Menu\n\n"
        "/adduser <id> – Authorize user (Owner only)\n"
        "/search <query> – Search\n\n"
        "Owner: @amane_loyal_me"
    )

# ---------- ADD USER ----------
async def adduser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ Only owner can use this")
        return

    if not context.args:
        await update.message.reply_text("Usage: /adduser <user_id>")
        return

    uid = int(context.args[0])
    authorized_users.add(uid)
    await update.message.reply_text(f"✅ User {uid} authorized")

# ---------- SEARCH ----------
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in authorized_users:
        await update.message.reply_text("❌ You are not authorized")
        return

    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Usage: /search <text>")
        return

    await update.message.reply_text(
        f"🔎 Search Result for: {query}\n"
        f"Requested by: @amane_loyal_me"
    )

# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("adduser", adduser))
    app.add_handler(CommandHandler("search", search))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
