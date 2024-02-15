import asyncio
import logging
from settings import server_ip, server_port

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', level=logging.INFO)

class Server:
    def __init__(self) -> None:
        self.priority_queue = asyncio.PriorityQueue()
    
    @staticmethod
    def is_float(num) -> bool:
        try:
            num = float(num)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_int(num) -> bool:
        try:
            num = int(num)
            return True
        except ValueError:
            return False
    
    async def check_expression(self, writer: asyncio.StreamWriter, expression: str) -> bool:
        parts = expression.split()
        
        if parts[1] not in ["+", "-", "/", "*", "%", "^", "**"]:
            writer.write(str("недоступная операция").encode())
            logging.info(f"Результат не обработан: недоступная операция")
            await writer.drain()
            return False
        
        if not all(Server.is_float(exp) or Server.is_int(exp) for exp in parts[0:3:2]):
            writer.write(str("проверьте правильность ввода чисел").encode())
            logging.info(f"Результат не обработан: ошибка ввода чисел")
            await writer.drain()
            return False
        
        if parts[1] == "/" and parts[2] == "0":
            writer.write(str("деление на ноль недопустимо").encode())
            logging.info(f"Результат не обработан: деление на ноль недопустимо")
            await writer.drain()
            return False
        
        return True
    
    async def calc_expression(self, expression: str):
        first_num, operation, second_num = expression.split()
        first_num, second_num = float(first_num), float(second_num)
        
        match operation:
            case "+":
                return first_num + second_num
            case "-":
                return first_num - second_num
            case "*":
                return first_num * second_num
            case "/":
                return first_num / second_num
            case "%":
                return first_num % second_num
            case "^" | "**":
                return first_num ** second_num
            
    async def handle_client_request(self, writer: asyncio.StreamWriter, expression: str):
        client_ip, client_port = writer.get_extra_info("peername")
        
        if not await self.check_expression(writer, expression):
            return
        
        result = await self.calc_expression(expression)
        writer.write(str(result).encode())
        await writer.drain()
        logging.info(f"Результат {result} отправлен на {client_ip}:{client_port}")
    
    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        while True:
            client_ip, client_port = writer.get_extra_info("peername")
            logging.info(f"Соединение с {client_ip}:{client_port}")
            
            try:
                data = await reader.read(1024)
            except (ConnectionResetError, ConnectionAbortedError):
                logging.info(f"Соединение с {client_ip}:{client_port} прервано")
                writer.close()
                await writer.wait_closed()
                return
            
            client_ip, client_port = writer.get_extra_info("peername")
            
            message = data.decode()
            
            priority, expression = message.split("|", 1)
            priority = int(priority)
            
            await self.priority_queue.put((priority, reader, writer, expression))
            logging.info(f"Получено выражение ({expression}) с приоритетом {priority} от {client_ip}:{client_port}") 

            while not self.priority_queue.empty():
                _, reader, writer, expression = await self.priority_queue.get()
                await self.handle_client_request(writer, expression)
    
    async def run(self):
        server = await asyncio.start_server(self.handle_connection, server_ip, server_port)
        logging.info("Сервер запущен, ожидаю на вход выражения (Ctrl+C для выхода)")

        async with server:
            await server.serve_forever()
    
if __name__ == "__main__":
    server = Server()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logging.info("Принудительно завершаю работу")