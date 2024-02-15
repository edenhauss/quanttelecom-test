import socket

class Client:
    def __init__(self) -> None:
        pass
    
    def get_priority(self):
        priority = input("Введите приоритет операции (целое число): ")
        return priority
    
    def main(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        server_address = ('127.0.0.1', 12345)
        previous_result = None

        while True:
            expression = input("Введите выражение (или 'exit' для выхода): ")
            if expression == 'exit':
                break
            
            if expression == 'previous' and previous_result is not None:
                expression = previous_result
            
            priority = self.get_priority()
            message = f"{priority}|{expression}"
            client_socket.sendto(message.encode(), server_address)
            
            response, _ = client_socket.recvfrom(1024)
            result = response.decode()
            print("Результат:", result)

            previous_result = result
      
if __name__ == "__main__":
    client = Client()
    client.main()