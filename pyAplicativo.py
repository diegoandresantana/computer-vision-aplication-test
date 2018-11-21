import tkFileDialog
from Tkinter import *

from PIL import Image, ImageTk
from skimage.exposure import rescale_intensity
import numpy as np
import threading #necessario para manter os frames independente das outras tarefas
from skimage import feature
import cv2
import time

"""
    Tarefa do Aplicativo, nesse caso foi realizado em Python
    16/10/2018
    Autor: Diego Andre Sant'Ana
    Disciplina: Visao Computacional
    
    A consulta das funcionalidades utilizou o tutorial do OpenCV para Python.
     
"""
class TELA:

    ##Inicializacao dds componentes
    def __init__(self):

        self.font10 = "-family {DejaVu Sans} -size 14 -weight normal -slant"  \
            " roman -underline 0 -overstrike 0"


        self.clicked = False
        self.fingerling = {}

        # janela
        self.window = Tk()
        self.window.title("App")
        self.window.attributes('-zoomed', True)

        # lado esquerdo
        self.frameMenuLateral = Frame(self.window)
        self.frameMenuLateral.pack(side=LEFT, anchor=N, expand=True)
        # controles
        self.frameControls = LabelFrame(self.frameMenuLateral, text="Controls", padx=5, pady=5)
        self.frameControls.pack(anchor=N, pady=5, padx=5, fill=X)

        self.frameControlsOrganize = Frame(self.frameControls)
        self.frameControlsOrganize.pack(fill=X, expand=True)

        #Botao de ativar a camera
        self.btnActiveCapture = Button(self.frameControlsOrganize, text="Active Capture", padx=5, pady=5,
                                      command=self.active_capture)
        self.btnActiveCapture.pack(padx=5, pady=5, expand=True, fill=X)


        #Campo que mostra os dados do passo a passo
        self.frameLabelCon = LabelFrame(self.frameControlsOrganize, text="Options", padx=5, pady=5)
        self.frameLabelCon.pack(anchor=N, pady=5, padx=5, fill=X)
        self.frameInputValue = Frame(self.frameLabelCon)
        self.frameInputValue.pack(fill=X, expand=False)
        self.frameInputValue.columnconfigure(0, weight=3)
        self.frameInputValue.columnconfigure(1, weight=3)
        self.frameInputValue.columnconfigure(2, weight=3)
        self.frameInputValue.columnconfigure(3, weight=3)
        self.frameInputValue.columnconfigure(4, weight=3)
        self.frameInputValue.columnconfigure(5, weight=3)
        self.frameInputValue.grid(row=0, padx=20, sticky="nsew")
        self.frameInputValue.grid(row=1, padx=20, sticky="nsew")
        self.frameInputValue.grid(row=2, padx=20, sticky="nsew")
        self.frameInputValue.grid(row=3, padx=20, sticky="nsew")

        #opcoes radio das funcionalidades
        MODES = [
                ("Filter - Adaptative thresh Glaussian C", 0),
                ("Filter - Adaptative Threash Mean", 1),
                ("Detection Border - Find Countours - Alter Value Min and Max ", 2),
                ("Detection Border -  Canny -Alter Value Min and Max", 3),
                ("Morphology  - BLACKHAT - Alter Value Kernel", 4),
                ("Morphology - Erode - Alter Value Kernel", 5),
                ("Morphology - Dilate- Alter Value Kernel", 6),
                ("Morphology - Open - Alter Value Kernel", 7),
                ("Morphology - Close - Alter Value Kernel", 8),
                ("Morphology - Gradient Morphology - Alter Value Kernel", 9),

                ("Segmentation- Thresh_Binary_Inv - Alter Value Min and Max", 10),
                ("Segmentation - Thresh Binary - Alter Value Min and Max", 11),

                ("None", -1)
        ]

        self.radio = IntVar()
        self.radio.set(-1) # initialize
        c=3
        r=0
        for text, mode in MODES:
             if(mode==-1):
                 break
             b = Radiobutton(self.frameInputValue, text=text,
                                variable=self.radio, value=mode, command=None)
             b.grid(column=c,row=r, padx=10, sticky="nsew")
             r=r+1
             if(r>3):
                 c=c+1
                 r=0


        self.imagemOriginal= None

        #variaveis utilizada pelo spinbox para armazenar os dados
        self.v1=DoubleVar()
        self.v2=DoubleVar()
        self.v3=DoubleVar()
        self.v4=DoubleVar()


        self.v2.set(5)    #inicializa o kernel com 5
        self.v3.set(127) # inicializa o minimo com 127
        self.v4.set(255) #inicializa o maximo com 255
        # cria os spinbox

        self.spin2=self.create_spinbox(self.v2,1,0,"Kernel")
        self.spin2=self.create_spinbox(self.v3,0,0,"Min ")
        self.spin2=self.create_spinbox(self.v4,0,1,"Max ")





        # lado direito

        self.frameImages = LabelFrame(self.frameControlsOrganize, text="Images", padx=2, pady=2)
        self.frameImages.pack(padx=5, pady=5, expand=True, fill=X)





        #Configura um frame com grid de 1 coluna e 3 linhas
        self.frameControlsOrganize2 = Frame(self.frameImages)
        self.frameControlsOrganize2.pack(fill=X, expand=False)
        self.frameControlsOrganize2.columnconfigure(0, weight=2)
        self.frameControlsOrganize2.columnconfigure(1, weight=2)

        self.frameControlsOrganize2.grid(row=0, padx=10, sticky="nsew")

        # Imagem cinza
        self.frame_img1 = LabelFrame(self.frameControlsOrganize2, text="Normal Cam", padx=1, pady=1)
        self.frame_img1['width'] = 600
        self.frame_img1['height'] = 600
        self.frame_img1.grid(column=0, row=0)


        # Imagem Alterada
        self.frame_img2 = LabelFrame(self.frameControlsOrganize2, text="Transformation Cam", padx=1, pady=1)
        self.frame_img2['width'] = 600
        self.frame_img2['height'] = 600
        self.frame_img2.grid(column=1, row=0)


    def click(self, event):
        self.mouseXClick = event.x
        self.mouseYClick = event.y
        self.clicked = True

    def release(self, event):
        # type: (object) -> object
        self.clicked = False

    #carrega a imagem comum
    def load_image(self, img, frame, op):

        label_img = Label(frame, width=int(750 - 3), height=int(600 - 3))
        label_img.pack(expand=True, fill=BOTH, padx=2, pady=2)
        if (op == 1 ):
                if(hasattr(self, 'label_img1')):
                    self.label_img1.destroy()
                self.label_img1 = label_img
        elif (op == 2   ):
                if(hasattr(self, 'label_img2')):
                    self.label_img2.destroy()
                self.label_img2 = label_img

        imgResize = Image.fromarray(img).resize((750 - 8, 600 - 8), Image.ADAPTIVE)
        imgtk = ImageTk.PhotoImage(image=imgResize)
        label_img.imgtk = imgtk
        label_img.configure(image=imgtk)







    #cria os botoes spinbox
    def create_spinbox(self, var, col, row,label):
            frameLabel = LabelFrame(self.frameInputValue, text=label, padx=5, pady=5)

            spinbox = Spinbox( frameLabel, from_=-255.0, to=255.0)

            spinbox .configure(activebackground="#f9f9f9")
            spinbox.configure(background="white")
            spinbox.configure(buttonbackground="wheat")
            spinbox.configure(disabledforeground="#b8a786")
            spinbox.configure(font=self.font10)
            spinbox.configure(from_="-255.0")
            spinbox.configure(highlightbackground="black")
            spinbox.configure(selectbackground="#c4c4c4")
            spinbox.configure(textvariable=var)
            spinbox.configure(to="255.0")
            spinbox.pack(padx=5, pady=5, expand=True, fill=X)
            frameLabel.grid(column=col, row=row)

            return spinbox


    def update_image(self):


                # Capture frame-by-frame
                ret, frame = self.cap.read()
                kernel = np.ones((int(self.v2.get()), int(self.v2.get())), np.uint8)
                if ret:
                    # Our operations on the frame come here
                    self.img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.img2=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    if(self.radio.get()==0):#Suavizacao com o glaussiana mediana
                        self.img2=cv2.adaptiveThreshold(self.img2,self.v4.get(),cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
                        self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==1): #Suavizacao glaussiana
                         self.img2=np.copy(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

                         self.img2= cv2.adaptiveThreshold(self.img2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
                         self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==2):#encontra contornos
                         #binario
                         ret, thresh = cv2.threshold(np.copy(self.img2), self.v3.get(),self.v4.get(), 0)
                         # encontra os contornos
                         self.img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                         self.img2=cv2.drawContours(np.copy(self.img1), contours, -1, (0,0,255), 1)
                         self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==3): #Canny Min Max

                            self.img2 = cv2.Canny(self.img2, self.v3.get(),self.v4.get())
                            self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==4):#operacao Gradiente Morphologica
                        # Morphologica Black Hat
                        self.img2 = cv2.morphologyEx(self.img2, cv2.MORPH_BLACKHAT, kernel)
                        self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==5):#Erosao
                        self.img2 = cv2.erode(self.img2, kernel, iterations=1)
                        self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==6):#Dilacao
                        # Realiza a dilatacao
                        self.img2 = cv2.dilate(self.img2, kernel, iterations=1)
                        self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==7):#oeracao Aberta
                        # Realiza oeracao Aberta
                        self.img2 = cv2.morphologyEx(self.img2, cv2.MORPH_OPEN, kernel)
                        self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==8):#oeracao fechada
                        # Realiza operacao Fechada
                        self.img2 = cv2.morphologyEx(self.img2, cv2.MORPH_CLOSE, kernel)
                        self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==9):#oeracao Gradiente Morphologica
                        # Realiza a operacaoo Gradiente Morphologica
                        self.img2 = cv2.morphologyEx(self.img2, cv2.MORPH_GRADIENT, kernel)
                        self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame

                    if(self.radio.get()==10):#operacao binary inverter

                        ret,self.img2 = cv2.threshold(self.img2,self.v3.get(),self.v4.get(),cv2.THRESH_BINARY_INV)

                        self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame
                    if(self.radio.get()==11):#operacao binary

                       ret,self.img2 = cv2.threshold(self.img2,self.v3.get(),self.v4.get(),cv2.THRESH_BINARY)
                       self.load_image(self.img2, self.frame_img2, 2) #chama funcao que mostra imagem no frame

                    self.load_image(self.img1, self.frame_img1, 1) #chama funcao que mostra imagem no frame
                    print("Atualiza frame")
                self.window.after(350,self.update_image )
                self.frameImages.update()

        #duas tecnicas de suavizacao,
        #duas de segmentacao e
        #duas de detecao de bordas em videos capturados

     #ativa a captura de video
    def active_capture(self):
        # trecho da documentacao do python com customizacao pessoal: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
        self.cap = cv2.VideoCapture(0)
        self.update_image()
        return

#instancia a classe
tela = TELA()
tela.window.mainloop()
