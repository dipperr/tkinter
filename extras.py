import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import numpy as np
import cv2
import PIL.Image
import PIL.ImageTk
from threading import Thread
import tkinter as tk
import dlib

from dtbase import dtbase


class SendEmail:
    def __init__(self, cpf):
        self.cod = str(np.random.randint(100000, 9000000))
        self.cpf = cpf
        self.database = dtbase.DataBase()
        self.__search_email()
        self.__mime()
        self.__smtp()

    def __mime(self):
        self.msg = MIMEMultipart()
        self.__password = 'xgjxdbkkotngvuyb'
        self.msg['From'] = 'portariateste3@gmail.com'
        self.msg['To'] = self.to_email
        self.msg['Subject'] = 'Senha Temporaria'
        self.msg.attach(MIMEText(self.cod, 'plain'))

    def __smtp(self):
        self.server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        if self.server.ehlo()[0] == 250:
            if self.server.starttls()[0] == 220:
                if self.server.login(self.msg['From'], self.__password)[0] == 235:
                    self.server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
                    self.__update_key()
                    self.server.quit()
                else:
                    raise ConnectionError('Não foi possivel conectar\nao servidor')
            else:
                raise ConnectionError('Não foi possivel conectar\nao servidor')
        else:
            raise ConnectionError('Não foi possivel conectar\nao servidor')

    def __update_key(self):
        self.database.update(
            "UPDATE portporteiro SET senha=:senha WHERE cpf=:cpf",
            {'senha': hashlib.md5(self.cod.encode()).hexdigest(), 'cpf': self.cpf}
        )

    def __search_email(self):
        self.database.search(f"SELECT email FROM portporteiro WHERE cpf = '{self.cpf}'")
        self.to_email = self.database.cursor.fetchone()
        self.database.close()
        if self.to_email:
            self.to_email = self.to_email[0]
        else:
            raise Exception('email não encontrado')


class Authentication:
    def __init__(self, cpf, senha=None):
        self.cpf = cpf
        self.senha = senha
        self.database = dtbase.DataBase()
        self.__format_cpf()

    def __search_key(self):
        self.database.search(f"SELECT senha FROM portporteiro WHERE cpf = '{self.cpf}'")
        consulta = self.database.cursor.fetchone()
        self.database.close()
        if consulta:
            return consulta[0]
        else:
            raise Exception('cpf inválido')

    def authentication(self):
        self.senha = hashlib.md5(self.senha.encode()).hexdigest()
        consulta = self.__search_key()
        if self.senha == consulta:
            return True
        else:
            return False

    def recovery_key(self):
        send_email = SendEmail(self.cpf)

    def __format_cpf(self):
        self.cpf = self.cpf.replace('.', '').replace('-', '').replace(' ', '')


class FaceDetector:
    def __init__(self):
        self.face_detector = dlib.get_frontal_face_detector()

    def detector(self, frame):
        detects = self.face_detector(frame)
        if len(detects) != 0:
            for face in detects:
                l, t, r, b = face.left(), face.top(), face.right(), face.bottom()
                cv2.rectangle(frame, (l, t), (r, b), (0, 0, 255), 2)
            return frame
        else:
            return frame


class VideoSurveillance:
    def __init__(self, cam):
        self.__init(cam)

    def __init(self, cam):
        self.window = tk.Toplevel()
        self.cap = cv2.VideoCapture(cam)
        self.face_detector = FaceDetector()
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.interval = 20
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0)
        self.__update_image()

    def __update_image(self):
        ok, self.frame = self.cap.read()
        if ok:
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            self.frame = self.face_detector.detector(self.frame)
            self.image = PIL.Image.fromarray(self.frame)
            self.image = PIL.ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        else:
            # print temporário. deverá ser implementado uma tratativa de erro
            self.window.destroy()
            raise Exception('impossivel obter video')
        self.window.after(self.interval, self.__update_image)

    def __del__(self):
        self.cap.release()


class ThreadVideo(Thread):
    def __init__(self, cam):
        super().__init__(daemon=True)
        self.cam = cam

    def run(self):
        self.app = VideoSurveillance(self.cam)
