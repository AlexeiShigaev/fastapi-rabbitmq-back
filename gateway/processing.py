from datetime import datetime
import json

import aio_pika
import asyncio

from db import add_book
from rabbit import BookRabbitTopicBroker
from schemas import NewLineOfBook

books = {}

sender = BookRabbitTopicBroker(amqp_url="amqp://test:test@rabbitmq")
consumer = BookRabbitTopicBroker(amqp_url="amqp://test:test@rabbitmq")


async def file_processing(path: str, file_name: str):
    await sender.send_messages(NewLineOfBook(datetime=datetime.utcnow(), title=file_name, text="!!!START!!!"))
    with open(path + file_name, 'r') as book_file:
        # title = book_file.readline().rstrip()
        # print(f"title: {title}")
        while line := book_file.readline():
            try:
                await sender.send_messages(
                    NewLineOfBook(
                        datetime=datetime.utcnow(), title=file_name, text=line
                    )
                )
            except Exception as ex:
                print("\t!!! Проблема со строкой {} !!!\n\t{}".format(line, ex))
            # await asyncio.sleep(3)
    await sender.send_messages(NewLineOfBook(datetime=datetime.utcnow(), title=file_name, text="!!!FINISH!!!"))


async def consumer_cor(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process():
        mess = NewLineOfBook(**json.loads(message.body))
        # print("receive =", mess.json())

        if mess.text == "!!!START!!!":
            print("метка старт")
            books[mess.title] = {"lines": 0, "XCount": 0}
        elif mess.text == "!!!FINISH!!!":
            print("метка финиш")
            print("books:", books)
            await add_book(title=mess.title, average=books[mess.title]["XCount"] / books[mess.title]["lines"])
        elif mess.text == "":
            print("строка пустая, пропускаем")
        else:
            books[mess.title]["lines"] += 1
            books[mess.title]["XCount"] += mess.text.upper().count("Х")

            # await asyncio.sleep(1)

