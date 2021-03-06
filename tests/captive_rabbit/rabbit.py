import logging
import pika

from queue import Queue


class Rabbit:

    def __init__(self):
        self.host = "localhost"
        self._queues = []
        self._connected = False
        self._configure_pika_logging()

    def make_queue(self):
        self.connect()
        queue = Queue(self)
        self._queues.append(queue)
        queue.create()
        return queue

    def channel(self):
        return self._channel;

    def teardown(self):
        for queue in self._queues:
            queue.delete()
        self.disconnect()

    def is_connected(self):
        return self._connected

    def connect(self):
        if self.is_connected():
            return
        params = pika.ConnectionParameters(self.host)
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._connected = True

    def disconnect(self):
        if not self.is_connected():
            return
        self._connection.close()
        self._connected = False

    def _configure_pika_logging(self):
        pika_logger = logging.getLogger('pika')
        pika_logger.setLevel(logging.CRITICAL)
