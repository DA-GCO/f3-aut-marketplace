from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
import python.llave.login_email as lg
from email.mime.application import MIMEApplication
from datetime import datetime
from email.encoders import encode_base64
dt_string = datetime.now().strftime('%y%m%d')

class EMAILHANDLER():

    def __init__(self) -> None:
        self.destinatario = input("Ingrese el correo del destinatario: ")
        self.remitente = input("Ingrese el correo del remitente: ")
        self.mensaje = MIMEMultipart("related")
        pass

    def header_email(self):
        self.mensaje["From"] = self.destinatario
        self.mensaje["To"] = self.remitente # TODO destinatario != de quién envía 
        self.mensaje["Subject"] = "asunto"

    def body(self):
        html_estado = open("output/archivos correo/local_agg.html", "r").read()
        html_abierto = open("output/archivos correo/estado_agg.html","r").read()
        html_local = open("output/archivos correo/estado_desc.html","r").read()
        email_content = f"""
                    <html>
                        <head>
                            <body>
                                <p> Buen dia equipo market place, amablemente les comparto el informe de F3 - MarketPlace</p>
                                <p> Resumen de F3 por estado </p>
                                {html_abierto}
                                <img src="cid:image1">
                                <p> Resumen F3 por local_agg</p>
                                {html_estado}
                                <img src="cid:image2">
                                <p> Resumen de F3 abiertos por local</p>
                                {html_local}
                                <img src="cid:image3">
                            </body>
                        </head>
                    """
        return email_content

    def build_body(self,email_content):
        msgAlternative = MIMEMultipart('alternative') 
        self.mensaje.attach(msgAlternative)
        msgText = MIMEText(email_content, 'html') 
        msgAlternative.attach(msgText)
        fp = open('output/archivos correo/estado_agg.jpg', 'rb') 
        msgImage = MIMEImage(fp.read()) 
        fp.close()
        fp2 = open('output/archivos correo/local_agg.jpg', 'rb')
        msgImage1 = MIMEImage(fp2.read()) 
        fp2.close()
        fp3 = open('output/archivos correo/estado_desc.jpg', 'rb')
        msgImage2 = MIMEImage(fp3.read()) 
        fp3.close()
        gr = open("output/archivos correo/estado_desc.jpg", 'rb')
        msgImage = MIMEImage(gr.read()) 
        gr.close()

        # arch = open(f'output/planillas/{dt_string}_F3_MKP.xlsx')
        # # arch = open('output/planillas/220131_F3_MKP.xlsx','rb')
        # msgAttach = MIMEApplication(arch.read())
        # arch.close()
        # msgAttach.add_header('Content-Disposition', '<excel1>')
        # Adjuntando excel
        # part = MIMEBase('application', "octet-stream")
        # part.set_payload(open('output/planillas/220131_F3_MKP.xlsx', "rb").read())
        # encode_base64(part)
        # part.add_header(f'Content-Disposition', 'attachment; filename={dt_string}_F3_MKP.xlsx')
        # self.mensaje.attach(part)


        msgImage.add_header('Content-ID', '<image1>') 
        self.mensaje.attach(msgImage)
        msgImage1.add_header('Content-ID', '<image2>') 
        self.mensaje.attach(msgImage1)
        msgImage2.add_header('Content-ID', '<image3>') 
        self.mensaje.attach(msgImage2)

    def send_email(self,correo,contraseña):
        smtp = SMTP("smtp-mail.outlook.com", 587)
        smtp.starttls()
        smtp.login(correo,contraseña)
        smtp.sendmail(self.remitente,self.destinatario,self.mensaje.as_string())
        smtp.quit() 