import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the start function to handle the /start command
def start(update, context):
    # Send the start message with the button
    introduction = "🌟 Welcome to the Business Bot! 🌟\n\nThis bot is designed to receive your valuable thoughts and ideas related to our business. We appreciate your contribution! 💡✨\n\nPlease submit your business thought or idea."
    keyboard = [[InlineKeyboardButton("Submit Idea", callback_data='submit_idea')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(introduction, reply_markup=reply_markup)
    # Set the conversation state to active
    context.user_data['conversation_active'] = True

# Define the button_click function to handle button clicks
def button_click(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'submit_idea':
        # Prompt the user to submit their idea
        query.message.reply_text('✏️ Please type your business thought or idea and send it to me.')
        # Set the conversation state to active
        context.user_data['conversation_active'] = True

# Define the reply function to handle user replies
def reply(update, context):
    # Check if the conversation is active
    if context.user_data.get('conversation_active', False):
        # Forward the user's message to the admins
        forward_message_to_admins(update.message, context.bot)
        # Send the acknowledgment message
        try:
            update.message.reply_text('🙌 Thank you for submitting your business thought or idea! 🚀')
        except Exception as e:
            logging.error(f"Error while sending the acknowledgment message: {e}")
        # Set the conversation state to inactive
        context.user_data['conversation_active'] = False

# Function to forward the user's message to admins
def forward_message_to_admins(message, bot):
    admins = ['5752259504, 834552248']  # Replace with the chat IDs of your bot's admins
    for admin_chat_id in admins:
        try:
            forwarded_message = message.forward(chat_id=admin_chat_id)
            # Include user ID and username in the forwarded message
            user_id = message.from_user.id
            username = message.from_user.username

            if username:
                forwarded_message.caption = f"From: @{username} (User ID: {user_id})\n\n{forwarded_message.caption or ''}"
            else:
                forwarded_message.caption = f"From: User ID: {user_id}\n\n{forwarded_message.caption or ''}"

            bot.send_message(chat_id=admin_chat_id, text=forwarded_message.caption)
        except Exception as e:
            logging.error(f"Error while forwarding the message to admins: {e}")

# Define the main function to start the bot
def main():
    # Create an updater and dispatcher
    updater = Updater('6330068245:AAHTCoDiTkovk2Ar7uymOhPrHfSwZIbErUY', use_context=True)
    dp = updater.dispatcher

    # Add handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(button_click))
    dp.add_handler(MessageHandler(Filters.text, reply))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

