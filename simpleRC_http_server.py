from socket import *
import sys

serverSocket = socket(AF_INET, SOCK_STREAM)
portadoserver = 6789
serverSocket.bind(('', portadoserver))
serverSocket.listen(1)

print(f"Servidor HTTP rodando em porta {portadoserver} ... (Ctrl+C para encerrar)")

try:
    while True:
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024).decode()
            if not message:
                connectionSocket.close()
                continue
            filename = message.split()[1]   

            try:
                with open(filename[1:], 'r', encoding='utf-8') as f:
                    outputdata = f.read()

                body_bytes = outputdata.encode('utf-8')
                header = "HTTP/1.1 200 OK\r\n"
                header += "Content-Type: text/html; charset=utf-8\r\n"
                header += f"Content-Length: {len(body_bytes)}\r\n"
                header += "\r\n"

                connectionSocket.send(header.encode('utf-8'))
                connectionSocket.send(body_bytes)

            except FileNotFoundError:
                response_body = "<html><body><h1>404 Not Found</h1></body></html>"
                body_bytes = response_body.encode('utf-8')
                header = "HTTP/1.1 404 Not Found\r\n"
                header += "Content-Type: text/html; charset=utf-8\r\n"
                header += f"Content-Length: {len(body_bytes)}\r\n"
                header += "\r\n"
                connectionSocket.send(header.encode('utf-8'))
                connectionSocket.send(body_bytes)

            connectionSocket.close()

        except Exception as e:
            print("Erro ao tratar requisição:", e)
            try:
                connectionSocket.close()
            except:
                pass

except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário.")

finally:
    serverSocket.close()
    sys.exit(0)

