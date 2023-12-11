import asyncio
import json

from aio_pika import connect, ExchangeType, Message, DeliveryMode

from schemas import NewLineOfBook


class BookRabbitTopicBroker(object):
    def __init__(
            self,
            amqp_url: str = "amqp://guest:guest@localhost:5672/",
            routing_key: str = "book.new.line"
    ):
        self._channel = None
        self._connection = None
        self._queue = None
        self._exchange = None
        self._amqp_url = amqp_url
        self._routing_key = routing_key

    async def start(self):
        self._connection = await connect(self._amqp_url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            "book-processor", ExchangeType.TOPIC,
        )
        self._queue = await self._channel.declare_queue(
            "book-queue", durable=True,
        )
        await self._queue.bind(self._exchange, routing_key=self._routing_key)
        print("\tBookRabbitTopicBroker started")

    async def stop(self):
        self._connection.close()

    async def send_messages(self, message: NewLineOfBook):
        # print("send mess:", message.json())
        mess = Message(
            json.dumps(message.dict(), default=str).encode("utf-8"),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await self._exchange.publish(mess, routing_key=self._routing_key)
        # await asyncio.sleep(3)

    async def set_consumer(self, callback):
        # Maximum message count which will be processing at the same time.
        # await self._channel.set_qos(prefetch_count=100)
        await self._queue.consume(callback)
