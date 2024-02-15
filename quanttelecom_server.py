import threading
import asyncio
import socket
from queue import PriorityQueue
from typing import Tuple
import logging
import signal

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s %(message)s', level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

class Server:
    def __init__(self) -> None:
        self.priority_queue = asyncio.PriorityQueue()
    
    async def process_expression(self, expression: str):
        logging.info(f"ОБРАБОТКА ВЫРАЖЕНИЯ {expression} TODO")
        return expression

    async def handle_client_request(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, expression: str):
        result = await self.process_expression(expression)
        writer.write(str(result).encode())
        await writer.drain()
        logging.info(f"Результат {result} отправлен на TODO") #{client_address} 
    
    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while True:
            data = await reader.read(1024)
            if not data:
                break
            message = data.decode()
            priority, expression = message.split("|", 1)
            priority = int(priority)
            await self.priority_queue.put((priority, reader, writer, expression))
            logging.info(f"TODO Получено сообщение с приоритетом {priority}") #{client_address} 

            while not self.priority_queue.empty():
                _, reader, writer, expression = await self.priority_queue.get()
                await self.handle_client_request(reader, writer, expression)
    
    async def run(self):
        server = await asyncio.start_server(self.handle_connection, '127.0.0.1', 12345)
        logging.info("Сервер запущен, ожидаю сообщения")

        async with server:
            await server.serve_forever()
    
if __name__ == "__main__":
    server = Server()
    asyncio.run(server.run())