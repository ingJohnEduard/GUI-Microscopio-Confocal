import serial, time
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image

from datetime import datetime 
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class SetupArduino(QObject):
    running = False
    signalOpen =  Signal(str, object)
    signalClose =  Signal(str)
    
    def __init__(self):
        QObject.__init__(self)
        print("Hola")

    def init_arduino(self):
        arduino = serial.Serial("COM3", 500000)
        self.signalOpen.emit("Ok", arduino)
        QThread.msleep(1000)
        #print("ok")

    def close_arduino(self, arduino):
        arduino.close()
        self.signalClose.emit("CIAO")
        QThread.msleep(1000)
        #print("ciao")

    def send_serial(self, string):
        self.arduino.write(str(string).encode())

    def read_serial(self):
        data = int(self.arduino.readline())
        return data

    
class CamUsb(QObject):
    stop = True
    SignalPreview = Signal(object)

    def __init__(self):
        QObject.__init__(self)
        print("Preview Cam")
        self.preview_cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.preview_cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.preview_cam.set(cv2.CAP_PROP_EXPOSURE, -6)
        self.preview_cam.set(cv2.CAP_PROP_BRIGHTNESS, 20)
        self.preview_cam.set(cv2.CAP_PROP_CONTRAST, 50)
        self.preview_cam.set(cv2.CAP_PROP_SATURATION, 85)
        self.preview_cam.set(cv2.CAP_PROP_BACKLIGHT, 1)
        

    def EndPreview(self, stop):
        self.stop = stop

    def RunPreview(self):
        
        while (self.stop):
            ret,frame = self.preview_cam.read()
            if ret:
                self.SignalPreview.emit(frame)
            else:
                break

        self.preview_cam.release()
        #cv2.destroyAllWindows() NO USAR CON LA INTERFAZ



class Escaneo(QObject):

    isRunning = True
    signalFrame = Signal(object)
    SignalBar = Signal(int, int)

    def __init__(self, limiteX, limiteY, resolucion, arduino):
        QObject.__init__(self)
        self.arduino = arduino
        self.limiteX = limiteX
        self.limiteY = limiteY
        self.resolucion = resolucion

    def end(self, isRunning):
        self.isRunning = isRunning

    def Sumatoria(self, matriz):
        elementos = 0
        total = 0
        for fila in matriz:
            for elemento in fila:
                total += elemento
                elementos += 1
        #print(fila,elemento)
        promedio = total / elementos
        #print(promedio)
        return promedio
    
    def RunScan(self):
        print("Run Scan")
        
        pixelesX = round(self.limiteX/self.resolucion)
        pixelesY = round(self.limiteY/self.resolucion)
        pasos = self.resolucion*2/5*32
        print(pixelesX, pixelesY, pasos)

        ROI=open("ROI.txt","r")
        x1=int(ROI.readline())
        y1=int(ROI.readline())
        x2=int(ROI.readline())
        y2=int(ROI.readline())
        ROI.close()
        print("ROI:", x1,y1,x2,y2)
        #  ----------------------------------------------------------------------------  #
        self.cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cam.set(cv2.CAP_PROP_EXPOSURE, -6)
        self.cam.set(cv2.CAP_PROP_BRIGHTNESS, 20)
        self.cam.set(cv2.CAP_PROP_CONTRAST, 50)
        self.cam.set(cv2.CAP_PROP_SATURATION, 85)
        self.cam.set(cv2.CAP_PROP_BACKLIGHT, 1)
        

        #  ----------------------------------------------------------------------------  #
        estado = b'3'
        self.arduino.write(str(estado).encode())
        self.arduino.write(str(pasos).encode())
        print("Conencting Arduino...")
        data = int(self.arduino.readline())
        print(data)
        photo_red = np.zeros((pixelesY,pixelesX))
        photo = np.zeros((pixelesY,pixelesX))
        #pil_image = Image.fromarray(photo_red)
        #pil_image.show()
        #  ----------------------------------------------------------------------------  #
        for j in range(pixelesY):
            print(j)
            self.SignalBar.emit(pixelesY, j)
            tiempot = 0
            inicio = time.time()

            #  ------------------------------------------------------------------------  #
            for i in range(pixelesX):
                estado = b'4'
                self.arduino.write(str(estado).encode())

                #ACK = 0
                #while (ACK != 4):
                #    ACK = int(self.arduino.readline())
                    #print(ACK)
                if(self.cam.isOpened()):
                    ret,frame = self.cam.read()
                    if ret:
                        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        self.signalFrame.emit(frame)
                        photo[j][i] = self.Sumatoria(gray_frame[y1:y2, x1:x2])
                        photo_red[j][i] = self.Sumatoria(frame[y1:y2, x1:x2, 2])
                else:
                    print("Reconecting...")
                    time.sleep(3)
                    self.cam.release()
                    self.cam = cv2.VideoCapture(0, cv2.CAP_MSMF)
                
                if not self.isRunning:
                    break
            #  ------------------------------------------------------------------------  #


            estado = b'5'
            self.arduino.write(str(estado).encode())
            ACK = 0
            while (ACK != 5):
               ACK = int(self.arduino.readline())

            #for k in range(pixelesX):
            estado = b'7'
            self.arduino.write(str(estado).encode())
            self.arduino.write(str(i+1).encode())

            ACK = 0
            while (ACK != 7):
               ACK = int(self.arduino.readline())

            #  ------------------------------------------------------------------------  #
            
            fin = time.time()
            tiempot = fin-inicio
            tiempof = tiempot
            print(tiempof)
            np.savetxt('backup.txt',photo)
            np.savetxt('backup_red.txt',photo_red)
            cv2.imwrite('photo.bmp', photo)
            cv2.imwrite('photo_red.bmp', photo_red)
            pil_image = Image.fromarray(photo_red)
            
            if not self.isRunning:
                    break

        #  ----------------------------------------------------------------------------  #
        
        #for m in range(pixelesY):
        estado = b'8'
        self.arduino.write(str(estado).encode())
        self.arduino.write(str(j).encode())
        #time.sleep(2/1000)
        ACK = 0
        while (ACK != 8):
            ACK = int(self.arduino.readline())
        

        self.SignalBar.emit(pixelesY, j+1)

        #  ----------------------------------------------------------------------------  #
        date = '-'+time.strftime("%Y-%m-%d-%H-%M-%S")
        info = '-'+str(self.limiteX)+'x'+str(self.limiteY)+'um'+'-'+str(pixelesX)+'x'+str(pixelesY)+'px'
        label_backup = 'imagenes/backup_red'+info+date+'.txt'
        label_photo = 'imagenes/photo_red'+info+date+'.bmp'
    
        np.savetxt(label_backup,photo_red)
        cv2.imwrite(label_photo, photo_red)
        #photo_plt = cv2.imread('photo.bmp')
        #plt.imshow(photo_plt)
        #plt.show()

        pil_image = Image.fromarray(photo)
        pil_image.show()
        
        self.cam.release()