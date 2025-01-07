from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests

# Bot Token
BOT_TOKEN = '7672438625:AAGnZBeCnsbnX0OtNCMrCw8IZkP1gvLIPnE'

# Dictionary to track user warnings
user_warnings = {}

# Function: Start Command
def start(update, context):
    group_name = update.message.chat.title  # Fetch group name
    update.message.reply_text(
        f"আপনাকে স্বাগতম Nation_Of_Saviors গ্রুপে! আমি বাতেন গ্রুপের বট। আমি আপত্তিকর কন্টেন্ট মুছে ফেলব এবং গ্রুপের নিয়ম ভাঙলে ব্যবহারকারীকে রিমুভ করব। দয়া করে নিয়ম মেনে চলুন।"
    )

# Function: Filter Adult Content and Handle Warnings
def filter_content(update, context):
    user_id = update.message.from_user.id
    group_id = update.message.chat.id
    group_name = update.message.chat.title  # Fetch group name

    # Initialize warning count for new users
    if user_id not in user_warnings:
        user_warnings[user_id] = 0

    if update.message.photo or update.message.document:  # Check for images/videos
        file = update.message.photo[-1].get_file() if update.message.photo else update.message.document.get_file()
        file_path = file.file_path

        # Example API Call for Adult Content Detection (DeepAI)
        response = requests.post(
            "https://api.deepai.org/api/nsfw-detector",
            files={'image': requests.get(file_path).content},
            headers={'api-key': '89f9e33c-1386-4b5d-a467-fc133d921fe1'}
        )
        result = response.json()

        if result.get('output', {}).get('nsfw_score', 0) > 0.7:  # If NSFW score > 70%
            update.message.delete()
            user_warnings[user_id] += 1

            if user_warnings[user_id] == 1:
                # Send warning with group name and logo
                context.bot.send_photo(
                    chat_id=group_id,
                    photo=open('group_logo.jpg', 'rb'),  # Replace with your group logo image file path
                    caption=f"⚠️ {update.message.from_user.first_name}, এটি আপনার প্রথম সতর্কবার্তা। দয়া করে {group_name} গ্রুপে আপত্তিকর কন্টেন্ট শেয়ার করবেন না!"
                )
            elif user_warnings[user_id] > 1:
                context.bot.send_message(
                    chat_id=group_id,
                    text=f"❌ {update.message.from_user.first_name} চুদানির পোলা কে Nation_Of_Saviors গ্রুপ থেকে অপসারণ করা হয়েছে বারবার নিয়ম ভাঙার কারণে।"
                )
                context.bot.kick_chat_member(chat_id=group_id, user_id=user_id)

    elif update.message.text:  # Check for text messages
        keywords = ["adult", "চুদি", " আবাল", "খানকি", " মাগি", "মাগী", " বেশ্যা", "ইনবক্সে আসো", " khanki", "magi", " chudbo", "chudi tomare", " potki marbo",  "xxx", "porn", "sex"]  # Add more keywords as needed
        if any(keyword in update.message.text.lower() for keyword in keywords):
            update.message.delete()
            user_warnings[user_id] += 1

            if user_warnings[user_id] == 1:
                # Send warning with group name and logo
                context.bot.send_photo(
                    chat_id=group_id,
                    photo=open('group_logo.jpg', 'rb'),  # Replace with your group logo image file path
                    caption=f"⚠️ {update.message.from_user.first_name}, এটি আপনার প্রথম সতর্কবার্তা। দয়া করে Nation_Of_Saviors গ্রুপে আপত্তিকর ভাষা ব্যবহার করবেন না!"
                )
            elif user_warnings[user_id] > 1:
                context.bot.send_message(
                    chat_id=group_id,
                    text=f"❌ {update.message.from_user.first_name} চুদানির পোলাকে Nation_Of_Saviors গ্রুপ থেকে অপসারণ করা হয়েছে বারবার নিয়ম ভাঙার কারণে।"
                )
                context.bot.kick_chat_member(chat_id=group_id, user_id=user_id)

# Main Function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.document, filter_content))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
