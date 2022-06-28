import cv2
from tkinter import *
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.message import EmailMessage
import smtplib, ssl

def emailsender(images, mail):

    mails = mail.split(",")
    

    zipz = zipfile.ZipFile('./images/WARNING.zip', 'w', zipfile.ZIP_DEFLATED)

    for image in images:
        zipz.write("./images/"+image+".jpg")

    zipz.close()
    
    

    for email in mails:
        corpo = "##Dete de Movimento## MOVIMENTO DETECTADO"
        de = "matheu.castelo@gmail.com"
        
        msg = MIMEMultipart()
        body_part = MIMEText(corpo, 'plain')
        msg['Subject'] = "DETECTOR DE MOVIMENTO"
        msg['From'] = de
        
        
        msg.attach(body_part)
        
           
        file = "./images/WARNING.zip"
        
       
        with open(file,'rb') as file:
       
            msg.attach(MIMEApplication(file.read(), Name=file.name))

        context=ssl.create_default_context()
    
        msg['To'] = email

        serv = smtplib.SMTP("smtp.gmail.com", 587)
        serv.connect("smtp.gmail.com",587)
        serv.ehlo()
        serv.starttls(context=context)
        serv.login(de, "teteu180500")

        serv.sendmail(msg['From'], msg['To'], msg.as_string())
        serv.quit()
        
        print("Email enviado para: "+ email)

    

def calculaDiferenca(img1, img2, img3):
    """
    Captura o movimento pela subtração de pixel dos frames.
    """
    d1 = cv2.absdiff(img3, img2)
    d2 = cv2.absdiff(img2, img1)
    imagem = cv2.bitwise_and(d1,d2)
    s,imagem = cv2.threshold(imagem, 60, 255, cv2.THRESH_BINARY)
    return imagem


def liga(event):
    """
    Inicia a detecção de movimento utlizando a webcam conectada. Salva as capturas de movimentos em 'C:\Imagens Deteccao/.
    """
    janela = "Tela de Captura"
    janela2 = "Tela Normal"
    i=1
    images = []
    contador = 0

    cv2.namedWindow(janela, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(janela2, cv2.WINDOW_AUTOSIZE)
    webcam = cv2.VideoCapture(2)
    ultima = cv2.cvtColor(webcam.read()[1], cv2.COLOR_RGB2GRAY)
    penultima = ultima
    antepenultima = ultima
    while (True):
        ret, frame = webcam.read()
        antepenultima = penultima
        penultima = ultima
        ultima = cv2.cvtColor(webcam.read()[1], cv2.COLOR_RGB2GRAY)
        cv2.imshow(janela, calculaDiferenca(antepenultima, penultima, ultima))
        cv2.imshow(janela2, frame)

        if contador == 50:
            if not images:
                print("sem interações")
                contador = 0

            else:
                print("PERIGO")
                mail = email.get()
                emailsender(images, mail)
                contador = 0
                images.clear()
                

        contador+=1

        if sum(sum(calculaDiferenca(antepenultima, penultima, ultima))) > 1000:
            print(sum(sum(calculaDiferenca(antepenultima, penultima, ultima))))
            nome = 'image'+str(i)
            print( nome)
            cv2.imwrite('./images/'+nome+".jpg", frame)
            i+=1

            images.append(nome)


        k=cv2.waitKey(10) & 0xFF
        if k == 27:
            webcam.release()
            cv2.destroyWindow(janela)
            cv2.destroyWindow(janela2)
            break

def getemail(event):
    print(email.get())

Janela = Tk()
Janela.title("Detector de Movimento")

label = Label(Janela, text = "Para Desligar a Detecção Pressione Esc.").place(x=80, y=10, width=300, height=50)
label2 = Label(Janela, text = "Se voce deseja enviar e-mail, adcione abaixo:").place(x=80, y=60, width=300, height=50)
label3 = Label(Janela, text = "Se desejar mais de um e-mail, separe por virgula.").place(x=60, y=100, width=350, height=50)
email = Entry(Janela, fg="Black", font="Arial,9")
email.place(x=80, y=150, width=300, height=30)


#botao = Button(Janela, text="Email", fg="Black", font="Arial,9")
#botao.bind("<Button-1>", getemail)
#botao.place(x=120, y=300, width=230, height=50)

botao = Button(Janela, text="Detectar Movimento", fg="Black", font="Arial,9")
botao.bind("<Button-1>", liga)
botao.place(x=120, y=200, width=230, height=50)
Janela.geometry('450x450')
Janela.title("Detector de Movimento")





Janela.mainloop()