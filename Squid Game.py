import numpy as np
import cv2
from time import sleep as dl
from PIL import ImageFont, ImageDraw, Image
from sys import exit, argv
from threading import Thread as Th
from winsound import SND_ASYNC, PlaySound
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QPushButton, QApplication
from PyQt5.QtGui import QImage, QPalette, QFont, QBrush

class Pencere(QWidget):
    def __init__(self):
        super().__init__()
        PlaySound('Data/a.wav', SND_ASYNC)
        self.Ana_Sayfa()
        self.list = [['Semsiye.png', 'Şemsiye', 3000, False, (0, 0, 0), 0.650],['Yuvarlak.png', 'Yuvarlak', 3000, False, (0, 0, 0), 0.650],['Ucgen.png', 'Üçgen', 3000, False, (0, 0, 0), 0.650],['Yildiz.png', 'Yıldız', 3000, False, (0, 0, 0), 0.650],['Kucuk_Ucgen.png', '', 0, True, (0, 255, 0), 0.551]]

    def Ana_Sayfa(self):
        oImage = QImage('Data/a.jpg')
        sImage = oImage.scaled(QSize(700, 400))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)
        self.setFixedSize(700, 400)
        self.l1 = QLabel('Squid Game Honeycomb')
        self.l1.setFont(QFont('Century Gothic', 47))
        self.b1 = QPushButton('Başla')
        self.b1.setFont(QFont('Century Gothic', 30))
        self.b1.clicked.connect(self.Thread)
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.l1)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.b1)
        self.form = QFormLayout()
        self.form.addRow(self.vbox)
        self.setLayout(self.form)
        self.setWindowTitle('Squid Game')
        self.show()

    def Thread(self):
        self.b1.setDisabled(True)
        self.resim_rgb = cv2.imread('Data/b.jpg')
        cv2.imshow('Squid Game', self.resim_rgb)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()
        self.resim_gri = cv2.cvtColor(self.resim_rgb, cv2.COLOR_BGR2GRAY)
        for i in self.list:
            th1 = Th(target=self.Nesne_Bulma, args=(i[0], i[1], i[2], i[3], i[4], i[5]))
            th1.start()
            dl(3.1)

    def Nesne_Bulma(self, Nesne, Nesne_isim, Zaman, bool, renk, tre):
        nesne = cv2.imread(f'Data/{Nesne}', 0)
        w, h = nesne.shape[:: -1]
        sonuc = cv2.matchTemplate(self.resim_gri, nesne, cv2.TM_CCOEFF_NORMED)
        loc = np.where(sonuc > tre)
        for i in zip(*loc[:: -1]):
            cv2.rectangle(self.resim_rgb, i, (i[0] + w, i[1] + h), renk, 2)
            self.w = i[0] + w
            self.h = i[1] + h
        resim_pil =Image.fromarray(self.resim_rgb)
        ciz =ImageDraw.Draw(resim_pil)
        font=ImageFont.truetype(font='Data/CenturyGothic.ttf',size=32)
        ciz.text((self.w-107, self.h),f"{Nesne_isim}",font=font,fill=(255, 0, 0))
        self.resim_rgb =np.array(resim_pil)
        cv2.imshow('Squid Game', self.resim_rgb)
        cv2.waitKey(Zaman)
        cv2.destroyAllWindows()
        if bool:
            self.b1.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(argv)
    pencere = Pencere()
    exit(app.exec())