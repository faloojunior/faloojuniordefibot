import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, CallbackContext

# Configuration (TESTING ONLY - WILL BE REVOKED)
BOT_TOKEN = "7751220488:AAEcGdNx4YTSU7LDAh8ToBZYXeyqs7101-E"  # Testing token - will be revoked
CHANNEL_USERNAME = "@your_channel"  # Replace with your actual channel username
GROUP_USERNAME = "@your_group"     # Replace with your actual group username
TWITTER_USERNAME = "your_twitter"  # Replace with your actual Twitter handle

async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    welcome_message = (
        f"🚀 *Welcome {user.first_name} to Our Mega Airdrop!* 🚀\n\n"
        "🎁 *Get 10 SOL tokens for completing these simple steps:*\n"
        "1. Join our official Telegram channel\n"
        "2. Join our community group\n"
        "3. Follow us on Twitter\n"
        "4. Submit your Solana wallet address\n\n"
        "_Click the buttons below to complete the steps:_"
    )
    
    keyboard = [
        [InlineKeyboardButton("📢 JOIN CHANNEL", url=f"https://t.me/{CHANNEL_USERNAME}")],
        [InlineKeyboardButton("👥 JOIN GROUP", url=f"https://t.me/{GROUP_USERNAME}")],
        [InlineKeyboardButton("🐦 FOLLOW TWITTER", url=f"https://twitter.com/{TWITTER_USERNAME}")],
        [InlineKeyboardButton("✅ DONE ALL STEPS", callback_data="completed_steps")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "completed_steps":
        await query.edit_message_text(
            "🎉 *Great job!* You're one step away from your reward!\n\n"
            "📤 *Please send me your Solana wallet address now.*\n\n"
            "Example: `D4W16X5JcV9j1Mjx7eQa1uJ7J8Zb3Jx7eQa1uJ7J8Zb3Jx7eQa1u`\n\n"
            "_We'll send your 10 SOL to this address_",
            parse_mode='Markdown'
        )

async def handle_wallet(update: Update, context: CallbackContext) -> None:
    wallet_address = update.message.text.strip()
    
    # Basic Solana address validation (length check)
    if 32 <= len(wallet_address) <= 44 and wallet_address.isalnum():
        response = (
            "✨ *CONGRATULATIONS!* ✨\n\n"
            "💎 *10 SOL Reward Approved!*\n\n"
            f"🔹 *Wallet:* `{wallet_address}`\n"
            "🔹 *Status:* Processing\n"
            "🔹 *Estimated Time:* 24-48 hours\n\n"
            "_Thank you for participating in our airdrop!_"
        )
        
        # Visual confirmation
        await update.message.reply_text("🔄 Processing your transaction...")
        await update.message.reply_text(response, parse_mode='Markdown')
        
        # Add some fun visuals
        await update.message.reply_text("✨" * 15)
        await update.message.reply_text("💎 10 SOL INCOMING 💎")
        await update.message.reply_text("✨" * 15)
    else:
        await update.message.reply_text(
            "⚠️ *Invalid Wallet Address*\n\n"
            "Please send a valid Solana wallet address.\n"
            "Example: `D4W16X5JcV9j1Mjx7eQa1uJ7J8Zb3Jx7eQa1uJ7J8Zb3Jx7eQa1u`\n\n"
            "_Make sure it's between 32-44 alphanumeric characters_",
            parse_mode='Markdown'
        )

def main() -> None:
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    
    # Start the bot
    print("🤖 Airdrop Bot is now running...")
    print(f"👉 Test it at: https://t.me/{application.bot.username}")
    application.run_polling()

if __name__ == "__main__":
    main()
