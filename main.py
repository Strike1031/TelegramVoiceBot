from elevenlabs import set_api_key, clone, generate, play
import telegram
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv() 
# Initialize
API_TOKEN = os.getenv("TELEGRAM_BOT_API_KEY")
ElevenLabs_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")

set_api_key(ElevenLabs_API_KEY) #set API key

print("Preparing bot....")
voice = clone(
    name="Strike",
    description="", # Optional
    files=["sample.mp3"],
)
print("Clone your voice completed!")

# Functions
async def start(update, context) -> None:
    await update.message.reply_text("Hello! I am a voice bot.")

async def textToVoice(update, context) -> None:
    # await update.message.reply_text(update.message.text)
    print(update.message.text)
    audio =generate(text=update.message.text, voice=voice)
    await update.message.reply_voice(audio)
    play(audio)


def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(API_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, textToVoice))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()