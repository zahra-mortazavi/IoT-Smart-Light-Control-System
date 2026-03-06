import logging
import time
import serial
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(
model="gpt-3.5-turbo",
base_url="https://api.avalai.ir/v1",
api_key="OPENAI_API_KEY""
)
ser = serial.Serial(port="COM4",  baudrate=115200, timeout=1,dsrdtr=False,rtscts=False)
ser.dtr = False
ser.rts=False
def process_command(command):
    prompt = [
        {
            "role": "system",
            "content": """You are an assistant for an IoT system that
    controls LED lights. Based on the user's prompt, you must decide which
    function to call for controlling the lights.
    The function options are:
    A: turning on the light kitchen,
    B: turning off the light kitchen,
    C: turning on the light room,
    D: turning off the light room,
    E: turning on both kitchen and room lights,
    F: turning off both kitchen and room lights.
    G: turning on the light room and turning off the light kitchen,
    H: turning on the light kitchen and turning off the light room,.
    You must only respond with a single character (A, B, C, D, E, F, G or H)
    corresponding to the function. DO NOT add any other information or
    text.""",
        },
        {
            "role": "user",
            "content": command
        },
    ]
    response = llm.invoke(prompt)
    return response.content.strip()
if not ser.is_open:
    ser.open()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Help!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.text)
    response = process_command(update.message.text)
    print(response)
    ser.write(f"{response}\n".encode('utf-8'))
    await update.message.reply_text(update.message.text)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    application = ApplicationBuilder().token("TELEGRAM_BOT_TOKEN").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_error_handler(error)
    application.run_polling()

if __name__ == '__main__':
    main()
