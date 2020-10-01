#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import logging
import os
import sys
from typing import Tuple

import telegram
from pinboard import Pinboard
from telegram import Message, MessageEntity, Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    pb = Pinboard(os.environ["PB_TOKEN"])
    authorized_user = int(os.environ["TELEGRAM_USER"])

    updater = Updater(token=os.environ["TELEGRAM_TOKEN"], use_context=True)
    dispatcher = updater.dispatcher

    message_handler = MessageHandler(
        Filters.text,
        lambda update, context: on_message(update, context, pb, authorized_user),
    )
    dispatcher.add_handler(message_handler)

    updater.start_polling()


def on_message(
    update: Update, context: CallbackContext, pb: Pinboard, authorized_user: int
):
    bot: telegram.Bot = context.bot

    if update.effective_user.id != authorized_user:
        bot.send_message(update.effective_chat.id, text="Not authorized")
        return

    message: Message = update.message

    urls: Tuple[str, ...] = tuple(message.parse_entities([MessageEntity.URL]).values())

    if len(urls) < 1:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="No URLs found in message",
            reply_to_message_id=message.message_id,
        )
        return

    if len(urls) > 1:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="More than one URL found in message",
            reply_to_message_id=message.message_id,
        )
        return

    url = urls[0]

    title: str = message.text.replace(url, "").strip()
    if not title:
        title = "[no title]"

    try:
        pb.posts.add(
            url=url, description=title, replace=False, shared=False, toread=True
        )
    except Exception as exception:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=str(exception),
            reply_to_message_id=message.message_id,
        )
    else:
        bot.send_message(
            chat_id=update.effective_chat.id,
            text="Added!",
            reply_to_message_id=message.message_id,
        )


if __name__ == "__main__":
    sys.exit(main())
