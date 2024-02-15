import socket
import asyncio
from exceptions import ExpressionInputError, PriorityInputError
from settings import server_ip, server_port

class Client:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.previous_result = None
    
    async def get_priority(self) -> str:
        return input("Введите приоритет операции (целое число):\n")

    async def send_message(self, writer: asyncio.StreamWriter, message: str):
        writer.write(message.encode())
        await writer.drain()

    async def receive_response(self, reader: asyncio.StreamReader):
        response = await reader.read(1024)
        return response.decode()

    async def interact_with_server(self, server_address):
        reader, writer = await asyncio.open_connection(*server_address)

        while True:
            try:
                hint = "Введите через пробел два числа и знак между ними,\nлибо введите '> <знак операции> <новое число>' "\
                        "для работы с предыдущим результатом (Ctrl+C для выхода):\n" if self.previous_result else "Введите через "\
                        "пробел два числа и знак между ними (Ctrl+C для выхода):\n"
                        
                expression = input(hint)
                
                if expression.startswith(">") and self.previous_result:
                    expression = f"{self.previous_result} {expression[2:]}"
                   
                if len(expression.split()) != 3:
                    raise ExpressionInputError
                
                priority = int(await self.get_priority())
            
            except ValueError:
                raise PriorityInputError
            
            except KeyboardInterrupt:
                print("Принудительно завершаю работу")
                writer.close()
                await writer.wait_closed()
                return
            
            else:
                message = f"{priority}|{expression}"
                await self.send_message(writer, message)
                
                result = await self.receive_response(reader)
                print(f"Результат: {result}\n")
                self.previous_result = result

    def main(self):
        server_address = (server_ip, server_port)
        self.loop.run_until_complete(self.interact_with_server(server_address))
        
if __name__ == "__main__":
    client = Client()
    try:
        client.main()
    except ConnectionResetError:
        print("Переподключение к серверу")
        client.main()
    except ConnectionRefusedError:
        print("Не удается подключиться к серверу")