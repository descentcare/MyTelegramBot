#!/usr/bin/env python
from config import TOKEN, CREATORID
import subprocess, os, eyed3
from telegram import Update
from telegram.ext import (
        ApplicationBuilder,
        CommandHandler,
        MessageHandler,
        ContextTypes,
        filters,
        )

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"""Hello! {update.effective_user.first_name}!
You cannot use me unless you are my creator! You're not so leave me alone""")

async def ytdlm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id == CREATORID:
        command = update.message.text.split()
        if len(command) > 1:
            await update.message.reply_text(f"Downloading {command[1]}")
            try:
                searchfor = "\n[ExtractAudio] Destination: "
                out = str(subprocess.check_output(['yt-dlp', '-x', '--audio-format', 'mp3',
                                               command[1]]), 'utf-8')
                if searchfor in out:
                    out = out[out.find(searchfor)+len(searchfor):]
                    out = out[:out.find('.mp3\n')+4]
                    audiofile = eyed3.load(out)
                    audiofile.tag.title = out[:out.rindex('[')-1]
                    audiofile.tag.save()
                    await update.message.reply_audio(open(out, 'rb').read())
                    os.system(f'rm "{out}"')
            except subprocess.CalledProcessError as err:
                print(err)
        else:
            await update.message.reply_text("Invalid action: send link after command")
    else:
        await update.message.reply_text("You are not my creator so you can't use this command")
async def wild_magic(update, context):
    try:
        magic = str(subprocess.check_output(["wm"]), 'utf-8')
        await update.message.reply_text(magic)
    except:
        pass

async def text_handler(update, context):
    try:
        #await update.message.reply_text("I do nothing in this circumstances")
        await update.message.reply_text(update)
    except:
        pass


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", hello))
app.add_handler(CommandHandler("yt", ytdlm))
app.add_handler(CommandHandler("wm", wild_magic))
app.add_handler(MessageHandler(filters.TEXT, text_handler))

app.run_polling()
