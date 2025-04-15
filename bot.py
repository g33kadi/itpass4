import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update
import os

DATA_FILE = "data.json"

# Load or initialize data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

user_data = load_data()

def get_user(update: Update):
    return str(update.effective_user.id)

# Start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Welcome to Financial Planner Bot!\nUse /help to see available commands.")

# Help
def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("/config - Set income & budgets\n/log - Log expense or income\n/summary - View budget\n/notifyon or /notifyoff")

# Config
def config(update: Update, context: CallbackContext):
    user = get_user(update)
    args = context.args
    if len(args) < 2:
        update.message.reply_text("Usage: /config [income] [category1:amount,category2:amount,...]")
        return
    income = float(args[0])
    budgets = dict(x.split(":") for x in args[1].split(","))
    user_data[user] = {"income": income, "budgets": budgets, "logs": []}
    save_data(user_data)
    update.message.reply_text("✅ Income and budgets set!")

# Log
def log(update: Update, context: CallbackContext):
    user = get_user(update)
    args = context.args
    if len(args) < 2:
        update.message.reply_text("Usage: /log [category] [amount]")
        return
    category, amount = args[0], float(args[1])
    if user not in user_data:
        update.message.reply_text("Use /config first.")
        return
    user_data[user]["logs"].append({"category": category, "amount": amount})
    save_data(user_data)
    update.message.reply_text("✅ Logged!")

# Summary
def summary(update: Update, context: CallbackContext):
    user = get_user(update)
    if user not in user_data:
        update.message.reply_text("Use /config first.")
        return
    logs = user_data[user]["logs"]
    budgets = user_data[user]["budgets"]
    summary_msg = "📊 Summary:\n"
    spent = {}
    for log in logs:
        spent[log["category"]] = spent.get(log["category"], 0) + log["amount"]
    for cat in budgets:
        spent_amt = spent.get(cat, 0)
        summary_msg += f"{cat}: {spent_amt} / {budgets[cat]}\n"
    update.message.reply_text(summary_msg)

# Notify on/off (dummy for now)
def notifyon(update: Update, context: CallbackContext):
    update.message.reply_text("🔔 Notifications turned ON!")

def notifyoff(update: Update, context: CallbackContext):
    update.message.reply_text("🔕 Notifications turned OFF!")

def main():
    TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("config", config))
    dp.add_handler(CommandHandler("log", log))
    dp.add_handler(CommandHandler("summary", summary))
    dp.add_handler(CommandHandler("notifyon", notifyon))
    dp.add_handler(CommandHandler("notifyoff", notifyoff))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
